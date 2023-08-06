import logging
from typing import Any, Dict, Optional

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.http import JsonResponse
from sentry_sdk import capture_exception
from requests.exceptions import HTTPError

from aims.models import Activity, OipaActivityLink

from . import serializers as oipa_serializers, services as oipa_api

logger = logging.getLogger(__name__)


def set_response(job: str, data: dict, status: int):
    data["job"] = job  # Keep the job number for the client
    cache.set(job, JsonResponse(data, status=status))
    return


@shared_task
def nightly_oipa_pull():
    """ Pull select transactions and budgets for all
        linked activities from OIPA server to Openly.
    """
    logger.debug("Nightly OIPA sync triggered")
    call_command("oipa_sync_transactions")
    logger.debug("Nightly OIPA sync completed")


@shared_task
def oipa_sync_job(openly_id: Optional[str], iati_identifier: Optional[str], job: str):

    results = {"activity": None, "transactions": {}, "validation_results": {}}  # type: Dict[str, Optional[Dict[str,Any]]]
    if getattr(settings, "OIPA_SYNC_ENABLED", True):
        if openly_id == "null":  # javascript null serializeds
            openly_id = None
        if iati_identifier == "null":
            iati_identifier = None
        if iati_identifier and openly_id:
            logger.debug(
                "OipaActivity start search for %s - link to %s",
                iati_identifier,
                openly_id,
            )
            try:
                activity = (
                    Activity.objects.all_openly_statuses().filter(id=openly_id).get()
                )  # type: Activity
            except Activity.DoesNotExist:
                return set_response(
                    job, {"errors": "Mohinga Activity not found."}, status=500
                )
            try:
                oipa = oipa_api.OipaRecords(iati_identifier, job=job)
                set_response(job, {"info": "Fetching activity"}, status=202)
                results["activity"] = oipa.activity
            except HTTPError as e:
                # This generally indicates that there is no OIPA record for the activity;
                # Return a 500 here for correct clientside error message
                logging.fatal(e, exc_info=True)
                return set_response(job, {"errors": "%s" % (e)}, status=500)
            except IndexError as e:
                # This generally indicates that there we've tried to use 'null' as an OIPA id;
                # Return a 500 here for correct clientside error message
                logging.fatal(e, exc_info=True)
                return set_response(job, {"errors": "%s" % (e)}, status=500)
            except AssertionError as e:
                # This generally indicates that there we've tried to use 'null' as an OIPA id;
                # Return a 500 here for correct clientside error message
                logging.fatal(e, exc_info=True)
                return set_response(job, {"errors": "%s" % (e)}, status=500)
            try:
                results["link_info"] = oipa_serializers.OipaActivityLinkSerializer(
                    oipa_api.ActivityLink(openly_id).get_link()
                ).data
                results["sync_records"] = oipa_api.get_syncs(openly_id)

                set_response(job, {"info": "Fetching budgets"}, status=202)
                oipa_budgets = oipa.budgets
                set_response(job, {"info": "Fetching Transactions"}, status=202)
                oipa_trans = oipa.transactions
                set_response(job, {"info": "Processing..."}, status=202)

                oipa_validator = oipa_api.OipaValidator(activity)
                oipa_validator.validate_budgets(oipa_budgets["data"])
                oipa_validator.validate_transactions(oipa_trans)
                results["validation_results"] = oipa_validator.results

                for f in ["B", "C", "OF", "IF"]:
                    try:
                        results["transactions"][f] = {
                            "clean_sum": sum(
                                [
                                    float(r.value)
                                    for r in oipa_validator.clean_records[f]
                                ]
                            ),
                            "clean_count": len(oipa_validator.clean_records[f]),
                            "raw_count": len(oipa_trans[f]["data"])
                            if f != "B"
                            else len(oipa_budgets["data"]),
                            "raw_sum": sum(
                                [float(r["value"]) for r in oipa_trans[f]["data"]]
                            )
                            if f != "B"
                            else sum([float(r["value"]) for r in oipa_budgets["data"]]),
                        }
                        if f != "B" and len(oipa_trans[f]["data"]) > 0:
                            try:
                                currency = oipa_trans[f]["data"][0]["currency"].code
                            except AttributeError:
                                currency = oipa_trans[f]["data"][0]["currency"]
                        elif len(oipa_budgets["data"]) > 0:
                            try:
                                currency = oipa_budgets["data"][0]["currency"].code
                            except AttributeError:
                                currency = oipa_budgets["data"][0]["currency"]
                        else:
                            currency = "USD"
                        results["transactions"][f]["currency"] = currency
                    except TypeError:
                        results["transactions"][f] = {
                            "clean_sum": 0,
                            "clean_count": 0,
                            "raw_count": 0,
                            "raw_sum": 0,
                        }
            except Exception as e:
                logging.fatal(e, exc_info=True)
                if settings.DEBUG:
                    return set_response(
                        job,
                        {"errors": "Could not look up data\n %s" % (e,)},
                        status=500,
                    )
                else:
                    capture_exception()
        else:
            return set_response(job, {"errors": "Missing IATI Activity ID"}, status=500)
    return set_response(job, results, status=200)


@shared_task
def oipa_sync_activities_job(job: str, initial_sync: bool, *linked_activity_ids):
    # pull OIPA records for each of the activities and update in Openly DB
    set_response(job, {"info": "Celery has your task"}, status=202)
    results = {}
    syncer = oipa_api.OipaSync()
    links = OipaActivityLink.objects.filter(pk__in=linked_activity_ids)
    links_count = links.count()
    logger.debug("Sync activities")
    try:
        for link_count, activity_link in enumerate(
            OipaActivityLink.objects.filter(pk__in=linked_activity_ids)
        ):
            set_response(
                job,
                {
                    "info": "Celery has your task and is working on {} ({}/{})".format(
                        activity_link.pk, link_count, links_count
                    )
                },
                status=202,
            )
            results[activity_link.activity_id] = syncer.sync_activity(
                activity_link, initial_sync=initial_sync
            )
    except Exception as e:
        logging.fatal(e, exc_info=True)
        set_response(job, {"errors": str(e)}, 500)
        return cache.get(job)

    set_response(job, {"results": results}, 200)
    return cache.get(job)

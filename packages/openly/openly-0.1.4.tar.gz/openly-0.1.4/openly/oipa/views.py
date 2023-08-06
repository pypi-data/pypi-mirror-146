import logging
import uuid

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from aims.models import Activity

from . import serializers as oipa_serializers, services as oipa_api
from .models import OipaActivityLink
from .tasks import oipa_sync_activities_job, oipa_sync_job

logger = logging.getLogger(__name__)


class OipaActivity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req, iati_identifier=None):
        # celerize = 'celerize' in req.GET
        openly_id = req.GET.get("openly_id", None)
        iati_identifier = req.GET.get("iati_identifier", iati_identifier)
        job = req.GET.get("job", uuid.uuid4())

        if "job" in req.GET:
            if cache.get(job):
                logger.debug("Returning a cached request object")
                return cache.get(job)

        if "celerize" not in req.GET:
            logger.warning(
                "OipaActivity get probably should be run as a celery task to avoid timeouts"
            )
            logger.warning("Your cache key is %s", job)
            oipa_sync_job(openly_id, iati_identifier, job)
            return cache.get(job)

        cache.set(
            job,
            JsonResponse(
                {
                    "info": "Started fetching data from OIPA",
                    "job": job,
                    "debug": "I hope celery is running",
                },
                status=202,
            ),
        )
        oipa_sync_job.delay(openly_id, iati_identifier, job)

        # Because this view is used by different URL schemes, adapt to suit view
        url_name = self.request.resolver_match.url_name

        if url_name == "oipa_activity":
            redirect = reverse(url_name, kwargs={"iati_identifier": iati_identifier})
            return HttpResponseRedirect(
                redirect + "?openly_id={}&celerize&job={}".format(openly_id, job)
            )

        elif url_name == "oipa_activity_by_iati_identifier":
            redirect = reverse(url_name)
            return HttpResponseRedirect(
                redirect
                + "?iati_identifier={}&openly_id={}&celerize&job={}".format(
                    iati_identifier, openly_id, job
                )
            )
        raise AssertionError("I do not know how to resolve that")


class OipaSyncActivities(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req, activity_id=None):
        initial_sync = False
        if getattr(settings, "OIPA_SYNC_ENABLED", True):
            try:
                # grab the OIPA Linked activities with fields to sync up
                linked_activities = OipaActivityLink.objects.exclude(oipa_fields=[])
                if activity_id:
                    initial_sync = True
                    linked_activities = linked_activities.filter(
                        activity_id=activity_id
                    )
                linked_activities = linked_activities.all()

                job = req.GET.get("job", uuid.uuid4())

                if "job" in req.GET:
                    if cache.get(job):
                        logger.debug("Returning a cached request object")
                        return cache.get(job)

                cache.set(
                    job,
                    JsonResponse(
                        {
                            "info": "Started syncing data from OIPA",
                            "job": job,
                            "debug": "I hope celery is running",
                        },
                        status=202,
                    ),
                )

                linked = linked_activities.values_list("pk", flat=True)

                if "celerize" not in req.GET:
                    logger.warning(
                        "OipaSyncActivities get probably should be run as a celery task to avoid timeouts"
                    )
                    logger.warning("Your cache key is %s", job)
                    oipa_sync_activities_job(job, initial_sync, *list(linked))
                    return cache.get(job)
                else:
                    oipa_sync_activities_job.delay(job, initial_sync, *list(linked))
                    return HttpResponseRedirect(
                        reverse(
                            "oipa_sync_activities", kwargs={"activity_id": activity_id}
                        )
                        + "?celerize&job={}".format(job)
                    )
            except Exception as e:
                cache.set(
                    job,
                    JsonResponse(
                        {"error": str(e), "info": str(e), "job": job}, status=500
                    ),
                )
            return cache.get(job)


class IatiIdentifierUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        if not req.POST:
            return JsonResponse({"error": "invalid request"}, status=500)
        else:
            data = req.POST
            # reset the Activity link to prevent data from being accidentally sync'd
            oipa_api.ActivityLink(data["aims-activity-id"]).clear_link()
            # update the Activity with new IATI ID
            Activity.objects.all_openly_statuses().filter(
                id=data["aims-activity-id"]
            ).update(iati_identifier=data["oipa-iati-id"])
            return JsonResponse({"iati_id": data["oipa-iati-id"]})


class OipaActivityLinkUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        if not req.POST:
            return JsonResponse({"error": "invalid request"}, status=500)
        else:
            data = req.POST
            linked_fields = [field for field in ["B", "C", "OF", "IF"] if field in data]
            new_link = oipa_api.ActivityLink(data["aims-activity-id"]).update_link(
                linked_fields
            )
            return JsonResponse(
                oipa_serializers.OipaActivityLinkSerializer(new_link).data
            )


class OipaActivityLinkClear(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        if not req.POST:
            return JsonResponse({"error": "invalid request"}, status=500)
        else:
            data = req.POST
            link = oipa_api.ActivityLink(data["aims-activity-id"])
            if link.link:
                return JsonResponse(link.clear_link())
            else:
                return JsonResponse({})


class OipaActivityLinkDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        if not req.POST:
            return JsonResponse({"error": "invalid request"}, status=500)
        else:
            data = req.POST
            link = oipa_api.ActivityLink(data["aims-activity-id"])
            if link.link:
                return JsonResponse(link.delete_link(), safe=False)
            else:
                return JsonResponse({})

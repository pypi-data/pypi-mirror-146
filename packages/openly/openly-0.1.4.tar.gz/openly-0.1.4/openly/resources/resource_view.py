import datetime
from collections import defaultdict
from datetime import timedelta

from django.apps import apps  # I get used to doing this to prevent circular imports
from django.conf import settings
from django.db.models import Func, TextField, Value as V
from django.db.models.functions import Concat


def rec_dd():
    """
    This little recipe is a lifesaver when building json: a recursive default dict.
    """
    return defaultdict(rec_dd)


class Resources:
    """
    Create an annotated DocumentLinks list
    """

    # Define the 'Heading' which we want to use to display this document
    # This is used to write 'Tags' and a list of document headings
    # "Temporarily" - says Lee - we are using (activity) organisation code
    # and title. Hah. Let's see if this comment is still here in 5 years' time.
    heading_function = Concat(
        Func("reporting_organisation__code", function="TRIM"),
        V("."),
        Func("title__title", function="TRIM"),
        output_field=TextField(),
    )

    def __init__(self, host="https://hamutuk.tl", *args, **kwargs):

        # "headings" language is prioritised here, but obviously based on settings.LANGUAGES
        # make sure that "en" appears first
        language_codes = kwargs.get(
            "language_codes", [lang[0] for lang in settings.LANGUAGES]
        )
        self.language_codes = []
        # and we have to translate "tm" to "tet" for downstream consumption of resources
        for language_code in language_codes:
            if language_code == "tm":
                language_code = "tet"
            self.language_codes.append(language_code)
        self.host = host

    def _details(self):
        """
        The document descriptions
        """
        model = apps.get_model("aims", "DocumentLink")
        details = model.objects.values(
            "id",
            "title",
            "activity_id",
            "language_id",
            "activity__reporting_organisation__name",
            "url",
            "iso_date",
        )
        for detail in details:
            if detail["language_id"] == "tm":
                detail["language_id"] = "tet"
        return details

    def _descriptions(self):
        """
        Document descriptions keyed by activity id and language
        """
        tags = rec_dd()
        model = apps.get_model("aims", "DocumentLink")
        for act, lang, text in model.objects.values_list(
            "activity_id", "language_id", "narrative__description"
        ):
            if lang == "tm":
                lang = "tet"
            tags[act][lang] = text
        return tags

    def _tags(self):
        """
        Generated 'Document tags' keyed by activity and language
        Modify 'self.heading_function' to change how tags are generated for a document
        """
        model = apps.get_model("aims", "Activity")
        tags = rec_dd()
        for act, lang, text in model.objects.annotate(
            h=self.heading_function
        ).values_list("id", "title__language_id", "h"):
            if lang == "tm":
                lang = "tet"
            tags[act][lang] = text
        return tags

    def _headings(self, tags):
        """
        Return the first tag found in order of self.language_codes
        Expects input to be derived from self._tags(), to prevent duplicating the
        db call to generate the tags
        """
        headings = {}
        for tag in tags:
            for language in self.language_codes:
                if language in tag:
                    headings[language] = tag[language]
                    break  # on the first found language
        return headings

    def resources(self):
        """
        Generate the list of DocumentLinks and Headings
        """

        def is_new(resource: dict) -> bool:
            # Return True if the 'iso_date' value is less than 30 days
            resource_date = resource["iso_date"]
            now = datetime.datetime.today().date()
            age = now - resource_date
            return age < timedelta(days=30)

        generated = []
        all_tags = self._tags()
        descriptions = self._descriptions()
        resources = self._details()
        tags = [{}]

        for resource in resources.order_by("-iso_date"):
            if resource["url"] == "" or not resource["url"]:
                # Don't include URLs empty
                # We could filter these out above but it's unlikely to be a major performance drag here
                continue

            aid = resource["activity_id"]

            if resource["url"].startswith(
                "/media"
            ):  # Internal documents get an href to our server
                resource["url"] = self.host + resource["url"]

            tagset = all_tags.get(aid, {})
            tags.append(tagset)

            language_id = resource["language_id"]
            if language_id == "tm":
                language_id = "tet"

            generated.append(
                {
                    "title": {language_id: resource["title"]},
                    "details": dict(descriptions.get(aid, {})),
                    "link": {language_id: resource["url"]},
                    "publicationDate": {language_id: resource["iso_date"]},
                    "author": resource["activity__reporting_organisation__name"],
                    "tags": [dict(tagset)],
                    "new": is_new(resource),
                }
            )

        headings = list(self._headings(tags).values())

        return generated, headings

    def resources_as_dict(self):
        generated, headings = self.resources()

        # Fetch 'foreign' data from the 'ResourceMetaData'
        resource_headings = list(
            apps.get_model("resources", "ResourceHeading").objects.values_list(
                "heading", flat=True
            )
        )
        resource_meta_body = list(
            apps.get_model("resources", "ResourceMetaData").objects.values_list(
                "resource_body", flat=True
            )
        )

        return dict(
            headings=resource_headings + headings,
            resources=resource_meta_body + generated,
        )

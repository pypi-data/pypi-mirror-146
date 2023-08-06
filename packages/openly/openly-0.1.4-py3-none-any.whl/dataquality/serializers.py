from rest_framework import serializers

from aims import models as aims_models


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = aims_models.Title
        fields = ("language", "title")
        extra_kwargs = {"title": {"allow_blank": True}}

    def convert_data(self, data):
        if "narratives" in data and len(data["narratives"]) > 0:
            data["language"] = data["narratives"][0]["language"]["code"]
            data["title"] = data.pop("narratives")[0]["text"]
        return data

    def get_instance_or_none(self, data):
        if "activity" in data:
            queryset = aims_models.Title.objects.filter(activity=data["activity"])
            if queryset.exists():
                return queryset.first()
        return None

    def to_representation(self, title):
        return {"language": title.language_id, "title": title.title}


class ActivityReportingOrganisationSerializer(serializers.ModelSerializer):
    """
    Augments information provided for an Activity in the data quality checks
    """

    class Meta:
        model = aims_models.Organisation
        fields = ("pk", "abbreviation", "name")


class ActivitySerializer(serializers.ModelSerializer):

    title_set = TitleSerializer(many=True, partial=True, required=False)
    reporting_organisation = ActivityReportingOrganisationSerializer(
        many=False, partial=True, required=False
    )

    class Meta:
        model = aims_models.Activity
        fields = ("id", "title_set", "reporting_organisation")

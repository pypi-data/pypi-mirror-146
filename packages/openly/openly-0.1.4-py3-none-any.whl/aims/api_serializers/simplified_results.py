from typing import Dict
from rest_framework import serializers
from aims import models as aims_models


class SimpleResultSerializer(serializers.ModelSerializer):
    """
    This "results" serializer adds Title and Description fields
    These are properties on Result which will set and return an
    appropriate Narrative model

    This serializer is for simple use cases where translated results
    are not required
    """

    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = aims_models.Result
        fields = ("title", "description", "activity", "type", "uuid")

    def create(self, *args, **kwargs):
        self.is_valid()
        title = self.validated_data.pop("title")
        description = self.validated_data.pop("description", "")
        result = super().create(self.validated_data)
        result.title = title
        result.description = description
        result.save()
        return result

    def update(self, *args, **kwargs):
        self.is_valid()
        title = self.validated_data.pop("title")
        description = self.validated_data.pop("description", "")
        result = super().update(*args, **kwargs)
        result.title = title
        result.description = description
        result.save()
        return result


class SimpleResultIndicatorSerializer(serializers.ModelSerializer):

    """
    This "result indicator" serializer uses the title, target and actual properties
    of a proxy model to return a combination of ResultIndicator and Period which
    suits the DIRD use case. Translated fields and time frames are not
    possible with this serializer.
    """

    title = serializers.CharField()
    target = serializers.DecimalField(
        required=False, allow_null=True, max_digits=25, decimal_places=10
    )
    actual = serializers.DecimalField(
        required=False, allow_null=True, max_digits=25, decimal_places=10
    )
    uuid = serializers.UUIDField(required=False)
    result_uuid = serializers.UUIDField(required=False)

    class Meta:
        model = aims_models.SimpleResultIndicator
        # Always return our "Result uuid" in the return to server
        fields = (
            "uuid",
            "result_uuid",
            "title",
            "baseline_value",
            "measure",
            "target",
            "actual",
        )

    def create(self, validated_data):
        # Extract title, target and actual fields from the data. These are properties not fields
        data = {k: validated_data.pop(k, None) for k in "title target actual".split()}

        # Require a UUID-based Result in order to save
        try:
            validated_data["result_id"] = aims_models.Result.objects.get(
                uuid=validated_data.pop("result_uuid")
            ).pk
        except aims_models.Result.DoesNotExist as E:
            raise KeyError(
                "The Result related to this Indicator is not present or has no UUID"
            ) from E

        if self.instance:
            instance = super().update(self.instance, validated_data)
        else:
            instance = super().create(validated_data)

        # Reinstate our property-based "fake fields"
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        # Redirect "updated" to "creates" for dry handling of the fun things
        # we do to make Results simple(r)
        return self.create(validated_data)

    def to_representation(self, instance: aims_models.SimpleResultIndicator) -> Dict:
        """
        Extends the model's serialized representation with the UUID of the related result
        """
        repr = super().to_representation(instance)
        repr["result_uuid"] = instance.result.uuid
        return repr

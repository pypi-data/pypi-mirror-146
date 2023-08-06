from rest_framework import serializers

from .models import OrganisationContactInfo, OrganisationProfile, Person


class OrganisationContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationContactInfo
        fields = '__all__'


class OrganisationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationProfile
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'organisation_profile', 'name', 'position', 'phone_number', 'email', 'order', 'photo')
        related_fields = tuple()

    def create(self, validated_data):
        data = {}
        for related_obj_name in self.Meta.related_fields:

            # Validated data will show the nested structure
            data[related_obj_name] = validated_data.pop(related_obj_name)

        instance = super(PersonSerializer, self).create(validated_data)

        for related_obj_name in self.Meta.related_fields:

            # Validated data will show the nested structure
            related_instance = getattr(instance, related_obj_name)

            # Same as default update implementation
            for attr_name, value in data[related_obj_name].items():
                setattr(related_instance, attr_name, value)
            related_instance.save()
        return instance

    def update(self, instance, validated_data):
        for related_obj_name in self.Meta.related_fields:

            # Validated data will show the nested structure
            data = validated_data.pop(related_obj_name)
            related_instance = getattr(instance, related_obj_name)

            # Same as default update implementation
            for attr_name, value in data.items():
                setattr(related_instance, attr_name, value)
            related_instance.save()
        return super(PersonSerializer, self).update(instance, validated_data)

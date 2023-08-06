from rest_framework import serializers


class OipaActivityLinkSerializer(serializers.Serializer):
    activity_id = serializers.CharField(max_length=150)
    oipa_fields = serializers.ListField()


class OipaSyncRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    activity_id = serializers.CharField(max_length=150)
    b_added = serializers.IntegerField()
    c_added = serializers.IntegerField()
    of_added = serializers.IntegerField()
    if_added = serializers.IntegerField()
    sync_datetime = serializers.DateTimeField()

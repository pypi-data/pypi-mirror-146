from datetime import date, timedelta
from math import ceil

from rest_framework import serializers
from rest_framework.fields import FloatField, IntegerField, ReadOnlyField

from aims import models as aims_models

__all__ = [
    'BudgetSerializer',
    'TransactionSerializer',
    'ActivityTagSerializer',
]


def date_to_quarter(date: date) -> int:
    """
    From a date object returns a value like "20171" for eg first quarter of 2017.
    """
    return date.year * 10 + (ceil(date.month / 3))


def quarter_to_date(quarter: int) -> date:
    """
    Expects a value like "20171" for eg first quarter of 2017.
    """
    year = int(quarter / 10)
    q = quarter - (year * 10)
    end_month = q * 3
    start_month = end_month - 2
    period_start = date(year, start_month, 1)
    if end_month == 12:
        period_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        period_end = date(year, end_month + 1, 1) - timedelta(days=1)
    return period_start, period_end


class BudgetSerializer(serializers.ModelSerializer):
    id = IntegerField(allow_null=True, required=False)
    value = FloatField()

    class Meta:
        model = aims_models.Budget
        fields = ('id', 'activity', 'type', 'status', 'period_start', 'period_end', 'value', 'value_date', 'currency')


class BudgetQuarterSerializer(BudgetSerializer):
    """
    Override serialize/deserialize to give
    a "year" and "quarter" field rather than
    start_date, end_date fields
    """
    currency_id = ReadOnlyField()

    class Meta:
        model = BudgetSerializer.Meta.model
        fields = ('period_start', 'period_end', 'value', 'currency_id')

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        if instance.period_start:
            ret['quarter'] = date_to_quarter(instance.period_start)
        else:
            ret['quarter'] = 1
        ret.pop('period_start')
        ret.pop('period_end')
        return ret

    def to_internal_value(self, data):
        if 'quarter' in data:
            data['period_start'], data['period_end'] = quarter_to_date(data.pop('quarter'))
        return data


class TransactionSerializer(serializers.ModelSerializer):

    currency = serializers.PrimaryKeyRelatedField(read_only=False, required=True, queryset=aims_models.Currency.objects.all())
    provider_organisation = serializers.PrimaryKeyRelatedField(read_only=False, required=True, queryset=aims_models.Organisation.objects.all())
    receiver_organisation = serializers.PrimaryKeyRelatedField(read_only=False, required=True, queryset=aims_models.Organisation.objects.all())

    class Meta:
        model = aims_models.Transaction
        fields = (
            'id',
            'activity',
            'aid_type',  # models.ForeignKey('aims.AidType', null=True, blank=True, on_delete=models.CASCADE)
            'description',  # models.TextField(default="", null=True, blank=True)
            # 'description_type',  # models.ForeignKey('aims.DescriptionType', null=True, blank=True, on_delete=models.CASCADE)
            # 'disbursement_channel',  # models.ForeignKey('aims.DisbursementChannel', null=True, blank=True, on_delete=models.CASCADE)
            'finance_type',  # models.ForeignKey('aims.FinanceType', null=True, blank=True, on_delete=models.CASCADE)
            'flow_type',  # models.ForeignKey('aims.FlowType', null=True, blank=True, on_delete=models.CASCADE)
            'provider_organisation',  # models.ForeignKey('aims.Organisation', related_name="transaction_providing_organisation", null=True, blank=True, on_delete=models.CASCADE)
            # 'provider_organisation_name',  # models.CharField(max_length=255, default="", null=True, blank=True)
            'provider_activity',  # models.CharField(max_length=100, null=True)
            'receiver_organisation',  # models.ForeignKey('aims.Organisation', related_name="transaction_receiving_organisation", null=True, blank=True, on_delete=models.CASCADE)
            # 'receiver_organisation_name',  # models.CharField(max_length=255, default="")
            'tied_status',  # models.ForeignKey('aims.TiedStatus', null=True, blank=True, on_delete=models.CASCADE)
            'transaction_date',  # models.DateField(null=True, default=None)
            'transaction_type',  # models.ForeignKey('aims.TransactionType', null=True, blank=True, on_delete=models.CASCADE)
            'value_date',  # models.DateField(null=True, default=None)
            'value',  # models.DecimalField(max_digits=15, decimal_places=2)
            'currency',  # models.ForeignKey('aims.Currency', null=True, blank=True, on_delete=models.CASCADE),
            'usd_value',
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.validate_usd_value()
        instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.validate_usd_value()
        instance.refresh_from_db()
        return instance


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = aims_models.ContactInfo
        fields = [
            "id",
            "uuid",
            "activity",
            "person_name",
            "organisation",
            "telephone",
            "email",
            "mailing_address",
            "website",
            "contact_type",
            "job_title",
        ]

        extra_kwargs = {
            field_name: {'required': False, 'allow_blank': True} for field_name in
            ['person_name', 'job_title', 'organisation', 'telephone', 'email', 'mailing_address', 'website']
        }


class ActivityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = aims_models.ActivityTag
        fields = ('tag',)


class ActivityNestedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = aims_models.Activity
        fields = ('pk', 'activitytag_set')

    activitytag_set = ActivityTagSerializer(many=True, read_only=True)

    def create(self, validated_data):
        raise NotImplementedError('Cannot create an Activity from this serializer')

    def update(self, instance, validated_data):
        # Pull out the nested funding sources from the serializer
        if 'activitytag_set' in self.initial_data:
            aims_models.ActivityTag.set_for_activity(
                instance,
                map(lambda obj: obj['tag'], self.initial_data['activitytag_set'])
            )
            instance = super().update(instance, validated_data)
        return instance

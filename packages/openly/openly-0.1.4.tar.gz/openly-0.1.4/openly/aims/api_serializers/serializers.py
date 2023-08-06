"""
Serializers defined in this file are used in the editor APIs.
They were shamelessly copy pasted from the oipa_serializers.
To do: clean up the logic in this file that is specific to importing from oipa.
"""
import logging
import random
from collections import Counter, OrderedDict
from decimal import Decimal
from itertools import product
from typing import Dict, Optional, Set, Tuple

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, empty, IntegerField, SerializerMethodField, UUIDField

import aims.models as aims_models
from iati_codelists import models as iati_codelists
from aims.models import StatusEnabledLocalData
from simple_locations.models import Area
import warnings

from .changes import v201_to_v105

logger = logging.getLogger(__name__)


def change_key(json_obj, old_key, new_key):
    ''' Given a dict D this moves key k1 to k2 so that {.. k1: v ..} -> {.. k2: v ..}.'''
    if old_key in json_obj:
        json_obj[new_key] = json_obj.pop(old_key)
    return json_obj


class FlexibleModelDeserializer(serializers.ModelSerializer):
    ''' Extends the Django Rest Framework ModelSerializer class to allow parsing, validation,
    and storage of different representations.

    By default ModelSerializer requires as input a dict-like data object containing k,v pairs
    such that the keys map exactly to field names on the serializer. FlexibleModelDeserializer
    provides a convert_data method that subclasses can implement to convert any data format
    to the dictlike object expected by the underlying ModelSerializer. Additionally
    get_instance_or_none is provided to return an existing model instance corresponding to
    given data. This is required to properly handle whether to create or update an object.
    '''

    def to_internal_value(self, data: Dict[str, str]):
        ''' Overrides ModelSerializer.to_internal_value to first parse and transform the
        given data to a format expected by the base class. Additionally self.instance is
        set to the existing model if such an object corresponding to the data exists in the
        database.
        '''
        if data is not empty:
            self.convert_data(data)
        return super(FlexibleModelDeserializer, self).to_internal_value(data)

    def convert_data(self, data):
        return data

    def get_instance_or_none(self, data):
        return None


class ForeignKeyChoiceSerializer(serializers.ModelSerializer):
    """ A model serializer used to set a foreign key among options existing in the database.

    A subclass should declare Meta.model and Meta.fields.
    """

    def to_representation(self, instance):
        if not instance.pk:
            return {'code': None}
        return {field_name: getattr(instance, field_name) for field_name in self.Meta.fields}

    def get_value(self, data):
        """ Override the default get_value to transform {'code': None} into None. """
        value = super(ForeignKeyChoiceSerializer, self).get_value(data)
        if isinstance(value, dict) and (value['code'] is None or value['code'] == ''):
            return None
        return value

    def to_internal_value(self, data):
        try:
            return self.Meta.model.objects.get(code=data['code'])
        except self.Meta.model.DoesNotExist:
            raise ValidationError('code "{}" does not exist'.format(data['code']))

    def validate_empty_values(self, data):
        if isinstance(data, dict) and data['code'] is None:
            if not self.allow_null:
                self.fail('null')
            else:
                return (True, None)
        return super(ForeignKeyChoiceSerializer, self).validate_empty_values(data)

    def get_attribute(self, transaction):
        """ When the foreign key is None, this method returns an empty object that will be picked up by
        to_representation. In turn, to_representation returns {'code': None}. """
        representation = super(ForeignKeyChoiceSerializer, self).get_attribute(transaction)
        if representation is not None:
            return representation
        else:
            return self.Meta.model()


class OrganisationDeserializer(FlexibleModelDeserializer):
    ''' Deserializes and validates the JSON objects returned by the OIPA/3.0 API into a format
    recognized by aims.models.Organisation.
    '''

    class Meta:
        model = aims_models.Organisation
        fields = ('code', 'type', 'reported_by_organisation', 'name')

    def get_instance_or_none(self, data):
        pk = data['code']
        if aims_models.Organisation.objects.filter(pk=pk).exists():
            return aims_models.Organisation.objects.get(pk=pk)
        return None

    def convert_data(self, data):
        # Remapped fields
        change_key(data, 'organisation_identifier', 'code')
        change_key(data, 'primary_name', 'name')

        # Extract the organisation identifier of the reporting org
        reporting_orgs = data.pop('reporting_orgs', [])
        if len(reporting_orgs) == 1:
            data['type'] = reporting_orgs[0]['org_type']['code']

        # Extract the name of the reporting organisation if set
        reported_by_orgs = data.pop('reported_by_orgs', [])
        if reported_by_orgs:
            reported_by_organisation = aims_models.Organisation.objects.get(
                code=reported_by_orgs[0]['organisation']
            )
            data['reported_by_organisation'] = reported_by_organisation.name

        return data

    def to_internal_value(self, data):
        if data is not empty:
            self.convert_data(data)
        org_code = data.pop('code')
        if 'type' in data and data['type'] is not None:
            data['type'] = aims_models.OrganisationType.objects.get(pk=int(data['type']))
        return aims_models.Organisation.objects.update_or_create(code=org_code, defaults=data)[0]


class TitleDeserializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.Title
        fields = ('language', 'title')
        extra_kwargs = {'title': {'allow_blank': True}}

    def convert_data(self, data):
        if 'narratives' in data and len(data['narratives']) > 0:
            data['language'] = data['narratives'][0]['language']['code']
            data['title'] = data.pop('narratives')[0]['text']
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data:
            queryset = aims_models.Title.objects.filter(activity=data['activity'])
            if queryset.exists():
                return queryset.first()
        return None

    def to_representation(self, title):
        return {'language': title.language_id, 'title': title.title}


class BudgetTypeSerializer(ForeignKeyChoiceSerializer):
    class Meta:
        model = aims_models.BudgetType
        fields = ('code', 'name')
        extra_kwargs = {
            'code': {'initial': 1},
            'name': {'initial': 'Original'},
        }


class BudgetStatusSerializer(ForeignKeyChoiceSerializer):
    class Meta:
        model = aims_models.BudgetStatus
        fields = ('code', 'name')
        extra_kwargs = {
            'code': {'initial': 1},
            'name': {'initial': 'Indicative'},
        }


class CurrencySerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.Currency
        fields = ('code', 'name')


class BudgetDeserializer(FlexibleModelDeserializer):
    id = IntegerField(allow_null=True, required=False)
    type = BudgetTypeSerializer()
    status = BudgetStatusSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = aims_models.Budget
        fields = '__all__'
        extra_kwargs = {
            'period_start': {'required': True, 'allow_null': False},
            'period_end': {'required': True, 'allow_null': False},
        }

    def convert_data(self, data):
        if 'value' in data and isinstance(data['value'], dict):
            data['value_date'] = data['value']['date']
            data['currency'] = data['value']['currency']['code']
            data['value'] = data.pop('value')['value']
        if 'activity' in data and isinstance(data['activity'], dict):
            data['activity'] = data['activity']['id']
        data['date_modified'] = timezone.now().date()
        if 'type' in data and isinstance(data['type'], dict):
            if data['type']['code'] is not None:
                data['type']['code'] = int(data['type']['code'])
        if 'status' in data and isinstance(data['status'], dict):
            if data['status']['code'] is not None:
                data['status']['code'] = int(data['status']['code'])
        if 'id' in data and not isinstance(data['id'], int) and data['id']:
            data['id'] = int(data['id'])
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data:
            queryset = aims_models.Budget.objects.filter(
                activity=data['activity'],
                period_start=data['period_start'],
                period_end=data['period_end'],
                value=data['value'],
                value_date=data['value_date']
            )
            if queryset.exists():
                return queryset.first()
        return None

    def validate(self, data):
        if data.get('period_end', '') < data.get('period_start', ''):
            raise ValidationError({'period_end': _('The budget end date cannot be before the budget start date')})
        return data

    def to_representation(self, budget):
        serialized_budget = super(BudgetDeserializer, self).to_representation(budget)
        serialized_budget['activity'] = {'id': serialized_budget['activity']}
        return serialized_budget


class DescriptionDeserializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.Description
        fields = ('type', 'language', 'description')
        extra_kwargs = {'description': {'allow_blank': True}}

    def convert_data(self, data):
        if ('narratives' in data and data['narratives'] is not None and len(data['narratives']) > 0):
            data['language'] = data['narratives'][0]['language']['code']
            data['description'] = data.pop('narratives')[0]['text']
        if ('type' in data and data['type'] is not None and len(data['type']) > 0):
            data['type'] = data.pop('type')['code']
        return data

    def get_instance_or_none(self, data):
        if 'description' in data and 'activity' in data:
            queryset = aims_models.Description.objects.filter(activity=data['activity'],
                                                              description=data['description'])
            if queryset.exists():
                return queryset.first()
        return None

    def to_representation(self, instance):
        data = super(DescriptionDeserializer, self).to_representation(instance)
        data['type'] = {'code': data.pop('type')}
        return data

    @staticmethod
    def add_missing_descriptions(serialized_activity):
        """ Add missing descriptions with an empty string in the `description` field.

        'missing' means descriptions that don't exist for a certain (activity_id, type_id, language_id) combination.
        Missing descriptions will be added to serialized_activity['descriptions'].
        """
        language_codes = (lang[0] for lang in settings.LANGUAGES)
        type_codes = aims_models.DescriptionType.objects.values_list('code', flat=True)
        # create a set where the keys are [language_code, type_code]
        existing_codes = {(d['language'], d['type']['code']) for d in serialized_activity['descriptions']}
        all_codes = {(language_code, type_code) for language_code, type_code in product(language_codes, type_codes)}
        missing_codes = list(all_codes - existing_codes)
        for language_code, type_code in missing_codes:
            serialized_activity['descriptions'].append(
                {'language': language_code, 'type': {'code': type_code}, 'description': ''})


class OrganisationChoiceSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.Organisation
        fields = ('code',)


class OrganisationRoleSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.OrganisationRole
        fields = ('code',)


class ActivityParticipatingOrganisationDeserializer(FlexibleModelDeserializer):
    ''' Deserializes and validates the JSON objects returned by the OIPA/3.0 API into a format
    recognized by aims.models.ActivityParticipatingOrganisation.
    '''
    organisation = OrganisationChoiceSerializer(required=False, allow_null=True)
    role = OrganisationRoleSerializer()

    class Meta:
        model = aims_models.ActivityParticipatingOrganisation
        fields = ('organisation', 'role', 'name')

    def to_representation(self, participating_organisation) -> Optional[str]:
        data = super(ActivityParticipatingOrganisationDeserializer, self).to_representation(participating_organisation)
        data['name'] = participating_organisation.organisation.full_name if participating_organisation.organisation else None
        return data

    def convert_data(self, data):
        # Check whether organisation exists and if so remap key
        org_id = data.pop('ref', None)
        if aims_models.Organisation.objects.filter(code=org_id).exists():
            data['organisation'] = {'code': org_id}

        # Get the organisation's role in this activity
        if data['role'] is not None and data['role']['code'] in v201_to_v105['OrganisationRole']:
            data['role']['code'] = v201_to_v105['OrganisationRole'][data['role']['code']]

        # If a name is given then set this
        if 'narratives' in data:
            narratives = data.pop('narratives')
            if len(narratives) == 1:
                data['name'] = narratives[0]['text']
        return data

    def get_instance_or_none(self, data):
        # Only return an ActivityParticipatingOrganisation if activity, organsation, and role
        # are all set
        if 'activity' in data and 'organisation' in data and 'role' in data:
            queryset = aims_models.ActivityParticipatingOrganisation.objects.filter(
                activity=data['activity'],
                organisation=data['organisation'],
                role=data['role']
            )
            if queryset.exists():
                return queryset.first()
        return None


class PolicyMarkerSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.PolicyMarker
        fields = ('code', 'name')


class PolicySignificanceSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.PolicySignificance
        fields = ('code', 'name', 'description')


class ActivityPolicyMarkerDeserializer(FlexibleModelDeserializer):
    policy_marker = PolicyMarkerSerializer()
    policy_significance = PolicySignificanceSerializer()

    class Meta:
        model = aims_models.ActivityPolicyMarker
        fields = ('id', 'alt_policy_marker', 'policy_marker', 'vocabulary', 'policy_significance')

    def to_internal_value(self, data):
        data['policy_marker_id'] = data.pop('policy_marker')['code']
        if 'vocabulary' in data and len(data['vocabulary']) > 0:
            data['vocabulary_id'] = data.pop('vocabulary')['code']
            if data['vocabulary_id'] in v201_to_v105['SectorVocabulary']:
                data['vocabulary_id'] = v201_to_v105['SectorVocabulary'][data['vocabulary_id']]
        if 'significance' in data:
            if data['significance'] is not None:
                data['policy_significance_id'] = data.pop('significance')['code']
            else:
                data.pop('significance')
        if 'narratives' in data:
            narratives = data.pop('narratives')
            if len(narratives) == 1:
                data['alt_policy_marker'] = narratives[0]['text']
        return aims_models.ActivityPolicyMarker(**data)

    def to_representation(self, activity_policy_marker):
        data = super(ActivityPolicyMarkerDeserializer, self).to_representation(activity_policy_marker)
        data['vocabulary'] = {'code': data.pop('vocabulary')}
        data['significance'] = data.pop('policy_significance')
        data['narratives'] = [{'text': data.pop('alt_policy_marker')}]
        return data


class SectorSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.Sector
        fields = ('code', 'name', 'category')


class ActivitySectorDeserializer(FlexibleModelDeserializer):
    sector = SectorSerializer()

    class Meta:
        model = aims_models.ActivitySector
        fields = ('id', 'alt_sector_name', 'percentage', 'sector', 'vocabulary')

    def to_internal_value(self, data):
        """
        Converts a Sector to an ActivitySector
        This also assigns a "vocabulary" where appropriate
        A "vocabulary" is a 3 digit or 5 digit OECD code,
        or can be a specific organisation determined code

        OECD codes are in `aims_models.Sector`
        """
        sector = aims_models.Sector.objects.get(code=data["sector"]["code"])  # type: Optional[aims_models.Sector]
        data['alt_sector_name'] = data['sector'].get('name', "")

        # Determine the appropriate "Vocabulary ID"
        # "RO" for national, "DAC-3" / "DAC-5" for OECD codes
        try:
            if aims_models.NationalSector.objects.filter(code=sector.code).exists():
                data["vocabulary"] = aims_models.Vocabulary.objects.get(pk="RO")
            elif aims_models.IATISector.dac_3.filter(code=sector.code).exists():
                data["vocabulary"] = aims_models.Vocabulary.objects.get(pk="DAC-3")
            elif aims_models.IATISector.dac_5.filter(code=sector.code).exists():
                data["vocabulary"] = aims_models.Vocabulary.objects.get(pk="DAC-5")

        except aims_models.Vocabulary.DoesNotExist:
            warnings.warn("An expected vocabulary item %s does not exist", (vocab_id))
        data['sector'] = sector
        return aims_models.ActivitySector(**data)

    def to_representation(self, activity_sector):
        data = super(ActivitySectorDeserializer, self).to_representation(activity_sector)
        data['vocabulary'] = {'code': data.pop('vocabulary')}
        return data

    @staticmethod
    def separate_sectors_and_sectors_working_groups(data):
        data['sector_working_groups'] = []
        sectors_without_working_groups = []
        codes_of_sector_working_groups = set(aims_models.NationalSector.objects.values_list('code', flat=True))
        for sector in data['sectors']:
            if sector['sector']['code'] in codes_of_sector_working_groups:
                sector['sector_working_group'] = sector.pop('sector')
                data['sector_working_groups'].append(sector)
            else:
                sectors_without_working_groups.append(sector)
        data['sectors'] = sectors_without_working_groups


class ActivityRecipientCountryDeserializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.ActivityRecipientCountry

    def convert_data(self, data):
        if 'country' in data and len(data['country']):
            data['country'] = data.pop('country')['code']
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data and 'country' in data:
            queryset = aims_models.ActivityRecipientCountry.objects.filter(
                activity=data['activity'],
                country=data['country']
            )
            if queryset.exists():
                return queryset.first()
        return None


class ActivityRecipientRegionDeserializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.ActivityRecipientRegion

    def convert_data(self, data):
        if 'region' in data and len(data['region']):
            data['region'] = data.pop('region')['code']
        if 'vocabulary' in data and len(data['vocabulary']) > 0:
            data['vocabulary'] = data.pop('vocabulary')['code']
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data and 'region' in data:
            queryset = aims_models.ActivityRecipientRegion.objects.filter(
                activity=data['activity'],
                region=data['region']
            )
            if queryset.exists():
                return queryset.first()
        return None


class LocationDeserializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.Location
        fields = ('id', 'adm_code', 'percentage', 'name', 'adm_country_adm1', 'adm_country_adm2')

    LOCATION_CLASS_ID = 1
    COUNTRY_TYPE_ID = 'ADMD'
    REGION1_TYPE_ID = 'ADM1'
    REGION2_TYPE_ID = 'ADM2'

    def get_instance_or_none(self, data):
        if 'activity' in data:
            queryset = aims_models.Location.objects.filter(
                activity=data['activity'],
                adm_country_adm1=data.get('adm_country_adm1', None),
                adm_country_adm2=data.get('adm_country_adm2', None)
            )
            if queryset.exists():
                return queryset.first()
        return None

    def to_representation(self, location: aims_models.Location):
        serialized_location = super(LocationDeserializer, self).to_representation(location)
        return {
            'location': {
                'code': location.adm_code,
                'name': location.name,
            },
            'percentage': serialized_location['percentage'],
            'id': serialized_location['id']
        }

    def to_internal_value(self, validated_data):
        """
        Return an instance of 'Location' with
        the area and percentage. Assigns the area name to the location.
        """
        code = validated_data['location']['code']
        area = Area.objects.filter(pk=int(code)).first()  # type: Optional[Area]
        return aims_models.Location(
            percentage = Decimal(validated_data['percentage']),
            area=area,
            name=area.name if area else '',
            adm_code=code
        )


class AidTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.AidType
        fields = ('code', 'name', 'description')


class DisbursementChannelSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.DisbursementChannel
        fields = ('code', 'name')


class FinanceTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.FinanceType
        fields = ('code', 'name')


class FlowTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.FlowType
        fields = ('code', 'name', 'description')


class TiedStatusSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.TiedStatus
        fields = ('code', 'name', 'description')


class TransactionTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.TransactionType
        fields = ('code', 'name', 'description')


class OrganisationChoiceSerializer(ForeignKeyChoiceSerializer):
    """ A serializer used to choose among organisations. """

    class Meta:
        model = aims_models.Organisation
        fields = ('code', 'name')


class TransactionDeserializer(FlexibleModelDeserializer):
    id = IntegerField(allow_null=True, required=False)
    aid_type = AidTypeSerializer(required=False, allow_null=True)
    disbursement_channel = DisbursementChannelSerializer(required=False, allow_null=True)
    finance_type = FinanceTypeSerializer(required=False, allow_null=True)
    flow_type = FlowTypeSerializer(required=False, allow_null=True)
    tied_status = TiedStatusSerializer(required=False, allow_null=True)
    transaction_type = TransactionTypeSerializer()
    currency = CurrencySerializer()
    provider_organisation = OrganisationChoiceSerializer(required=False)
    receiver_organisation = OrganisationChoiceSerializer(required=False)

    class Meta:
        model = aims_models.Transaction
        fields = (
            'id', 'activity', 'description', 'transaction_type', 'transaction_date', 'currency', 'value', 'value_date',
            'provider_organisation', 'receiver_organisation', 'disbursement_channel', 'aid_type', 'finance_type',
            'flow_type', 'tied_status')
        extra_kwargs = {'transaction_date': {'required': True}}

    def convert_data(self, data):
        if 'activity' in data:
            data['activity'] = data['activity'].pop('id', None)
            activity = aims_models.Activity.objects.filter(id=data['activity']).first()
        else:
            activity = None
        if 'description' in data:
            description = data.pop('description')
            if description is not None and 'narratives' in description:
                narrative = description['narratives'][0]
                if 'text' in narrative:
                    data['description'] = narrative['text']
        if ('finance_type' not in data or data[
                'finance_type'] is None) and activity is not None and activity.default_finance_type_id is not None:
            data['finance_type'] = {'code': activity.default_finance_type_id}
        if 'provider_organisation' in data and data['provider_organisation'] is not None:
            provider_org_dict = data.pop('provider_organisation')
            org_ref = provider_org_dict['code'] if 'code' in provider_org_dict else provider_org_dict['ref']
            if 'narratives' in provider_org_dict and len(provider_org_dict['narratives']) > 0:
                data['provider_organisation_name'] = provider_org_dict['narratives'][0]['text']
            if 'provider_activity' in provider_org_dict:
                data['provider_activity'] = provider_org_dict['provider_activity']
            if aims_models.Organisation.objects.filter(code=org_ref).exists():
                data['provider_organisation'] = {'code': org_ref}
        elif 'provider_organisation' not in data and activity is not None:
            data['provider_organisation'] = {'code': activity.reporting_organisation_id}
        if 'receiver_organisation' in data and data['receiver_organisation'] is not None:
            receiver_org_dict = data.pop('receiver_organisation')
            org_ref = receiver_org_dict['code'] if 'code' in receiver_org_dict else receiver_org_dict['ref']
            if 'narratives' in receiver_org_dict and len(receiver_org_dict['narratives']) > 0:
                data['receiver_organisation_name'] = receiver_org_dict['narratives'][0]['text']
            if aims_models.Organisation.objects.filter(code=org_ref).exists():
                data['receiver_organisation'] = {'code': org_ref}
        if 'ref' in data and data['ref'] is None:
            data.pop('ref')
        if 'transaction_type' in data and data['transaction_type'] is not None:
            transaction_type = data['transaction_type']
            if transaction_type['code'] in v201_to_v105['TransactionType']:
                transaction_type['code'] = v201_to_v105['TransactionType'][transaction_type['code']]

        data['date_modified'] = timezone.now().date()
        return data

    def get_instance_or_none(self, data):
        if ('activity' in data and 'transaction_date' in data and 'provider_organisation' in data and 'value' in data):
            queryset = aims_models.Transaction.objects.filter(
                activity__iati_identifier=aims_models.Activity.objects.get(
                    pk=data['activity']
                ).iati_identifier,
                transaction_date=data['transaction_date'],
                provider_organisation=data['provider_organisation'],
                value=data['value']
            )
            if queryset.exists():
                return queryset.first()
        return None

    def to_representation(self, transaction):
        serialized_transaction = super(TransactionDeserializer, self).to_representation(transaction)
        serialized_transaction['activity'] = {'id': serialized_transaction['activity']}
        return serialized_transaction


class CollaborationTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.CollaborationType
        fields = ('code', 'name')


class ActivityStatusSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.ActivityStatus
        fields = ('code', 'name')

    def validate_empty_values(self, data):
        return super(ActivityStatusSerializer, self).validate_empty_values(data)


class ActivityDeserializer(FlexibleModelDeserializer):
    ''' Deserializes and validates the JSON objects returned by the OIPA/3.0 API into a format
    recognized by aims.models.Activity.
    '''
    reporting_organisation = OrganisationDeserializer(partial=True)
    activity_status = ActivityStatusSerializer(required=False, allow_null=True)
    collaboration_type = CollaborationTypeSerializer(required=False, allow_null=True)
    participating_organisations = ActivityParticipatingOrganisationDeserializer(partial=True, many=True, required=False)
    activitypolicymarker_set = ActivityPolicyMarkerDeserializer(partial=True, many=True, required=False)
    activitysector_set = ActivitySectorDeserializer(partial=True, many=True, required=False)
    description_set = DescriptionDeserializer(partial=True, many=True, required=False)
    budget_set = BudgetDeserializer(partial=True, many=True, required=False)
    title_set = TitleDeserializer(many=True, partial=True, required=False)
    location_set = LocationDeserializer(partial=True, many=True, required=False)

    default_currency = CurrencySerializer(required=False, allow_null=True)
    default_aid_type = AidTypeSerializer(required=False, allow_null=True)
    default_finance_type = FinanceTypeSerializer(required=False, allow_null=True)
    default_flow_type = FlowTypeSerializer(required=False, allow_null=True)
    default_tied_status = TiedStatusSerializer(required=False, allow_null=True)

    class Meta:
        model = aims_models.Activity
        fields = ('id', 'internal_identifier', 'iati_identifier', 'default_currency', 'hierarchy',
                  'last_updated_datetime', 'linked_data_uri', 'secondary_publisher',
                  'activity_status', 'start_planned', 'end_planned', 'start_actual',
                  'end_actual', 'collaboration_type', 'default_flow_type',
                  'default_aid_type', 'default_finance_type', 'default_tied_status',
                  'xml_source_ref', 'scope', 'reporting_organisation',
                  'participating_organisations', 'activitypolicymarker_set', 'activitysector_set',
                  'title_set', 'description_set', 'budget_set', 'location_set',
                  'openly_status', 'completion_percentage', 'completion_tasks', 'date_created', 'date_modified',
                  'start_planned_detail', 'end_planned_detail', 'start_actual_detail', 'end_actual_detail',
                  )
        many_fields = {
            'participating_organisations': 'participating_organisations',
            'activitypolicymarker_set': 'policy_markers',
            'description_set': 'descriptions',
            'budget_set': 'budget_set',
            'location_set': 'locations',
            'activitysector_set': 'sectors',
        }
        extra_kwargs = {
            'id': {'required': False},
            'iati_identifier': {'required': False},
            'xml_source_ref': {'allow_blank': True},
            'linked_data_uri': {'allow_blank': True},
            'last_updated_datetime': {'allow_blank': True},
            **{f: {'required': False} for f in ('start_planned_detail', 'end_planned_detail', 'start_actual_detail', 'end_actual_detail')},
        }

    @staticmethod
    def eager(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related(
            'sector',
            'title_set',
            'location_set',
            'description_set',
            'participating_organisations',
            'transaction_set',
            'transaction_set__provider_organisation',
            'transaction_set__receiver_organisation',
            'participating_organisations',
            'participating_organisations__role',
            'participating_organisations__organisation',
            'activitypolicymarker_set',
            'activitysector_set',
            'activitysector_set__sector__category',
        ).select_related(
            'reporting_organisation',
        )
        return queryset

    @classmethod
    def eager_id(cls, activity_id):
        return cls.eager(aims_models.Activity.objects.filter(pk=activity_id))

    def __init__(self, *args, **kwargs):
        """ editor_creation will create activities as draft. It's used by the editor."""
        self.force_publish = kwargs.pop('force_publish', False)
        self.editor_creation = kwargs.pop('editor_creation', False)
        super(ActivityDeserializer, self).__init__(*args, **kwargs)

    def get_initial(self):
        """ Used when a serializer is instantiated with no instance and no data. """
        data = super(ActivityDeserializer, self).get_initial()
        for internal_name, external_name in self.Meta.many_fields.items():
            data[external_name] = data.pop(internal_name)
        DescriptionDeserializer.add_missing_descriptions(data)
        data['activity_dates'] = [{'type': {'code': type_code}, 'iso_date': None} for type_code in range(1, 5)]
        data['sector_working_groups'] = []
        return data

    def get_instance_or_none(self, data):
        if self.instance is not None:
            return self.instance
        id = data.get('iati_identifier', None)
        if id is None:
            return None
        if aims_models.Activity.objects.filter(iati_identifier=id).exists():
            return aims_models.Activity.objects.get(iati_identifier=id)
        elif aims_models.Activity.objects.iatixml().filter(iati_identifier=id).exists():
            aims_models.Activity.objects.iatixml().filter(iati_identifier=id).delete()
        return None

    def convert_locations(self, data):
        locations = data.pop('locations', None)
        if locations is None:
            return
        data['locations'] = []
        if aims_models.Activity.objects.filter(iati_identifier=data['iati_identifier'], location__isnull=False) \
                .exclude(location__adm_country_adm1='') \
                .exists():
            for location in aims_models.Activity.objects.get(
                    iati_identifier=data['iati_identifier']).location_set.all():
                data['locations'].append(OrderedDict({
                    'adm_country_adm1': location.adm_country_adm1,
                    'adm_country_adm2': location.adm_country_adm2,
                    'percentage': location.percentage,
                }))
        else:
            data['locations'].append(OrderedDict({
                'adm_country_adm1': 'Nation-wide',
            }))

    def get_new_activity_identifier(self, org_code):
        exists = True
        while exists:
            id_number = str(random.randint(0, 10000)).zfill(4)
            iati_identifier = '%s-%s' % (org_code.replace(' ', '_'), id_number)
            exists = aims_models.Activity.objects.filter(iati_identifier=iati_identifier).exists()
        return iati_identifier

    def convert_data(self, data):
        # Get the instance first so we can pass pk to many-related models where necessary
        self.instance = self.get_instance_or_none(data)

        if not self.editor_creation:
            self.convert_locations(data)

        for field_internal_name, field_external_name in list(self.Meta.many_fields.items()):
            field_value = data.pop(field_external_name, None)
            data[field_internal_name] = field_value

        if 'scope' in data and data['scope'] is not None:
            data['scope'] = data.pop('scope')['code']

        for field in list(data.keys()):
            if data[field] is None:
                data.pop(field)

        if data.get('activity_dates', None):
            activity_dates = data.pop('activity_dates', [])
            for activity_date in activity_dates:
                if "iso_date" in activity_date:
                    type_code = int(activity_date['type']['code'])
                    if type_code == 1:
                        data['start_planned'] = activity_date['iso_date']
                    elif type_code == 2:
                        data['start_actual'] = activity_date['iso_date']
                    elif type_code == 3:
                        data['end_planned'] = activity_date['iso_date']
                    elif type_code == 4:
                        data['end_actual'] = activity_date['iso_date']
                    else:
                        raise KeyError('Not a valid date type')
            self.validate_activity_dates(data)

        if 'sector_working_groups' in data:
            # merge the sector working groups with the sectors, because they are stored in the same table
            if 'activitysector_set' not in data:
                data['activitysector_set'] = []
            for sector_working_group in data['sector_working_groups']:
                sector_working_group['sector'] = sector_working_group.pop('sector_working_group')
            data['activitysector_set'].extend(data['sector_working_groups'])

        return data

    def validate_activity_dates(self, data):
        for date_name in ['start_planned', 'start_actual', 'end_planned', 'end_actual']:
            data[date_name] = data.get(date_name, None)
            if data[date_name] == '':
                data[date_name] = None

        if data['start_planned'] is not None and data['end_planned'] is not None:
            if data['start_planned'] > data['end_planned']:
                raise ValidationError(
                    {'activity_dates': _('Your planned end date must be after your planned start date')})
        if data['start_actual'] is not None and data['end_actual'] is not None:
            if data['start_actual'] > data['end_actual']:
                raise ValidationError(
                    {'activity_dates': _('Your actual end date must be after your actual start date')})
        if (data['end_planned'] or data['end_actual']) and not (data['start_planned'] or data['start_actual']):
            raise ValidationError(
                {'activity_dates': _('If you set end dates you must set at least one start date.')})

    def validate_participating_organisations(self, data):
        """ Validate that the same organisation wasn't entered twice for the same role. """
        orgs_and_roles = [(d['organisation'], d['role']) for d in data]
        org_and_role_count = Counter(orgs_and_roles)  # a dict (organisation, role) -> count
        duplicates = [org_and_role for org_and_role, count in org_and_role_count.items() if count > 1]
        if not duplicates:
            return data
        error_message = []
        for (organisation, role) in duplicates:
            error_message.append('Organisation {} with role {} was entered twice'.format(organisation.code, role.code))
        raise ValidationError(error_message)

    def validate_openly_status(self, openly_status):
        """
        When attempting to publish an activity, validate that the activity has all the publishing requirements.
        """
        if openly_status == self.instance.openly_status:
            return openly_status

        if not self.instance.can_change_openly_status(self.context['request'].user, openly_status):
            raise PermissionDenied()

        if (openly_status in (self.instance.OPENLY_STATUS_PUBLISHED, self.instance.OPENLY_STATUS_REVIEW) and
                self.instance.openly_status != self.instance.OPENLY_STATUS_PUBLISHED):
            publish_errors = self.instance.publish_errors
            if len(publish_errors):
                raise ValidationError(publish_errors)

        # Looks like there is going to be a status change. Log this.
        alm = aims_models.ActivityLogmessage(activity=self.instance)
        alm.body = {
            'type': 'status_change',
            'uid': self.context['request'].user.id,
            'from': self.instance.openly_status,
            'to': openly_status,
        }
        alm.save()
        return openly_status

    def to_representation(self, activity):
        data = super(ActivityDeserializer, self).to_representation(activity)
        # Force translations, otherwise we may attempt to JSON encode the lazy translation object
        data['activity_dates'] = [
            {'type': {'code': 1, 'name': str(_('Planned Start Date'))}, 'iso_date': data.pop('start_planned')},
            {'type': {'code': 2, 'name': str(_('Actual Start Date'))}, 'iso_date': data.pop('start_actual')},
            {'type': {'code': 3, 'name': str(_('Planned End Date'))}, 'iso_date': data.pop('end_planned')},
            {'type': {'code': 4, 'name': str(_('Actual End Date'))}, 'iso_date': data.pop('end_actual')},
        ]
        # ex: rename the 'description_set' key to 'descriptions'
        for internal_key, oipa_key in self.Meta.many_fields.items():
            data[oipa_key] = data.pop(internal_key)
        DescriptionDeserializer.add_missing_descriptions(data)

        ActivitySectorDeserializer.separate_sectors_and_sectors_working_groups(data)
        return data

    def extract_many_related_data(self, validated_data):
        many_related_data = {}
        for field_name in self.Meta.many_fields.keys():
            if field_name in validated_data:
                many_related_data[field_name] = validated_data.pop(field_name)
            else:
                many_related_data[field_name] = None
        return many_related_data

    def create(self, validated_data):
        ''' Create an aims.models.Activity model based on the validated_data. If the
        deserializer was initialized with force_publish set to True then we will publish the
        corresponding aims.models.Activity model.
        '''
        many_related_data = self.extract_many_related_data(validated_data)

        titles = validated_data.pop('title_set', [])

        if self.editor_creation:
            validated_data['id'] = self.get_new_activity_identifier(validated_data['reporting_organisation'].code)
        activity = aims_models.Activity(**validated_data)
        activity.save()
        aims_activity = aims_models.Activity.objects.iatixml().get(id=activity.id)
        if self.force_publish:
            aims_activity.openly_status = StatusEnabledLocalData.OPENLY_STATUS_PUBLISHED
        if self.editor_creation:
            aims_activity.openly_status = StatusEnabledLocalData.OPENLY_STATUS_BLANK
        aims_activity.save()

        if many_related_data['participating_organisations'] is not None:
            for participating_organisation in many_related_data['participating_organisations']:
                aims_models.ActivityParticipatingOrganisation(activity=activity,
                                                              **participating_organisation).save()
        if many_related_data['activitypolicymarker_set'] is not None:
            for policy_marker in many_related_data['activitypolicymarker_set']:
                aims_models.ActivityPolicyMarker(activity=activity, **policy_marker).save()
        if many_related_data['activitysector_set'] is not None:
            for sector in many_related_data['sectors']:
                aims_models.ActivitySector(activity=activity, **sector).save()
        if many_related_data['description_set'] is not None:
            for description in many_related_data['description_set']:
                aims_models.Description(activity=activity, **description).save()
        if many_related_data['budget_set'] is not None:
            for budget in many_related_data['budget_set']:
                aims_models.Budget(activity=activity, **budget).save()
        if many_related_data['location_set'] is not None:
            for location in many_related_data['location_set']:
                aims_models.Location(activity=activity, **location).save()

        for title in titles:
            title['activity'] = activity
            aims_models.Title.objects.update_or_create(**title)

        return aims_activity

    @atomic
    def update(self, activity: aims_models.Activity, validated_data):
        ''' Update the published activity if force_publish was set to True during initialization
        If not then we create a new aims.models.Activity model corresponding with
        openly_status iatixml.
        '''

        # on the first update, the status will be changed from blank to draft
        # the main effect is to make the activity appear in the organisation activity manager
        if activity.openly_status == aims_models.StatusEnabledLocalData.OPENLY_STATUS_BLANK:
            activity.openly_status = aims_models.StatusEnabledLocalData.OPENLY_STATUS_DRAFT

        logger.debug('Handling many_related_data')
        many_related_data = self.extract_many_related_data(validated_data)

        logger.debug('Handling Titles')
        for title in validated_data.pop('title_set', []):
            title_text = title.get('title', '')
            title_lang = title.get('language', 'en')
            try:
                title_in_database = aims_models.Title.objects.get(activity=activity, language=title_lang)
                if title_text != title_in_database.title:
                    logger.debug('Update text of activity:%s lang:%s from %s to %s', activity.pk, title_lang, title_in_database.title, title_text)
                    title_in_database.title = title_text
                    title_in_database.save()
                else:
                    logger.debug('Title text of activity:%s lang:%s is unchanged %s', activity.pk, title_lang, title_in_database.title)
            except aims_models.Title.DoesNotExist:
                logger.debug('Title text of activity:%s lang:%s created: %s', activity.pk, title_lang, title_text)
                aims_models.Title.objects.create(activity=activity, language=title_lang, title=title_text)

        logger.debug('Processing Participating organisations')
        if many_related_data['participating_organisations'] is not None:
            participating_organisations = []
            for participating_organisation in many_related_data['participating_organisations']:
                role = participating_organisation.get('role')
                organisation = participating_organisation.get('organisation')
                # A 'Participating Organisation' might have a name, an Organisation relationship, or both
                # Prefer to use 'organisation.name' if given else use 'name'
                if 'organisation' not in participating_organisation or (not participating_organisation['organisation'] and participating_organisation['name']):
                    name = participating_organisation.get('name', None)
                else:
                    name = participating_organisation['organisation'].name
                participating_org_record, _ = aims_models.ActivityParticipatingOrganisation.objects.update_or_create(
                    organisation=organisation, role=role, activity=activity,
                    defaults={'name': name})

                participating_organisations.append(participating_org_record)

            # Remove excluded ActivityParticipatingOrganisation
            aims_models.ActivityParticipatingOrganisation.objects.filter(activity=activity)\
                .exclude(pk__in=[po.pk for po in participating_organisations])\
                .delete()

        if many_related_data['description_set'] is not None:
            logger.debug('Processing Descriptions')
            for description in many_related_data['description_set']:
                try:
                    obj = aims_models.Description.objects.get(activity=activity, language=description.get('language', None), type=description.get('type', None))
                    if obj.description != description.get('description'):
                        obj.description = description.get('description')
                        obj.save()
                except aims_models.Description.DoesNotExist:
                    obj = aims_models.Description.objects.create(activity=activity, language=description.get('language', None), type=description.get('type', None), description=description.get('description', ''))

        if many_related_data['budget_set'] is not None:
            logger.debug('Processing Budgets')
            for budget in many_related_data['budget_set']:

                if budget.get('id'):
                    obj = aims_models.Budget.objects.get(pk=budget['id'])
                else:
                    obj = aims_models.Budget()

                obj.activity = activity
                obj.type = budget.get('type', None)
                obj.period_start = budget.get('period_start', '')
                obj.period_end = budget.get('period_end', '')
                obj.value = budget.get('value')
                obj.value_date = budget.get('value_date', None)
                obj.currency = budget.get('currency', None)

                obj.save()

            logger.debug('Drop budgets which were not submitted')
            budget_ids = [budget.get('id') for budget in many_related_data['budget_set']]
            to_delete = aims_models.Budget.objects.filter(activity=activity).exclude(pk__in=budget_ids)
            to_delete.delete()

        if many_related_data['location_set'] is not None:
            logger.debug('Processing percentages for locations')
            self.proportionate_percentages(many_related_data['location_set'])

        for many_field_name in ('location_set', 'activitysector_set', 'activitypolicymarker_set'):
            if many_related_data[many_field_name] is not None:
                # Reset many_to_one fields
                self.reset_many_to_one(many_field_name, many_related_data[many_field_name])

        for field_name, field_value in validated_data.items():
            # ex: set the activity status
            # do not allow setting the activity status back to "blank"
            if field_name == 'openly_status' and field_value == aims_models.StatusEnabledLocalData.OPENLY_STATUS_BLANK:
                continue
            setattr(activity, field_name, field_value)

        if validated_data.get('openly_status', None) == 'draft':
            activity.activityendorsement_set.all().delete()

        activity.date_modified = timezone.now().date()
        activity.save()
        return activity

    def reset_many_to_one(self, many_field_name, list_to_create):
        """ Delete the existing objects for that many field, then create new ones from the list_to_create.

        Deleting and recreating is necessary because the front-end does not track the IDs for these objects.
        """
        activity = self.instance
        logger.info('Deleting {} for activity {}'.format(many_field_name, activity.pk))
        getattr(activity, many_field_name).all().delete()
        for one_of_many in list_to_create:
            one_of_many.activity = activity
            one_of_many.save()

    @staticmethod
    def proportionate_percentages(locations):
        """ When the percentages don't equal 100, adapt them so that they do. """
        percentage_sum = sum([loc.percentage for loc in locations])
        if percentage_sum == 0:
            for location in locations:
                location.percentage = 100 / len(locations)
        else:
            for location in locations:
                location.percentage = location.percentage * 100 / percentage_sum


class ActivityManyRelatedSerializer(FlexibleModelDeserializer):
    """ Subclass this serializer for models that have a foreign key to activity.

    It makes the conversion between the default PrimaryKeySerializer used for activities,
    and the format we use {'id': <activity_id>}.
    """

    def convert_data(self, data):
        if 'activity' in data and isinstance(data['activity'], dict):
            data['activity'] = data['activity']['id']
        return data

    def to_representation(self, instance):
        data = super(ActivityManyRelatedSerializer, self).to_representation(instance)
        data['activity'] = {'id': data['activity']}
        return data


class ContactTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.ContactType
        fields = ('code', 'name')


class ContactSerializer(ActivityManyRelatedSerializer):
    contact_type = ContactTypeSerializer(required=False, allow_null=True)
    id = IntegerField(allow_null=True, required=False)
    uuid = UUIDField(allow_null=True, required=False, validators=[])

    class Meta:
        model = aims_models.ContactInfo
        fields = '__all__'
        extra_kwargs = {
            field_name: {'required': False, 'allow_blank': True} for field_name in
            ['person_name', 'job_title', 'organisation', 'telephone', 'email', 'mailing_address', 'website']
        }


class DocumentCategorySerializer(ForeignKeyChoiceSerializer):
    class Meta:
        model = aims_models.DocumentCategory
        fields = ('code', 'name')


class LanguageSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.Language
        fields = ('code', 'name')


class ActivityDateTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.ActivityDateType
        fields = ('code', 'name')


class AidTypeCategorySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.AidTypeCategory
        fields = ('code', 'name', 'desciption')


class CollaborationTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.CollaborationType
        fields = ('code', 'name', 'description')


class ConditionTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.ConditionType
        fields = ('code', 'name')


class DescriptionTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.DescriptionType
        fields = ('code', 'name', 'description')


class DocumentCategoryCategorySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.DocumentCategoryCategory
        fields = ('code', 'name')


class FileFormatSerializer(ForeignKeyChoiceSerializer):
    class Meta:
        model = aims_models.FileFormat
        fields = ('code', 'name')


class FinanceTypeCategorySerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = aims_models.FinanceTypeCategory
        fields = ('code', 'name', 'description')


class GazetteerAgencySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.GazetteerAgency
        fields = ('code', 'name')


class GeographicalPrecisionSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.GeographicalPrecision
        fields = ('code', 'name', 'description')


class GeographicLocationClassSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.GeographicLocationClass
        fields = ('code', 'name')


class GeographicLocationReachSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.GeographicLocationReach
        fields = ('code', 'name')


class GeographicExactnessSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.GeographicExactness
        fields = ('code', 'name')


class LocationTypeCategorySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.LocationTypeCategory
        fields = ('code', 'name')


class LocationTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.LocationType
        fields = ('code', 'name', 'description', 'category')


class OrganisationIdentifierSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.OrganisationIdentifier
        fields = ('code', 'abbreviation', 'name')


class OrganisationRoleSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.OrganisationRole
        fields = ('code', 'name', 'description')


class OrganisationTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.OrganisationType
        fields = ('code', 'name')


class PublisherTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.PublisherType
        fields = ('code', 'name')


class RelatedActivityTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.RelatedActivityType
        fields = ('code', 'name', 'description')


class SectorCategorySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.SectorCategory
        fields = ('code', 'name', 'description')


class VerificationStatusSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.VerificationStatus
        fields = ('code', 'name')


class ActivityScopeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.ActivityScope
        fields = ('code', 'name')


class AidTypeFlagSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.AidTypeFlag
        fields = ('code', 'name')


class BudgetIdentifierSectorCategorySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.BudgetIdentifierSectorCategory
        fields = ('code', 'name')


class BudgetIdentifierSectorSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.BudgetIdentifierSector
        fields = ('code', 'name', 'category')


class BudgetIdentifierSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.BudgetIdentifier
        fields = ('code', 'name', 'category')


class LoanRepaymentPeriodSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.LoanRepaymentPeriod
        fields = ('code', 'name')


class LoanRepaymentTypeSerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.LoanRepaymentType
        fields = ('code', 'name')


class OrganisationRegistrationAgencySerializer(FlexibleModelDeserializer):

    class Meta:
        model = aims_models.OrganisationRegistrationAgency
        fields = ('code', 'name', 'description', 'category', 'url')


class ActivityBudgetDeserializer(serializers.ModelSerializer):
    budget_set = BudgetDeserializer(many=True, partial=True, required=True)

    class Meta:
        model = aims_models.Activity
        fields = ('budget_set',)
        validators = []

    def update(self, instance, validated_data):

        for budget in validated_data['budget_set']:
            if budget.get('id'):
                obj = aims_models.Budget.objects.get(pk=budget['id'])
            else:
                obj = aims_models.Budget()

            obj.activity = instance
            obj.type = budget.get('type', None)
            obj.period_start = budget.get('period_start', '')
            obj.period_end = budget.get('period_end', '')
            obj.value = budget.get('value')
            obj.value_date = budget.get('value_date', None)
            obj.currency = budget.get('currency', None)

            obj.save()
            logger.debug('Save budget: %s', obj)

        budget_ids = [budget.get('id') for budget in validated_data['budget_set']]
        logger.debug('Keeping budgets %s', budget_ids)
        to_delete = aims_models.Budget.objects.filter(activity=instance).exclude(pk__in=budget_ids)
        logger.debug('Drop budgets: %s', to_delete)
        to_delete.delete()

        return instance


class ResultTypeSerializer(ForeignKeyChoiceSerializer):
    """
    DEPRECATED - Keeping this for backwards compatibility
    """
    # TODO: Remove this class once openly_phd, openly_hamutuk use the new Results models

    class Meta:
        model = iati_codelists.ResultType
        fields = ('code', 'name')


class ResultSerializer(ActivityManyRelatedSerializer):
    """
    DEPRECATED - Keeping this for backwards compatibility
    """
    # TODO: Remove this class once openly_phd, openly_hamutuk use the new Results models

    type = ResultTypeSerializer(required=False, allow_null=True)
    id = IntegerField(allow_null=True, required=False)

    class Meta:
        model = aims_models.Result
        fields = ('activity', 'type', 'title', 'description', 'id')
        extra_kwargs = {
            field_name: {'required': False, 'allow_blank': True} for field_name in ('title', 'description')
        }


class ActivityResultsDeserializer(serializers.ModelSerializer):
    """
    DEPRECATED - Keeping this for backwards compatibility
    """
    # TODO: Remove this class once openly_phd, openly_hamutuk use the new Results models

    results = ResultSerializer(many=True, partial=True, required=True)

    class Meta:
        model = aims_models.Activity
        fields = ('results',)
        validators = []

    def update(self, instance, validated_data):
        results = validated_data['results']
        result_ids = []
        for result in results:

            if result.get('id'):
                obj = aims_models.Result.objects.get(pk=result['id'])
            else:
                obj = aims_models.Result()

            obj.activity = instance
            obj.type = result['type']
            obj.title = result['title']
            obj.description = result['description']
            obj.save()
            result_ids.append(obj.id)

        to_delete = aims_models.Result.objects.filter(activity=instance).exclude(pk__in=result_ids)
        to_delete.delete()

        return instance


class ActivityContactSerializer(serializers.ModelSerializer):
    contactinfo_set = ContactSerializer(many=True, partial=True, required=True)

    class Meta:
        model = aims_models.Activity
        fields = ('contactinfo_set', 'completion_percentage', 'completion_tasks')
        validators = []

    def update(self, instance, validated_data):
        contacts = validated_data['contactinfo_set']
        for contact in contacts:
            if contact.get('id'):
                obj = aims_models.ContactInfo.objects.get(pk=contact['id'])
            else:
                obj = aims_models.ContactInfo()
            obj.activity = instance
            for key, value in contact.items():
                setattr(obj, key, value)
            obj.save()
        contact_ids = [contact.get('id') for contact in contacts]
        to_delete = aims_models.ContactInfo.objects.filter(activity=instance).exclude(pk__in=contact_ids)
        to_delete.delete()
        return instance


class ActivityTransactionSerializer(serializers.ModelSerializer):
    transaction_set = TransactionDeserializer(many=True, partial=True, required=True)

    class Meta:
        model = aims_models.Activity
        fields = ('transaction_set', 'completion_percentage', 'completion_tasks')
        validators = []

    def update(self, instance: aims_models.Activity, validated_data: Dict):
        # Any transactions not seen in the response will be removed
        # This is a complete replacement

        def create_or_update() -> Tuple[Set[int], Set[int]]:
            created = set()
            updated = set()
            for transaction in validated_data['transaction_set']:
                if transaction.get('id'):
                    obj = aims_models.Transaction.objects.get(pk=transaction['id'])
                else:
                    obj = aims_models.Transaction()
                obj.activity = instance
                for key, value in transaction.items():
                    setattr(obj, key, value)
                obj.save()

                if transaction.get('id'):
                    updated.add(obj.pk)
                else:
                    created.add(obj.pk)
            return created, updated

        def delete(keep: Set[int]) -> Set[int]:
            aims_models.Transaction.objects.filter(
                activity=instance
            ).exclude(
                pk__in=keep
            ).delete()

        created, updated = create_or_update()
        delete(keep=created | updated)
        return instance


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'kind', 'parent')


class DocumentNarrativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = aims_models.DocumentNarrative
        fields = ('description', 'language')


class DocumentSerializer(serializers.ModelSerializer):
    id = IntegerField(required=False)
    title = CharField(allow_blank=True)
    url = CharField(allow_blank=True, required=False)

    # Add some properties for file type
    file_size = SerializerMethodField()
    upload = SerializerMethodField()
    file_type = SerializerMethodField()
    org_name = SerializerMethodField()
    activity_name = SerializerMethodField()

    narrative = DocumentNarrativeSerializer(required=False, many=True, read_only=True)  # See DocumentsViewset for how this is saved
    categories = serializers.PrimaryKeyRelatedField(allow_empty=True, many=True, queryset=aims_models.DocumentCategory.objects.all())
    types = serializers.PrimaryKeyRelatedField(allow_empty=True, many=True, queryset=aims_models.ResourceType.objects.all())

    class Meta:
        model = aims_models.DocumentLink
        fields = (
            "id",
            "activity",
            "organisation",
            "org_name",
            "activity_name",
            "url",
            "file_format",
            "categories",
            "title",
            "file_size",
            "upload",
            "file_type",
            "iso_date",
            "language",
            "narrative",
            "private",
            "date_created",
            "date_modified",
            "types",
        )

    def get_file_size(self, obj):
        if hasattr(obj, "upload") and obj.upload.doc:
            try:
                return obj.upload.doc.size
            except FileNotFoundError:
                pass

    def get_file_type(self, obj):
        if hasattr(obj, "upload") and obj.upload.doc:
            # Naive - just return the file extension
            return obj.upload.doc.name.split(".")[-1]

    def get_upload(self, obj):
        if hasattr(obj, "upload") and obj.upload.doc:
            return obj.upload.pk

    def get_org_name(self, obj):
        try:
            return obj.organisation.name
        except AttributeError:
            return None

    def get_activity_name(self, obj):
        try:
            return obj.activity.title
        except AttributeError:
            return None


class DocumentUploadSerializer(serializers.ModelSerializer):
    documentlink = DocumentSerializer(required=False, allow_null=True, read_only=True)

    class Meta:
        model = aims_models.DocumentUpload
        fields = ('documentlink', 'doc')

    def to_internal_value(self, data):
        # Allow a primary key link to DocumentLink

        def get_doc_title():
            title = data['doc'].name
            title = title.replace('-', ' ')
            title = title.replace('_', ' ')
            title = title.replace('.', ' ')
            title = ' '.join(title.split(' ')[:-1])
            return title

        data.pop('csrfmiddlewaretoken', '')
        activity_id = data.pop('activity', '')[0]
        document_link_id = data.pop('documentlink', '')[0]

        if document_link_id.isdigit():
            data['documentlink'] = aims_models.DocumentLink.objects.get(pk=int(document_link_id))

        else:
            try:
                activity = aims_models.Activity.objects.get(id=activity_id)
            except BaseException:
                raise Exception('Ouch {}'.format(activity_id))

            data['documentlink'] = aims_models.DocumentLink.objects.create(
                activity=activity,
                title=get_doc_title()
            )
            try:
                data['documentlink'].file_format = aims_models.FileFormat.objects.get(code=data['doc'].content_type)
                data['documentlink'].save()
            except aims_models.FileFormat.DoesNotExist:
                pass

        # Save document descriptions

        return data


class ActivityCompletionSerializer(serializers.ModelSerializer):

    completion_percentage = SerializerMethodField()
    completion_tasks = SerializerMethodField()

    class Meta:
        model = aims_models.Activity
        fields = ('completion_percentage', 'completion_tasks')

    def get_completion_percentage(self, obj):
        return obj.completion_percentage

    def get_completion_tasks(self, obj):
        return obj.completion_tasks


class ResourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = aims_models.ResourceType
        fields = '__all__'


class ActivityLogmessageSerializer(serializers.ModelSerializer):
    """
    Note that this serializer expects instances of the `objects` (Manager) passed
    in order to resolve the author and title fields
    """
    class Meta:
        model = aims_models.ActivityLogmessage
        fields = [
            "type",
            "time_stamp",
            "message",
            "author",
            "title"
        ]

    type = serializers.SerializerMethodField()
    time_stamp = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_type(self, obj: aims_models.ActivityLogmessage):
        return obj.body.get('type')

    def get_time_stamp(self, obj: aims_models.ActivityLogmessage):
        return obj.tstamp.isoformat()

    def get_message(self, obj: aims_models.ActivityLogmessage):
        message, params = obj.message()
        return message.format(**params)

    def get_author(self, obj: aims_models.ActivityLogmessage):
        return getattr(obj, "author", None)

    def get_title(self, obj: aims_models.ActivityLogmessage):
        return getattr(obj, "title", None)

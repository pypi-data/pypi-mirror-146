from collections import OrderedDict


from rest_framework import serializers
from rest_framework.fields import empty

import aims.models as aims_models
from iati_codelists import models as iati_codelists
from aims.models import StatusEnabledLocalData

from .changes import v201_to_v105


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

    def __init__(self, *args, **kwargs):
        self._convert = True
        if 'convert' in kwargs:
            self._convert = kwargs.pop('convert')

        super(FlexibleModelDeserializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        ''' Overrides ModelSerializer.to_internal_value to first parse and transform the
        given data to a format expected by the base class. Additionally self.instance is
        set to the existing model if such an object corresponding to the data exists in the
        database.
        '''
        if data is not empty:
            if self._convert:
                self.convert_data(data)
            self.instance = self.get_instance_or_none(data)
        return super(FlexibleModelDeserializer, self).to_internal_value(data)

    def convert_data(self, data):
        return data

    def get_instance_or_none(self, data):
        return None


class OrganisationTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.OrganisationType
        fields = ('code', 'name')

    def get_instance_or_none(self, data):
        pk = data['code']
        try:
            return aims_models.OrganisationType.objects.get(pk=pk)
        except aims_models.OrganisationType.DoesNotExist:
            return None


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
        reporting_orgs = data.pop('reporting_orgs')
        if len(reporting_orgs) == 1:
            data['type'] = reporting_orgs[0]['org_type']['code']

        # Extract the name of the reporting organisation if set
        reported_by_orgs = data.pop('reported_by_orgs')
        if len(reported_by_orgs) > 0:
            reported_by_organisation = aims_models.Organisation.objects.get(
                code=reported_by_orgs[0]['organisation']
            )
            data['reported_by_organisation'] = reported_by_organisation.name

        return data


class ReportingOrganisationDeserializer(FlexibleModelDeserializer):
    ''' Deserializes and validates the JSON objects returned by the OIPA/3.0 API into a format
    recognized by aims.models.Organisation.
    '''
    type = OrganisationTypeSerializer(partial=True)

    class Meta:
        model = aims_models.Organisation
        fields = ('code', 'type', 'reported_by_organisation', 'name')

    def get_instance_or_none(self, data):
        pk = data['code']
        try:
            return aims_models.Organisation.objects.get(pk=pk)
        except aims_models.Organisation.DoesNotExist:
            return None

    def convert_data(self, data):
        change_key(data, 'ref', 'code')
        return data

    def validate(self, data):
        assert self.instance is not None, "We cannot import activities with references to an unknown Organisation"
        return super(ReportingOrganisationDeserializer, self).validate(data)


class TitleDeserializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.Title
        fields = '__all__'
        # remove the default <UniqueTogetherValidator> which would make activity a required field,
        # and does not play well with our partial inclusion of this serializer
        validators = []

    def convert_data(self, data):
        if 'narratives' in data and len(data['narratives']) > 0:
            data['language'] = data['narratives'][0]['language']['code']
            data['title'] = data.pop('narratives')[0]['text'][0:255]
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data:
            queryset = aims_models.Title.objects.filter(activity=data['activity'])
            if queryset.exists():
                return queryset.first()
        return None


class BudgetDeserializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.Budget
        fields = '__all__'

    def convert_data(self, data):
        if 'value' in data:
            data['value_date'] = data['value']['date']
            data['currency'] = data['value']['currency']['code']
            data['value'] = data.pop('value')['value']
        if 'type' in data and data['type'] is not None and len(data['type']) > 0:
            data['type'] = data.pop('type')['code']
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


class DescriptionDeserializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.Description
        fields = ('type', 'language', 'description')

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


class ActivityParticipatingOrganisationDeserializer(FlexibleModelDeserializer):
    ''' Deserializes and validates the JSON objects returned by the OIPA/3.0 API into a format
    recognized by aims.models.ActivityParticipatingOrganisation.
    '''
    class Meta:
        model = aims_models.ActivityParticipatingOrganisation
        fields = ('organisation', 'role', 'name')

    def convert_data(self, data):
        # Check whether organisation exists and if so remap key
        org_id = data.pop('ref')
        if aims_models.Organisation.objects.filter(code=org_id).exists():
            data['organisation'] = org_id

        # Get the organisation's role in this activity
        data['role'] = v201_to_v105['OrganisationRole'][data.pop('role')['code']]

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
            return aims_models.ActivityParticipatingOrganisation.objects.filter(
                activity=data['activity'],
                organisation=data['organisation'],
                role=data['role']
            ).first()
        return None


class ActivityPolicyMarkerDeserializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.ActivityPolicyMarker
        fields = '__all__'

    def convert_data(self, data):
        if 'code' in data and len(data['code']) > 0:
            data['policy_marker'] = data.pop('code')['code']
        if 'vocabulary' in data and len(data['vocabulary']) > 0:
            data['vocabulary'] = v201_to_v105['PolicyMarkerVocabulary'][data.pop('vocabulary')['code']]
        if 'significance' in data and len(data['significance']) > 0:
            data['policy_significance'] = data.pop('significance')['code']
        if 'narratives' in data:
            narratives = data.pop('narratives')
            if len(narratives) == 1:
                data['alt_policy_marker'] = narratives[0]['text']
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data and 'policy_marker' in data:
            queryset = aims_models.ActivityPolicyMarker.objects.filter(
                activity=data['activity'],
                policy_marker=data['policy_marker']
            )
            if queryset.exists():
                return queryset.first()
        return None


class ActivitySectorDeserializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.ActivitySector
        fields = ('id', 'alt_sector_name', 'percentage', 'sector', 'vocabulary')

    def convert_data(self, data):
        if 'sector' in data and len(data['sector']) > 0:
            data['alt_sector_name'] = data['sector']['name']
            data['sector'] = data.pop('sector')['code']
        if 'vocabulary' in data and len(data['vocabulary']) > 0:
            data['vocabulary'] = v201_to_v105['SectorVocabulary'][data.pop('vocabulary')['code']]
        return data

    def get_instance_or_none(self, data):
        if 'activity' in data and 'sector' in data:
            queryset = aims_models.ActivitySector.objects.filter(
                activity=data['activity'],
                sector=data['sector']
            )
            if queryset.exists():
                return queryset.first()
        return None


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
        fields = '__all__'

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


class TransactionDeserializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.Transaction
        fields = '__all__'

    def convert_data(self, data):
        if 'activity' in data and len(data['activity']) > 0:
            data['activity'] = data.pop('activity')['id']
        if 'aid_type' in data and data['aid_type'] is not None:
            data['aid_type'] = data.pop('aid_type')['code']
        if 'description' in data:
            description = data.pop('description')
            if description is not None and 'narratives' in description:
                try:
                    narrative = description['narratives'][0]
                    if 'text' in narrative:
                        data['description'] = narrative['text']
                except IndexError:
                    pass
        if 'disbursement_channel' in data and data['disbursement_channel'] is not None:
            data['disbursement_channel'] = int(data.pop('disbursement_channel'))
        if 'finance_type' in data and data['finance_type'] is not None:
            data['finance_type'] = data.pop('finance_type')['code']
        elif aims_models.Activity.objects.get(id=data['activity']).default_finance_type is not None:
            data['finance_type'] = aims_models.Activity.objects.get(id=data['activity']).default_finance_type.code
        if 'flow_type' in data and data['flow_type'] is not None:
            data['flow_type'] = data.pop('flow_type')['code']
        if 'provider_organisation' in data and data['provider_organisation'] is not None:
            provider_org_dict = data.pop('provider_organisation')
            org_ref = provider_org_dict['ref']
            if 'narratives' in provider_org_dict and len(provider_org_dict['narratives']) > 0:
                data['provider_organisation_name'] = provider_org_dict['narratives'][0]['text']
            data['provider_activity'] = provider_org_dict['provider_activity']
            if aims_models.Organisation.objects.filter(code=org_ref).exists():
                data['provider_organisation'] = org_ref
        else:
            data['provider_organisation'] = aims_models.Activity.objects.get(id=data['activity']).reporting_organisation.code
        if 'receiver_organisation' in data and data['receiver_organisation'] is not None:
            receiver_org_dict = data.pop('receiver_organisation')
            org_ref = receiver_org_dict['ref']
            if 'narratives' in receiver_org_dict and len(receiver_org_dict['narratives']) > 0:
                data['receiver_organisation_name'] = receiver_org_dict['narratives'][0]['text']
            if aims_models.Organisation.objects.filter(code=org_ref).exists():
                data['receiver_organisation'] = org_ref
        if 'ref' in data and data['ref'] is None:
            data.pop('ref')
        if 'tied_status' in data and data['tied_status'] is not None:
            data['tied_status'] = data.pop('tied_status')['code']
        if 'transaction_type' in data and data['transaction_type'] is not None:
            data['transaction_type'] = v201_to_v105['TransactionType'][data.pop('transaction_type')['code']]
        if 'currency' in data and data['currency'] is not None:
            data['currency'] = data.pop('currency')['code']

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


class ActivityDeserializer(FlexibleModelDeserializer):
    ''' Deserializes and validates the JSON objects returned by the OIPA/3.0 API into a format
    recognized by aims.models.Activity.
    '''
    reporting_organisation = ReportingOrganisationDeserializer(partial=True)
    participating_organisation = ActivityParticipatingOrganisationDeserializer(partial=True,
                                                                               many=True)
    policy_marker = ActivityPolicyMarkerDeserializer(partial=True, many=True)
    sector = ActivitySectorDeserializer(partial=True, many=True)
    description_set = DescriptionDeserializer(partial=True, many=True)
    budget_set = BudgetDeserializer(partial=True, many=True)
    title_set = TitleDeserializer(partial=True)
    location_set = LocationDeserializer(partial=True, many=True)

    class Meta:
        model = aims_models.Activity
        fields = ('iati_identifier', 'default_currency', 'hierarchy',
                  'last_updated_datetime', 'linked_data_uri', 'secondary_publisher',
                  'activity_status', 'start_planned', 'end_planned', 'start_actual',
                  'end_actual', 'collaboration_type', 'default_flow_type',
                  'default_aid_type', 'default_finance_type', 'default_tied_status',
                  'xml_source_ref', 'scope', 'reporting_organisation',
                  'participating_organisation', 'policy_marker', 'sector',
                  'title_set', 'description_set', 'budget_set', 'location_set')
        many_fields = {
            'participating_organisation': 'participating_organisations',
            'policy_marker': 'policy_markers',
            'sector': 'sectors',
            'description_set': 'descriptions',
            'budget_set': 'budgets',
            'location_set': 'locations'
        }

    def __init__(self, force_publish=False, *args, **kwargs):
        super(ActivityDeserializer, self).__init__(*args, **kwargs)

        self.force_publish = force_publish

    def get_instance_or_none(self, data):
        iati_identifier = data['iati_identifier']
        if aims_models.Activity.objects.iatixml().filter(iati_identifier=iati_identifier).exists():
            aims_models.Activity.objects.iatixml().filter(iati_identifier=iati_identifier).delete()
        if aims_models.Activity.objects.filter(iati_identifier=iati_identifier).exists():
            return aims_models.Activity.objects.get(iati_identifier=iati_identifier)
        return None

    def convert_locations(self, data):
        # TODO: correctly convert locations when we can recognize the format
        data.pop('locations')
        data['locations'] = []
        if aims_models.Activity.objects.filter(iati_identifier=data['iati_identifier'], location__isnull=False)\
                .exclude(location__adm_country_adm1='')\
                .exists():
            for location in aims_models.Activity.objects.get(iati_identifier=data['iati_identifier']).location_set.all():
                data['locations'].append(OrderedDict({
                    'adm_country_adm1': location.adm_country_adm1,
                    'adm_country_adm2': location.adm_country_adm2,
                    'percentage': location.percentage,
                }))
        else:
            data['locations'].append(OrderedDict({
                'adm_country_adm1': 'Nation-wide',
            }))

    def convert_data(self, data):
        # Get the instance first so we can pass pk to many-related models where necessary
        self.instance = self.get_instance_or_none(data)

        data['reporting_organisation'] = data.pop('reporting_organisations')[0]
        self.convert_locations(data)
        for field_name in self.Meta.many_fields.keys():
            field_values = data.pop(self.Meta.many_fields[field_name])
            if self.instance is not None and self.force_publish:
                for field_value in field_values:
                    field_value['activity'] = self.instance
            data[field_name] = field_values

        change_key(data, 'title', 'title_set')

        if 'default_currency' in data and data['default_currency'] is not None:
            data['default_currency'] = data.pop('default_currency')['code']
        if 'activity_status' in data and data['activity_status'] is not None:
            data['activity_status'] = data.pop('activity_status')['code']
        if 'collaboration_type' in data and data['collaboration_type'] is not None:
            data['collaboration_type'] = data.pop('collaboration_type')['code']
        if 'default_flow_type' in data and data['default_flow_type'] is not None:
            data['default_flow_type'] = data.pop('default_flow_type')['code']
        if 'default_aid_type' in data and data['default_aid_type'] is not None:
            data['default_aid_type'] = data.pop('default_aid_type')['code']
        if 'default_finance_type' in data and data['default_finance_type'] is not None:
            data['default_finance_type'] = data.pop('default_finance_type')['code']
        if 'default_tied_status' in data and data['default_tied_status'] is not None:
            data['default_tied_status'] = data.pop('default_tied_status')['code']
        if 'scope' in data and data['scope'] is not None:
            data['scope'] = data.pop('scope')['code']
        # For now just create a nation-wide location

        activity_dates = data.pop('activity_dates')
        for activity_date in activity_dates:
            type_code = int(activity_date['type']['code'])
            if type_code == 1:
                data['start_planned'] = activity_date['iso_date']
            elif type_code == 2:
                data['start_actual'] = activity_date['iso_date']
            elif type_code == 3:
                data['end_planned'] = activity_date['iso_date']
            else:
                data['end_actual'] = activity_date['iso_date']

        cleaned_data = {}
        for field, value in data.items():
            if value is not None:
                cleaned_data[field] = value

        return cleaned_data

    def extract_many_related_data(self, validated_data):
        many_related_data = {}
        for field_name in self.Meta.many_fields.keys():
            if field_name in validated_data:
                many_related_data[field_name] = validated_data.pop(field_name)
            else:
                many_related_data[field_name] = None
        return many_related_data

    def merge_duplicate_sectors(self, sectors):
        sector_codes = [sector['sector'].code for sector in sectors]
        unique_codes = set(sector_codes)
        if len(sector_codes) == len(list(unique_codes)):
            # no duplicates, everything normal
            return sectors
        else:
            unique_sectors = []
            for code in unique_codes:
                sectors_for_code = [s for s in sectors if s['sector'].code == code]
                total_percentage = sum([s['percentage'] for s in sectors_for_code])
                sectors_for_code[0]['percentage'] = total_percentage
                unique_sectors.append(sectors_for_code[0])
            return unique_sectors

    def create(self, validated_data):
        ''' Create an aims.models.Activity model based on the validated_data. If the
        deserializer was initialized with force_publish set to True then we will publish the
        corresponding aims.models.Activity model.
        '''
        many_related_data = self.extract_many_related_data(validated_data)

        validated_data['reporting_organisation'] = self.fields['reporting_organisation'].instance

        title = validated_data.pop('title_set')

        activity = aims_models.Activity(**validated_data)
        activity.save()
        aims_activity = aims_models.Activity.objects.iatixml().get(iati_identifier=activity.iati_identifier)
        if self.force_publish:
            aims_activity.openly_status = StatusEnabledLocalData.OPENLY_STATUS_PUBLISHED
            aims_activity.save()

        if 'participating_organisation' in many_related_data:
            for participating_organisation in many_related_data['participating_organisation']:
                aims_models.ActivityParticipatingOrganisation(activity=activity,
                                                              **participating_organisation).save()
        if 'policy_marker' in many_related_data:
            for policy_marker in many_related_data['policy_marker']:
                aims_models.ActivityPolicyMarker(activity=activity, **policy_marker).save()
        if 'sector' in many_related_data:
            # combine sectors of the same code
            sectors = self.merge_duplicate_sectors(many_related_data['sector'])
            for sector in sectors:
                aims_models.ActivitySector(activity=activity, **sector).save()
        if 'description_set' in many_related_data:
            for description in many_related_data['description_set']:
                aims_models.Description(activity=activity, **description).save()
        if 'budget_set' in many_related_data:
            for budget in many_related_data['budget_set']:
                aims_models.Budget(activity=activity, **budget).save()
        if 'location_set' in many_related_data:
            for location in many_related_data['location_set']:
                aims_models.Location(activity=activity, **location).save()

        title['activity'] = activity
        aims_models.Title.objects.update_or_create(**title)

        return aims_activity

    def update(self, instance, validated_data):
        ''' Update the published instance if force_publish was set to True during initialization
        If not then we create a new aims.models.Activity model corresponding with
        openly_status iatixml.
        '''

        if not self.force_publish:
            return self.create(validated_data)
        many_related_data = self.extract_many_related_data(validated_data)

        reporting_org = validated_data.pop('reporting_organisation')
        validated_data['reporting_organisation'] = aims_models.Organisation.objects.update_or_create(**reporting_org)[0]

        title = validated_data.pop('title_set')
        title['activity'] = instance
        aims_models.Title.objects.update_or_create(**title)

        if 'participating_organisation' in many_related_data:
            for participating_organisation in many_related_data['participating_organisation']:
                obj, created = aims_models.ActivityParticipatingOrganisation.objects.update_or_create(
                    activity=instance,
                    organisation=participating_organisation.get('organisation', None),
                    role=participating_organisation.pop('role'),
                    name=(participating_organisation.get('name', None)
                          if 'organisation' not in participating_organisation
                          else participating_organisation['organisation'].name)
                )
        if 'policy_marker' in many_related_data:
            for policy_marker in many_related_data['policy_marker']:
                obj, created = (
                    aims_models.ActivityPolicyMarker.objects.update_or_create(
                        activity=instance,
                        policy_marker=policy_marker.get('policy_marker', None),
                        alt_policy_marker=policy_marker.get('alt_policy_marker', ''),
                        vocabulary=policy_marker.get('vocabulary', None),
                        policy_significance=policy_marker.get('policy_significance', None)
                    )
                )
        if 'sector' in many_related_data:
            for sector in many_related_data['sector']:
                obj, created = (
                    aims_models.ActivitySector.objects.update_or_create(
                        activity=instance,
                        sector=sector.get('sector', None),
                        vocabulary=sector.get('vocabulary', None),
                        percentage=sector.get('percentage', None)
                    )
                )
        if 'description_set' in many_related_data:
            for description in many_related_data['description_set']:
                obj, created = (
                    aims_models.Description.objects.update_or_create(
                        activity=instance,
                        description=description.pop('description'),
                        language=description.get('language', None),
                        type=description.get('type', None)
                    )
                )
        if 'budget_set' in many_related_data:
            for budget in many_related_data['budget_set']:
                obj, created = (
                    aims_models.Budget.objects.update_or_create(
                        activity=instance,
                        type=budget.get('type', None),
                        period_start=budget.get('period_start', ''),
                        period_end=budget.get('period_end', ''),
                        value=budget.get('value'),
                        value_date=budget.get('value_date', None),
                        currency=budget.get('currency', None)
                    )
                )
        if 'location_set' in many_related_data:
            for location in many_related_data['location_set']:
                obj, created = (
                    aims_models.Location.objects.update_or_create(
                        activity=instance,
                        adm_country_adm1=location.get('adm_country_adm1', ''),
                        adm_country_adm2=location.get('adm_country_adm2', ''),
                        percentage=location.get('percentage', None)
                    )
                )

        return instance


class DocumentCategorySerializer(FlexibleModelDeserializer):
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


class ActivityStatusSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.ActivityStatus
        fields = ('code', 'name')


class AidTypeCategorySerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.AidTypeCategory
        fields = ('code', 'name', 'desciption')


class AidTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.AidType
        fields = ('code', 'name', 'description', 'category')


class BudgetTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.BudgetType
        fields = ('code', 'name')


class CollaborationTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.CollaborationType
        fields = ('code', 'name', 'description')


class ConditionTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.ConditionType
        fields = ('code', 'name')


class CurrencySerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.Currency
        fields = ('code', 'name')


class DescriptionTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.DescriptionType
        fields = ('code', 'name', 'description')


class DisbursementChannelSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.DisbursementChannel
        fields = ('code', 'name')


class DocumentCategoryCategorySerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.DocumentCategoryCategory
        fields = ('code', 'name')


class FinanceTypeCategorySerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.FinanceTypeCategory
        fields = ('code', 'name', 'description')


class FinanceTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.FinanceType
        fields = ('code', 'name', 'category')


class FlowTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.FlowType
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


class PolicyMarkerSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.PolicyMarker
        fields = ('code', 'name')


class PolicySignificanceSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.PolicySignificance
        fields = ('code', 'name', 'description')


class PublisherTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.PublisherType
        fields = ('code', 'name')


class RelatedActivityTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.RelatedActivityType
        fields = ('code', 'name', 'description')


class ResultTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = iati_codelists.ResultType
        fields = ('code', 'name')


class SectorCategorySerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.SectorCategory
        fields = ('code', 'name', 'description')


class SectorSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.Sector
        fields = ('code', 'name', 'description', 'category')


class TiedStatusSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.TiedStatus
        fields = ('code', 'name', 'description')


class ValueTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.ValueType
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


class ContactTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.ContactType
        fields = ('code', 'name')


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


class TransactionTypeSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.TransactionType
        fields = ('code', 'name', 'description')


class IATISourceRefSerializer(FlexibleModelDeserializer):
    class Meta:
        model = aims_models.IATISourceRef
        fields = ('ref', 'title', 'url', 'date_created', 'date_updated', 'last_found_in_registry', 'activity_count', 'is_parsed')

    def get_instance_or_none(self, data):
        ref = data['ref']
        try:
            return aims_models.IATISourceRef.objects.get(ref=ref)
        except aims_models.IATISourceRef.DoesNotExist:
            return None

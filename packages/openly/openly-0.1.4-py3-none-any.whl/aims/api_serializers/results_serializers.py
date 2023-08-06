from aims.api_serializers.serializers import ForeignKeyChoiceSerializer
from rest_framework import serializers
from rest_framework import fields

from aims import models as aims_models
from iati_codelists import models as iati_codelists
from iati_vocabulary import models as iati_vocabulary

__all__ = [
    'IndicatorMeasureSerializer',
    'IndicatorVocabularySerializer',
    'NarrativeSerializer',
    'ResultDescriptionSerializer',
    'ResultIndicatorDescriptionSerializer',
    'ResultIndicatorPeriodActualCommentSerializer',
    'ResultIndicatorPeriodActualDimensionSerializer',
    'ResultIndicatorPeriodActualLocationSerializer',
    'ResultIndicatorPeriodSerializer',
    'ActualDimensionSetSerializer',
    'ResultIndicatorPeriodTargetCommentSerializer',
    'ResultIndicatorPeriodTargetDimensionSerializer',
    'ResultIndicatorPeriodTargetLocationSerializer',
    'ResultIndicatorReferenceSerializer',
    'ResultIndicatorSerializer',
    'ResultIndicatorTitleSerializer',
    'ResultIndicatorBaselineCommentSerializer',
    'ResultSerializer',
    'ResultTitleSerializer',
    'ResultTypeSerializer',
    'ResultIndicatorKeyProgressStatementSerializer'
]


class NarrativeSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)

    class Meta:
        model = aims_models.Narrative
        fields = ('id', 'language', 'content', 'related_object_id', 'related_content_type', 'activity')


class IndicatorMeasureSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)

    class Meta:
        model = iati_codelists.IndicatorMeasure
        fields = ('id', 'code', 'name', 'description')


class ResultIndicatorTitleSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultIndicatorTitle
        fields = ('id', 'result_indicator', 'narratives')


class ResultIndicatorKeyProgressStatementSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultIndicatorKeyProgressStatement
        fields = ('id', 'result_indicator', 'narratives')


class ResultIndicatorBaselineCommentSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultIndicatorBaselineComment
        fields = ('id', 'result_indicator', 'narratives')


class ResultTypeSerializer(ForeignKeyChoiceSerializer):

    class Meta:
        model = iati_codelists.ResultType
        fields = ('code', 'name')


class ResultTitleSerializer(serializers.ModelSerializer):
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultTitle
        fields = ('result', 'id', 'narratives')


class ResultDescriptionSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultDescription
        fields = ('id', 'result', 'narratives')
        validators = []


class ResultIndicatorDescriptionSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultIndicatorDescription
        fields = ('id', 'narratives', 'result_indicator')


class ResultIndicatorPeriodActualCommentSerializer(serializers.ModelSerializer):
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultIndicatorPeriodActualComment
        fields = ('id', 'narratives')


class ResultIndicatorPeriodTargetCommentSerializer(serializers.ModelSerializer):
    narratives = NarrativeSerializer(many=True, read_only=True)

    class Meta:
        model = aims_models.ResultIndicatorPeriodTargetComment
        fields = ('id', 'narratives')


class ResultIndicatorPeriodActualDimensionSerializer(serializers.ModelSerializer):

    class Meta:
        model = aims_models.ResultIndicatorPeriodActualDimension
        fields = ('result_indicator_period', 'id', 'name', 'value')


class ResultIndicatorPeriodActualLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = aims_models.ResultIndicatorPeriodActualLocation
        fields = ('id', 'location')


class ResultIndicatorPeriodTargetLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = aims_models.ResultIndicatorPeriodTargetLocation
        fields = ('id', 'location')


class ResultIndicatorPeriodTargetDimensionSerializer(serializers.ModelSerializer):

    class Meta:
        model = aims_models.ResultIndicatorPeriodTargetDimension
        fields = ('id', 'name', 'value')


class ResultIndicatorReferenceSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)

    class Meta:
        model = aims_models.ResultIndicatorReference
        fields = ('id', 'code', 'result_indicator', 'vocabulary', 'vocabulary_uri')


class ActualDimensionSetSerializer(serializers.ModelSerializer):

    resultindicatorperiodactualdimension_set = ResultIndicatorPeriodActualDimensionSerializer(many=True, required=False)

    def create(self, validated_data):
        raise NotImplementedError('Invalid method - ResultIndicatorPeriod needs to be defined first')

    def update(self, instance, validated_data):
        set_field = self.Meta.set_field
        model_set = getattr(instance, set_field)
        model_set.all().delete()
        [model_set.create(**d) for d in validated_data[set_field]]
        return instance

    class Meta:
        model = aims_models.ResultIndicatorPeriod
        fields = ('id', 'resultindicatorperiodactualdimension_set')
        set_field = 'resultindicatorperiodactualdimension_set'


class ResultIndicatorPeriodSerializer(serializers.ModelSerializer):
    resultindicatorperiodactualdimension_set = ResultIndicatorPeriodActualDimensionSerializer(many=True, required=False, read_only=True)
    resultindicatorperiodactuallocation_set = ResultIndicatorPeriodActualLocationSerializer(many=True, required=False, read_only=True)
    resultindicatorperiodtargetdimension_set = ResultIndicatorPeriodTargetDimensionSerializer(many=True, required=False, read_only=True)
    resultindicatorperiodtargetlocation_set = ResultIndicatorPeriodTargetLocationSerializer(many=True, required=False, read_only=True)
    resultindicatorperiodactualcomment = ResultIndicatorPeriodActualCommentSerializer(read_only=True)
    resultindicatorperiodtargetcomment = ResultIndicatorPeriodTargetCommentSerializer(read_only=True)

    target = fields.FloatField(required=False, allow_null=True)
    actual = fields.FloatField(required=False, allow_null=True)

    period_start = fields.DateField(required=False, allow_null=True)
    period_end = fields.DateField(required=False, allow_null=True)

    class Meta:
        model = aims_models.ResultIndicatorPeriod
        fields = (
            'id',
            'result_indicator',
            'period_start',
            'period_end',
            'target',
            'actual',
            'resultindicatorperiodactualdimension_set',
            'resultindicatorperiodtargetdimension_set',
            'resultindicatorperiodactuallocation_set',
            'resultindicatorperiodtargetlocation_set',
            'resultindicatorperiodactualcomment',
            'resultindicatorperiodtargetcomment'
        )


class ResultIndicatorTypeSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)

    class Meta:
        model = aims_models.ResultIndicatorType
        fields = ('id', 'result_indicator', 'display', 'sector', 'target')


class ResultIndicatorSerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)
    activity = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()

    def get_activity(self, object):
        return object.result.activity_id

    def get_organisation(self, object):
        return object.result.activity.reporting_organisation_id

    class Meta:
        model = aims_models.ResultIndicator
        fields = (
            'id',
            'result',
            'activity',
            'organisation',
            'measure',
            'ascending',
            'baseline_year',
            'baseline_value',
            'last_updated',
        )


class IndicatorVocabularySerializer(serializers.ModelSerializer):
    id = fields.IntegerField(allow_null=True, required=False)

    class Meta:
        model = iati_vocabulary.IndicatorVocabulary
        fields = ('code', 'name', 'description', 'url')


class ResultSerializer(serializers.ModelSerializer):
    '''
    For best results you'll ALWAYS want to prefetch_related some fields
    In fact, don't use this except for single instances
    '''
    type = ResultTypeSerializer()
    id = fields.IntegerField(allow_null=True, required=False)
    resulttitle = ResultTitleSerializer(required=False, read_only=True)
    resultdescription = ResultDescriptionSerializer(required=False, read_only=True)
    resultindicator_set = ResultIndicatorSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = aims_models.Result
        fields = (
            # Regular fields on the Result
            'activity',
            'aggregation_status', 'id', 'type',
            # "Special" fields which are actually properties
            'title', 'description',
            # Nested Serializers
            'resulttitle', 'resultdescription', 'resultindicator_set'
        )


class LegacyResultSerializer(serializers.ModelSerializer):
    '''
    Mohinga style results in phd style models
    '''
    title = fields.CharField(allow_null=True, allow_blank=True, required=False)
    description = fields.CharField(allow_null=True, allow_blank=True, required=False)

    def create(self, attrs):
        title = attrs.pop('title')
        description = attrs.pop('description')
        instance = super(LegacyResultSerializer, self).create(attrs)
        instance.title = title
        instance.description = description
        instance.save()
        return instance

    class Meta:
        model = aims_models.Result
        fields = (
            # Regular fields on the Result
            'activity',
            'aggregation_status', 'id', 'type',
            # "Special" fields which are actually properties
            'title', 'description',
        )


class SimpleResultSerializer(serializers.ModelSerializer):
    type = ResultTypeSerializer()
    id = fields.IntegerField(allow_null=True, required=False)

    class Meta:
        model = aims_models.Result
        fields = (
            'activity',
            'aggregation_status', 'id', 'type',
        )

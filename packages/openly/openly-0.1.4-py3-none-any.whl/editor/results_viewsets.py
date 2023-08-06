import rest_framework
from aims.api_serializers import results_serializers as serializers
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from iati_codelists.models import IndicatorMeasure, ResultType
from iati_vocabulary.models import IndicatorVocabulary
from rest_framework import viewsets
from aims import models as aims
from aims.api_serializers.simplified_results import SimpleResultSerializer, SimpleResultIndicatorSerializer
from editor.viewsets import UUIDFieldViewset

import logging
logger = logging.getLogger(__name__)

__all__ = [
    'IndicatorMeasureViewSet',
    'IndicatorVocabularyViewSet',
    'NarrativeViewSet',
    'ResultDescriptionViewSet',
    'ResultIndicatorDescriptionViewSet',
    'ResultIndicatorPeriodActualCommentViewSet',
    'ResultIndicatorPeriodActualDimensionViewSet',
    'ResultIndicatorPeriodActualLocationViewSet',
    'ResultIndicatorPeriodTargetCommentViewSet',
    'ResultIndicatorPeriodTargetDimensionViewSet',
    'ResultIndicatorPeriodTargetLocationViewSet',
    'ResultIndicatorPeriodViewSet',
    'ResultIndicatorReferenceViewSet',
    'ResultIndicatorTitleViewSet',
    'ResultIndicatorViewSet',
    'ResultTitleViewSet',
    'ResultTypeViewSet',
    'ResultViewSet',
    'LegacyResultViewSet',
    'ResultIndicatorTypeViewSet',
    'ResultIndicatorBaselineCommentViewSet',
    'ResultIndicatorKeyProgressStatementViewSet',
    'ActualDimensionSetViewSet',
    'SimpleResultViewSet',
    'SimpleResultIndicatorViewSet',
]


class ActualDimensionSetViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActualDimensionSetSerializer
    queryset = aims.ResultIndicatorPeriod.objects.all()


class ResultIndicatorTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorTypeSerializer
    queryset = aims.ResultIndicatorType.objects.all()


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultSerializer
    queryset = aims.Result.objects.all()


class LegacyResultViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LegacyResultSerializer
    queryset = aims.Result.objects.all()


class ResultTitleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultTitleSerializer
    queryset = aims.ResultTitle.objects.all()


class ResultIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorSerializer
    queryset = aims.ResultIndicator.objects.all()


class ResultIndicatorTitleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorTitleSerializer
    queryset = aims.ResultIndicatorTitle.objects.all()


class ResultIndicatorKeyProgressStatementViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorKeyProgressStatementSerializer
    queryset = aims.ResultIndicatorKeyProgressStatement.objects.all()


class ResultIndicatorDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorDescriptionSerializer
    queryset = aims.ResultIndicatorDescription.objects.all()


class IndicatorVocabularyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IndicatorVocabularySerializer
    queryset = IndicatorVocabulary.objects.all()


class NarrativeViewSet(viewsets.ModelViewSet):
    """
    Overrides "save" and "update" to use a "model" rather than django_content_type_id, if provided

    When this Narrative is being created, if an intermediate object should be created first (for instance
    a through model such as ResultTitle) then pass no 'related_object_id' and instead pass 'related_object_data'
    to get_or_create the object
    """
    serializer_class = serializers.NarrativeSerializer
    queryset = aims.Narrative.objects.all()

    def _indicator_update(self, response):
        if hasattr(response.data.serializer.instance.related_object, 'result_indicator'):
            indicator = response.data.serializer.instance.related_object.result_indicator
            indicator.last_updated = now()
            indicator.save()
        return response

    def create(self, request, *args, **kwargs):

        if 'model' in request.data:
            request.data['related_content_type'] = ContentType.objects.get(model=request.data.pop('model')).pk

        if 'related_object_id' not in request.data:
            content_type_id = self.request.data['related_content_type']
            related_object_data = self.request.data.pop('related_object_data')

            model = ContentType.objects.get(pk=content_type_id).model_class()
            instance, _ = model.objects.get_or_create(**related_object_data)

            self.request.data['related_object_id'] = instance.pk

        response = super(NarrativeViewSet, self).create(request, *args, **kwargs)
        self._indicator_update(response)
        return response

    def update(self, request, *args, **kwargs):
        if 'model' in request.data:
            request.data['related_content_type'] = ContentType.objects.get(model=request.data.pop('model')).pk
        response = super(NarrativeViewSet, self).update(request, *args, **kwargs)
        self._indicator_update(response)
        return response


class ResultDescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultDescriptionSerializer
    queryset = aims.ResultDescription.objects.all()


class IndicatorMeasureViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IndicatorMeasureSerializer
    queryset = IndicatorMeasure.objects.all()


class ResultIndicatorPeriodActualCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodActualCommentSerializer
    queryset = aims.ResultIndicatorPeriodActualComment.objects.all()


class ResultIndicatorPeriodActualDimensionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodActualDimensionSerializer
    queryset = aims.ResultIndicatorPeriodActualDimension.objects.all()


class ResultIndicatorPeriodActualLocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodActualLocationSerializer
    queryset = aims.ResultIndicatorPeriodActualLocation.objects.all()


class ResultIndicatorPeriodViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodSerializer
    queryset = aims.ResultIndicatorPeriod.objects.all()

    #  Functions to update the related resultindicator's last_updated
    #  when any priod is saved through the API
    def _indicator_update(self, response):
        indicator = response.data.serializer.instance.result_indicator
        indicator.last_updated = now()
        indicator.save()
        return response

    def create(self, request, *args, **kwargs):
        response = super(ResultIndicatorPeriodViewSet, self).create(request, *args, **kwargs)
        return self._indicator_update(response)

    def update(self, request, *args, **kwargs):
        response = super(ResultIndicatorPeriodViewSet, self).update(request, *args, **kwargs)
        return self._indicator_update(response)


class ResultIndicatorPeriodTargetCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodTargetCommentSerializer
    queryset = aims.ResultIndicatorPeriodTargetComment.objects.all()


class ResultIndicatorPeriodTargetDimensionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodTargetDimensionSerializer
    queryset = aims.ResultIndicatorPeriodTargetDimension.objects.all()


class ResultIndicatorPeriodTargetLocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorPeriodTargetLocationSerializer
    queryset = aims.ResultIndicatorPeriodTargetLocation.objects.all()


class ResultIndicatorReferenceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorReferenceSerializer
    queryset = aims.ResultIndicatorReference.objects.all()


class ResultTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultTypeSerializer
    queryset = ResultType.objects.all()


class ResultIndicatorBaselineCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResultIndicatorBaselineCommentSerializer
    queryset = aims.ResultIndicatorBaselineComment.objects.all()


class LoggerModelViewSet(viewsets.ModelViewSet):

    """
    This class creates an ActivityLogmessage instance
    on create, update, and delete.
    The class which inherits from this must add the
    following two functions:

    _create_id
    _object_activity_id

    This class adds one private function to create log messages

    __log

    This class calls `__log(...)` when `create`, `update`, and `delete` methods
    are called
    """

    def _create_id(self, response: rest_framework.response.Response) -> str:
        """
        Given a 201 "created" find the activity ID to create a log message for
        When update or destory is called you can use 'get_object', but this does not work
        from a create call. You have to parse the 'response' to get the correct activity ID
        """
        try:
            return response.data['id']  # type: ignore
        except Exception as E:
            raise NotImplementedError('Should be overridden by subclass') from E

    def _object_activity_id(self):
        """
        From an "update" or "delete" call, obtain the id from the object
        For example when a "ResultViewSet" receives a call to update, the "update" returns a Result object.
        The activity id is the activity_id property
        >>> return self.get_object().activity_id
        """
        raise NotImplementedError('Should be overridden by subclass')

    def __log(self, activity_id):
        try:
            aims.ActivityLogmessage.from_editor_request(self.request, activity=activity_id)
        except Exception as E:
            logger.error(F"Failed to write a log message: {E}")

    def create(self, *args, **kwargs):
        """
        Overrides the general "create" call to add a log message
        """
        response = super().create(*args, **kwargs)
        self.__log(self._create_id(response))
        return response

    def update(self, *args, **kwargs):
        """
        Override to create a log message
        """
        self.__log(self._object_activity_id())
        return super().update(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        """
        Override to create a log message
        """
        self.__log(self._object_activity_id())
        return super().destroy(*args, **kwargs)


class SimpleResultViewSet(UUIDFieldViewset):
    lookup_field = "uuid"
    serializer_class = SimpleResultSerializer
    queryset = aims.Result.objects.all()

    def _create_id(self, response) -> str:
        acts = aims.Activity.objects.all_openly_statuses()
        result_uuid = response.data.get('uuid')
        return acts.get(results__result_uuid=result_uuid).id


class SimpleResultIndicatorViewSet(UUIDFieldViewset):
    lookup_field = "uuid"
    serializer_class = SimpleResultIndicatorSerializer
    queryset = aims.SimpleResultIndicator.objects.annotate(result_uuid=F('result__uuid'))

    def _create_id(self, response) -> str:
        acts = aims.Activity.objects.all_openly_statuses()
        resultindicator_uuid = response.data.get('uuid')
        return acts.get(results__resultindicator__uuid=resultindicator_uuid).id

    def get_activity_id(self):
        return self.get_object().result.activity_id

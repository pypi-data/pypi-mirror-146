from typing import Optional
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from sentry_sdk.api import capture_exception
from aims import models as aims
import django
from django.conf import settings

from aims.api_serializers import serializers
from aims.api_serializers.editor import BudgetQuarterSerializer, TransactionSerializer, ContactSerializer, ActivityNestedTagSerializer
from .permissions import ActivityPermission
from rest_framework.permissions import IsAuthenticated

from rest_framework.request import Request
from aims.models import ActivityLogmessage

import logging
logger = logging.getLogger(__name__)

__all__ = [
    'BudgetViewSet',
    'TransactionViewSet',
    'ContactViewSet',
    'ContactUUIDViewSet',
    'ResourceTypeViewSet',
    'ActivityTagViewSet',
    'UUIDFieldViewset',
]


class ActivityLogMessageFailed(Exception):
    pass


class UUIDFieldViewset(viewsets.ModelViewSet):

    def make_activity_log(self):

        def get_activity() -> Optional[aims.Activity]:
            """
            Different ways to fetch an "activity" from a request
            Depending on the type of model and how it relates to an "activity".
            """
            activity = None
            if hasattr(self, "activity_id"):
                activity = aims.Activity.objects.all_openly_statuses().get(pk=getattr(self, "activity_id"))
            elif callable(getattr(self, "get_activity_id", None)):
                activity = aims.Activity.objects.all_openly_statuses().get(pk=getattr(self, "get_activity_id")())
            elif callable(getattr(self, 'get_object', None)) and hasattr(self.get_object(), "activity_id"):
                activity = aims.Activity.objects.all_openly_statuses().get(pk=self.get_object().activity_id)
            else:
                raise ActivityLogMessageFailed("Could not determine the source activity for request for logging purposes")

            return activity

        try:
            activity = get_activity()
            try:
                log = ActivityLogmessage.from_editor_request(self.request, activity=activity)
                logger.info(log)
            except Exception as E:
                raise ActivityLogMessageFailed("Could not create a log message") from E
        except ActivityLogMessageFailed as E:
            if settings.DEBUG or settings.TEST:
                raise
            capture_exception(E)

    def create(self, *args, **kwargs):
        raise NotImplementedError("URL should have end in a UUID")

    def update(self, request: Request, *args, **kwargs):
        # When a 404 is encountered this object does not exists yet. Redirect to
        # the "create" view. Adds our UUID to the request data, It
        # won't be collected from the URL.
        request.data[self.lookup_field] = request.resolver_match.kwargs[self.lookup_field]
        try:
            current_instance = self.get_object()
        except (django.core.exceptions.ObjectDoesNotExist, django.http.response.Http404):
            current_instance = None

        instance = super().update(request, *args, **kwargs) if current_instance else super().create(request, *args, **kwargs)
        self.make_activity_log()
        return instance

    def destroy(self, *args, **kwargs):
        self.make_activity_log()
        return super().destroy(*args, **kwargs)

    def get_queryset(self):
        """
        Optionally restricts the returned expenditures to a given activity,
        by filtering against a `activity` query parameter in the URL.
        """
        queryset = self.serializer_class.Meta.model.objects.all()
        activity = self.request.query_params.get("activity", None)
        if activity is not None:
            queryset = queryset.filter(activity_id=activity)
        return queryset


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetQuarterSerializer
    queryset = BudgetQuarterSerializer.Meta.model.objects.all()
    renderer_classes = (JSONRenderer, )
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post'])
    def by_activity(self, request, *args, **kwargs):
        """
        This handles a POSTed list of budget instances
        Examples: GET en/editor/api/editor-api-budget/by_activity/?activity=MM-FERD-ID28

        """
        if (request._request.method == 'POST'):
            """
            If the request includes a GET param with activity PK, we will replace ALL of the budgets
            for this activity. Otherwise we'll get an error
            """
            default_currency_id = 'USD'
            activity_id = self.request.query_params.get('activity', None)
            if not activity_id or not isinstance(request.data, list):
                raise AssertionError('This POST view expects a set of data like [{value: 100, quarter:20201}] and an activity_id GET param')
            self.queryset.filter(activity_id=activity_id).delete()
            for data in request.data:
                data.pop('id', None)
                data['activity_id'] = activity_id
                data['currency_id'] = aims.Activity.objects.with_drafts().get(pk=activity_id).default_currency_id or default_currency_id
                serializer = self.get_serializer(self.serializer_class.Meta.model(), data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

            queryset = self.queryset.filter(activity_id=activity_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Must have an activity ID
        queryset = self.queryset
        activity = self.request.query_params.get('activity')
        if activity is not None:
            queryset = queryset.filter(activity_id=activity)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = TransactionSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = ContactSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, *args, **kwargs):
        aims.ActivityLogmessage.from_editor_request(self.request, activity=self.request.data["activity"])
        return super().create(*args, **kwargs)

    def update(self, *args, **kwargs):
        aims.ActivityLogmessage.from_editor_request(self.request, activity=self.request.data["activity"])
        return super().update(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        aims.ActivityLogmessage.from_editor_request(self.request, activity=self.get_object().activity_id)
        return super().destroy(*args, **kwargs)


class ContactUUIDViewSet(ContactViewSet, UUIDFieldViewset):
    lookup_field = 'uuid'

    def get_activity_id(self):
        return self.get_object().activity.pk

    def _create_id(self, response):
        return response.data['uuid']


class ResourceTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ResourceTypeSerializer
    queryset = serializers.ResourceTypeSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]


class ActivityTagViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityNestedTagSerializer
    queryset = ActivityNestedTagSerializer.Meta.model.objects.all_openly_statuses()
    permission_classes = [ActivityPermission]

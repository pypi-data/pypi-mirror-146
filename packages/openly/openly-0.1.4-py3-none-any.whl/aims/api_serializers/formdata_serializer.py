import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class FormDataModelViewSet(ModelViewSet):
    """
    A viewset which overrides ModelViewSet to provide "update" and "create" views which
    are compatible with HTML5's FormData specification
    This simply overrides the serializer's data retrieval to get "_data" from the request rather than each individual key
    """

    def get_data(self, request):
        if '_data' in request.data:
            return json.loads(request.data['_data'])
        else:
            return request.data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_data(request))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.get_data(request), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AlwaysListViewSet(FormDataModelViewSet):
    """
    Wraps the returned serialize of a single object to return a list of all of the objects belonging to
    the updated objects' activity if 'activity' is provided in the GET string
    Always returns the whole queryset after create, update or delete requests
    """

    def serialize_list_wrapper(self, response, status_code=None):
        # This function would normally be overridden by subclass
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status_code or response.status_code)

    def create(self, request, *args, **kwargs):
        return self.serialize_list_wrapper(response=super(AlwaysListViewSet, self).create(request, *args, **kwargs))

    def destroy(self, request, *args, **kwargs):
        return self.serialize_list_wrapper(response=super(AlwaysListViewSet, self).destroy(request, *args, **kwargs), status_code=200)

    def update(self, request, *args, **kwargs):
        return self.serialize_list_wrapper(response=super(AlwaysListViewSet, self).update(request, *args, **kwargs))

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs and request.method == 'GET':  # Return one object only
            return super().retrieve(request, *args, **kwargs)
        return self.serialize_list_wrapper(response=super(AlwaysListViewSet, self).retrieve(request, *args, **kwargs))

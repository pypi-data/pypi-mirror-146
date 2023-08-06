from django.conf.urls import url
from django.urls import re_path, path, include
from django.views.decorators.http import etag
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers
from .routers import router, results_router

from . import views


js_info_dict = {
    'packages': ('editor',),
}

urlpatterns = [
    url(r'^activity-manager/(?P<org_id>[^\/\&\|\?]+)/$', views.OrganisationActivityManager.as_view(), name="activity_manager"),
    url(r'^activity/choose-organisation/$', views.ChooseOrganisation.as_view(), name='choose_activity_organisation'),
    url(r'^activity/(?P<organisation_id>[^\/\&\|\?]+)/new/$', views.CreateActivity.as_view(), name='create_activity'),
    url(r'^activity/archive/(?P<pk>[\w-]+)/$',
        views.ArchiveActivity.as_view(), name='archive_activity'),
    url(r'^activity/(?P<pk>[\w-]+)/$',
        views.EditActivity.as_view(), name='edit_activity'),
    url(r'^activity_iati/(?P<pk>[\w-]+)/$',
        views.IatiActivity.as_view(), name='iati_activity'),
    url(r'^activity/import/(?P<pk>[\w-]+)/$',
        views.ImportActivityToLocal.as_view(), name='import_activity_to_local'),
    url(r'^activity/(?P<org_id>[^\/\&\|\?]+)/import/$',
        views.ImportActivityAll.as_view(), name='import_activity_all'),
    url(r'^activity/compare/(?P<left>[\w-]+)/(?P<right>[\w-]+)/$',
        views.CompareActivities.as_view(), name='compare'),
    url(r'^activity/replace/(?P<local>[\w-]+)/(?P<remote>[\w-]+)/$',
        views.ReplaceLocalWithIATI.as_view(), name='replace'),
    url(r'^activity/restore/(?P<archived>[\w-]+)/(?P<local>[\w-]+)/$',
        views.RestoreArchived.as_view(), name='restore'),
    url(r'^activity/(?P<pk>[\w-]+)/update/$',
        views.ActivityViewSet.as_view({'put': 'partial_update'}), name='activity_update_general'),
    url(r'^activities/', views.ActivityViewSet.as_view({'get': 'list'}), name='organisation_activities'),

    # views used for endorsements
    url(r'^activity/(?P<activity_pk>[\w-]+)/endorsement/(?P<org_pk>[^\/\&\|\?]+)/$', views.Endorsement.as_view(), name='endorsement'),
    url(r'^activity/(?P<activity_pk>[\w-]+)/log/$', etag(views.ActivityLog.etag_function)(views.ActivityLog.as_view()), name='activitylog'),
    url(r'^activity/(?P<activity_pk>[\w-]+)/publish-errors/$', views.get_activity_publish_errors, name='publish_errors'),
    url(r'^review/(?P<organisation_pk>[^\/\&\|\?]+)/$', views.ActivitiesForReview.as_view(), name='activities_for_review'),
    url(r'^session/$', views.session_params, name='session_params'),

    path('activity/api/', include(router().urls), name='api'),
    path('activity/results-api/', include(results_router().urls)),

    # For offline POST caching we want to use the activity prefix in the URL
    # Note that the (?:[\/\w-]+) below is a "non-capturing" regex: it will pass on
    # to the correct view but this is no longer accessible after match
    # This means these are equivalent:
    #   /en/editor/activity/api/editor-api-budget/
    #   /en/editor/activity/fuzzzywuzzyfoobar/api/editor-api-budget/
    # To get this along with `reverse` and `{% url %}` working correctly
    # we repeat the API with first a non capturing group (for correct viewset)
    # and a named group.
    # Note the order is important
    re_path(r'activity/(?:[\w-]*\/{0,1})api/', include(router().urls), name='api'),
    re_path(r'activity/(?:[\w-]*\/{0,1})results-api/', include(results_router().urls)),

    # Repeat the above, this time with a named group
    # This allows reversing the URL like so:
    #   >>> reverse('editor-api-budget-list', kwargs={'activity_id': 'foo'})
    #   >>> '/en/editor/activity/foo/api/editor-api-budget/'
    path('activity/<str:activity_id>/api/', include(router().urls), name='api'),
    path('activity/<str:activity_id>/results-api/', include(results_router().urls)),
]

activity_attributes_router = routers.SimpleRouter()
activity_attributes_router.register('activitycompletion', views.ActivityCompletionViewSet, basename='activitycompletion')
activity_attributes_router.register('activitybudgets', views.ActivityBudgetsViewSet, basename='activitybudgets')
activity_attributes_router.register('activitycontacts', views.ActivityContactsViewSet, basename='activitycontacts')
activity_attributes_router.register('activitytransactions', views.ActivityTransactionsViewSet, basename='activitytransactions')
activity_attributes_router.register('documents', views.DocumentsViewset, basename='documents')
urlpatterns += activity_attributes_router.urls

api_endpoints = (
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=['editor']),
        name='editor-javascript-catalog'),
)
urlpatterns += api_endpoints

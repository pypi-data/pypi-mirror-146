from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sync/(?P<activity_id>[^\&\|\?]+)?$', views.OipaSyncActivities.as_view(), name="oipa_sync_activities"),
    url(r'^activity/(?P<iati_identifier>[^\&\|\?]+)?$', views.OipaActivity.as_view(), name="oipa_activity"),
    url(r'^activity_search/$', views.OipaActivity.as_view(), name="oipa_activity_by_iati_identifier"),
    url(r'^link/activity/update$', views.OipaActivityLinkUpdate.as_view(), name="oipa_activity_link_update"),
    url(r'^link/activity/clear$', views.OipaActivityLinkClear.as_view(), name="oipa_activity_link_clear"),
    url(r'^link/activity/delete$', views.OipaActivityLinkDelete.as_view(), name="oipa_activity_link_delete"),
    url(r'^link/iati/update$', views.IatiIdentifierUpdate.as_view(), name="iati_identifier_update"),
]

from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from .views import ActivityProfileView, ActivityViewSet


urlpatterns = [
    url(r'^activity/(?P<activity_id>[^/]+)/$', ActivityProfileView.as_view(),
        name='activity_profile'),
    url(r'^activity_profile/jsi18n/$', JavaScriptCatalog.as_view(), name='activity_profile-javascript-catalog'),
    # endpoint used by Project Bank when retrieving data from Mohinga
    url(r'^activity/(?P<pk>[^/]+)/data$', ActivityViewSet.as_view({'get': 'retrieve'}), name='activity_profile_data'),
]

api_endpoints = (
    url(r'^activity_profile/jsi18n/$', JavaScriptCatalog.as_view(), name='activity_profile-javascript-catalog'),
)

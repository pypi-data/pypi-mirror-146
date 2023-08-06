from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^location/$",
        views.AidByLocation.as_view(), name='aid_by_location'),
    url(r"^location/(?P<state>[\w\.-]+)$",
        views.AidByLocation.as_view(), name='aid_by_location'),
    url(r"^commitment_by_location/(?P<area_id>[\w\.-]+)$",
        views.CommitmentByLocation.as_view(), name='commitment_by_location'),
    url(r"^ministry/$",
        views.AidByMinistry.as_view(), name='aid_by_ministry'),
    url(r"^ministry/(?P<ministry>[\w-]+)$",
        views.AidByMinistry.as_view(), name='aid_by_ministry'),
    url(r"^donor/$",
        views.AidByDonor.as_view(), name='aid_by_donor'),
    url(r"^donor/(?P<donor>[\w %-]+)$",
        views.AidByDonor.as_view(), name='aid_by_donor'),
    url(r"^sector/$",
        views.AidBySector.as_view(), name='aid_by_sector'),
    url(r"^sector/(?P<category>[\w-]+)$",
        views.AidBySector.as_view(), name='aid_by_sector'),
    url(r"^sector/(?P<category>[\w-]+)/(?P<sector>[\w-]+)$",
        views.AidBySector.as_view(), name='aid_by_sector'),
    url(r"^summary/$",
        views.AidBySummary.as_view(), name='aid_by_summary'),
    url(r"^geo/$",
        views.GeoJson.as_view(), name='aid_geojson'),
    url(r"^geo/(?P<state>[\w\.-]+)$",
        views.GeoJson.as_view(), name='aid_geojson'),

    url(r"^welcome/$", views.WelcomeJS.as_view(), name='welcomejs'),
    url(r"^query/$", views.QueryBuilder.as_view(), name='query'),
    url(r"^query/data$", views.QueryBuilderData.as_view(), name='querydata'),
]

if 'haystack' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^search/', views.SearchView.as_view(), name='search'))

from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.i18n import JavaScriptCatalog
from rest_framework.routers import SimpleRouter

from profiles_v2 import views


router = SimpleRouter()
router.register(r'organisation_people', views.PersonViewSet, basename='organisation_people')

# We may want to override the organisation profile in openly instances but we will always
# want the API endpoints for updating the organisation's contact info and people. The URL
# definitions are separated so instances can select the portions they need correctly.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^update/', login_required(views.UpdateGenericView.as_view()), name='update'),
    url(r'^upload/', login_required(views.UploadGenericView.as_view()), name='upload'),
    url(r'^organisation/(?P<iati_identifier>[^/]+)/', views.OrganisationProfileView.as_view(), name='organisation_profile'),
    url(r'^organisation_activities/(?P<organisation>[^/]+).json', views.OrganisationActivities.as_view(), name='organisation_activities'),
    url(r'^organisation_contact_info/(?P<profile__organisation__pk>[^/]+)/', views.RetrieveUpdateOrganisationContactInfoView.as_view(), name='organisation_contact_info'),
    url(r'^organisation_profile/jsi18n/$', JavaScriptCatalog.as_view(packages=('profiles_v2',)), name='profiles_v2-javascript-catalog'),
    url(r'^organisation_profile/(?P<organisation__pk>[^/]+)/', views.RetrieveUpdateOrganisationProfileView.as_view(), name='edit_organisation_profile'),
    # Below URLs are from Profiles v1
    url(r'^commitment_by_category/(?P<iati_identifier>[^/]+)/$', views.DonorCommitmentByCategory.as_view(), name='commitment_by_category'),
    url(r'^activities_status_values/(?P<iati_identifier>[^/]+)/$', views.DonorActivityStatusValues.as_view(), name='activities_status_values'),
    url(r'^transactions_by_year/(?P<iati_identifier>[^/]+)/$', views.DonorTransactionsByYear.as_view(), name='transactions_by_year'),
    url(r'^activities/(?P<iati_identifier>[^/]+)/$', views.DonorActivities.as_view(), name='donor_activities'),
    url(r'^donor/(?P<iati_identifier>[^/]+)/',
        views.OrganisationProfileView.as_view(), name='donor_profile'),
    url(r'^fetch-person/(?P<pk>[\d]+)/?$',
        login_required(views.PersonView.as_view()), name='fetch_person'),
    url(r'^create-person/$',
        login_required(views.CreatePerson.as_view()), name='create_person'),
    url(r'^update-person/(?P<pk>[\d]+)/$',
        login_required(views.UpdatePerson.as_view()), name='update_person'),
    url(r'^delete-person/(?P<pk>[\d]+)/?$',
        login_required(views.DeletePerson.as_view()), name='delete_person'),
    url(r'^fetch-contact/(?P<pk>[\d]+)/?$',
        login_required(views.ContactView.as_view()), name='fetch_contact'),
    url(r'^save-contact/(?P<pk>[\d]+)/$',
        login_required(views.SaveContact.as_view()), name='save_contact'),
    url(r'^fetch-data/(?P<pk>[\d]+)/?$',
        login_required(views.PersonData.as_view()), name='person_data'),
    url(r'^reorder-people/$', login_required(views.ReorderPeople.as_view()), name='reorder_people'),
    url(r'^riot/(?P<tags>[^/]+)/$', views.RiotTagView.as_view(), name='riot'),
]


api_endpoints = (
    url(r'^', include(router.urls)),
    url(r'^update/', login_required(views.UpdateGenericView.as_view()), name='update'),
    url(r'^upload/', login_required(views.UploadGenericView.as_view()), name='upload'),
    url(r'^organisation_contact_info/(?P<profile__organisation__pk>[^/]+)/', views.RetrieveUpdateOrganisationContactInfoView.as_view(), name='organisation_contact_info'),
    url(r'^organisation_profile/jsi18n/$', JavaScriptCatalog.as_view(packages=('profiles_v2',)), name='profiles_v2-javascript-catalog'),
    url(r'^organisation_profile/(?P<organisation__pk>[^/]+)/', views.RetrieveUpdateOrganisationProfileView.as_view(), name='edit_organisation_profile'),
)

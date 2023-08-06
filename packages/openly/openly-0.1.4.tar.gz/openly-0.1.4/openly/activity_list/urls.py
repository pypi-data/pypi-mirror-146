from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.ActivitiesPageView.as_view(), name='activities_page'),
]

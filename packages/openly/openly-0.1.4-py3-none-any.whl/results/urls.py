from django.conf.urls import url

from results import views

urlpatterns = [
    url(r'^', views.ResultsView.as_view(), name='results_page'),
]

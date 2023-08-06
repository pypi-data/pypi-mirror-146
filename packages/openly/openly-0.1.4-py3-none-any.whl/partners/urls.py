from django.conf.urls import url

from partners import views

urlpatterns = [
    url(r'^', views.PartnersPageView.as_view(), name='partners_page'),
]

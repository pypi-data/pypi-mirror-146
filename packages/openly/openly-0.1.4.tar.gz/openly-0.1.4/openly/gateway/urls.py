from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.Index.as_view(), name='index'),
    url(r"^home/$", views.HomeRedirectView.as_view(), name='home'),
]

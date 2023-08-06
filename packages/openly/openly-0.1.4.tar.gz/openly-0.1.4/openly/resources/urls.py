from django.conf.urls import url
from resources.views import ResourcesView

urlpatterns = [url(r"^$", ResourcesView.as_view(), name="resources_view")]

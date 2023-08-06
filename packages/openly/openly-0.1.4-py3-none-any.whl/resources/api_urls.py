from django.conf.urls import url

from .views import ResourceJsonView

urlpatterns = (url(r"^main.json$", ResourceJsonView.as_view(), name="resources_json"),)

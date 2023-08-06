from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(
        r"^$", login_required(views.QualityAssuranceIndex.as_view()), name="dataquality"
    ),
    url(
        r"^(?P<category>[\w-]+)/(?P<nickname>[\w-]+)/$",
        login_required(views.QualityAssuranceTest.as_view()),
        name="dataquality_test",
    ),
    url(
        r"^(?P<category>[\w-]+)/(?P<nickname>[\w-]+)/json/$",
        login_required(views.QualityAssuranceObjects.as_view()),
        name="dataquality_test_json",
    ),
    url(
        r"^transaction/(?P<nickname>[\w-]+)/excel/$",
        login_required(views.TransactionQualityAssuranceExport.as_view()),
        name="transaction_dataquality_test_excel",
    ),
    # Most dataquality exports are a list of activities
    url(
        r"^(?P<category>[\w-]+)/(?P<nickname>[\w-]+)/excel/$",
        login_required(views.QualityAssuranceExport.as_view()),
        name="dataquality_test_excel",
    ),

]

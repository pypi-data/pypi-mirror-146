from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from aims.utils import render

from aims import models as aims
from aims.api_serializers import results_serializers
from iati_codelists import models as iati_codelists


class ResultsView(TemplateView):

    template_name = "results/results.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ResultsView, self).get_context_data(*args, **kwargs)

        context['page_title'] = _('Results Page')
        context['data'] = render(dict(
            results=self.results,
            choices=self.model_choices
        ))

        return context

    @property
    def model_choices(self):
        choices = {}

        choices['sectors'] = [(obj) for key, obj in aims.ResultIndicatorType.sector_choices]
        choices['sectors'].insert(0, _('All'))

        choices['indicatormeasure'] = [(obj.code, obj.name) for obj in iati_codelists.IndicatorMeasure.objects.all()]

        return choices

    @property
    def results(self):
        ''' Results and related objects for this Activity '''
        return dict(
            result=results_serializers.SimpleResultSerializer(aims.Result.objects.prefetch_related('type').all(), many=True).data,
            resulttitle=results_serializers.ResultTitleSerializer(aims.ResultTitle.objects.all(), many=True).data,
            resultdescription=results_serializers.ResultDescriptionSerializer(aims.ResultDescription.objects.all(), many=True).data,
            resultindicator=results_serializers.ResultIndicatorSerializer(aims.ResultIndicator.objects.all().prefetch_related('result'), many=True).data,
            resultindicatortitle=results_serializers.ResultIndicatorTitleSerializer(aims.ResultIndicatorTitle.objects.all(), many=True).data,
            resultindicatordescription=results_serializers.ResultIndicatorDescriptionSerializer(aims.ResultIndicatorDescription.objects.all(), many=True).data,
            contenttype=ContentType.objects.filter(app_label='aims').values('id', 'app_label', 'model'),
            resulttype=iati_codelists.ResultType.objects.values('code', 'name', 'description'),
            resultindicatorperiod=results_serializers.ResultIndicatorPeriodSerializer(aims.ResultIndicatorPeriod.objects.all(), many=True).data,
            resultindicatortype=results_serializers.ResultIndicatorTypeSerializer(aims.ResultIndicatorType.objects.all(), many=True).data,
            resultindicatorperiodactualdimension=results_serializers.ResultIndicatorPeriodActualDimensionSerializer(aims.ResultIndicatorPeriodActualDimension.objects.all(), many=True).data,

            # This is the field we use for a "shorter" narrative title
            resultindicatorbaselinecomment=results_serializers.ResultIndicatorBaselineCommentSerializer(aims.ResultIndicatorBaselineComment.objects.all(), many=True).data,
            resultindicatorkeyprogressstatement=results_serializers.ResultIndicatorKeyProgressStatementSerializer(aims.ResultIndicatorKeyProgressStatement.objects.all(), many=True).data,
        )

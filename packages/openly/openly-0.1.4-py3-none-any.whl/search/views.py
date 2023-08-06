from el_pagination.views import AjaxListView
from haystack.views import SearchView as HaystackSearchView
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from .forms import ActivitySearchForm
from aims.models import Activity, Partner


class SearchResultsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            partner_results = SearchQuerySet().models(Partner).filter(content__contains=q)[:4]
            activity_results = SearchQuerySet().models(Activity).filter(content__contains=q)

        if self.request.user.is_superuser:
            activity_results = activity_results[:4]
        elif self.request.user.is_authenticated and self.request.user.organisation:
            activity_results = activity_results.filter(Q(openly_status='published') | Q(openly_status='draft', reporting_organisation_id=self.request.user.organisation.code))[:4]
        else:
            activity_results = activity_results.filter(openly_status='published')[:4]
        serialized_results = {
            'partners': [{'html': sr.rendered_nav} for sr in partner_results],
            'activities': [{'html': sr.rendered_nav} for sr in activity_results]
        }
        return Response(serialized_results)


class SearchView(AjaxListView, HaystackSearchView):
    template_name = 'search/search.html'
    page_template = 'search/search_results.html'
    form_class = ActivitySearchForm
    load_all = False
    searchqueryset = None

    def get_queryset(self):
        self.form = self.build_form()
        self.query = self.get_query()
        return self.get_results()

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['page_template'] = self.page_template
        context['form'] = self.form

        if self.request.is_ajax():
            self.template_name = self.page_template

        q = self.request.GET['q'] or None
        activity_results = SearchQuerySet().models(Activity).filter(content__contains=q)

        if self.request.user.is_superuser:
            pass
        elif self.request.user.is_authenticated and self.request.user.organisation:
            activity_results = activity_results.filter(Q(openly_status='published') | Q(openly_status='draft', reporting_organisation_id=self.request.user.organisation.code))
        else:
            activity_results = activity_results.filter(openly_status='published')

        context['activities'] = activity_results
        context['partners'] = SearchQuerySet().models(Partner).filter(content__contains=q)

        return context

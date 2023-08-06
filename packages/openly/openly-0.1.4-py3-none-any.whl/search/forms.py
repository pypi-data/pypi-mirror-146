from django import forms
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet, SQ

from aims import models


class ActivitySearchForm(SearchForm):
    q = forms.CharField(label="", max_length=128, required=False)

    reporting_organisation = forms.ModelChoiceField(models.Organisation.objects, required=False)
    sector = forms.ModelChoiceField(models.Sector.objects, required=False)
    participating_organisation = forms.ModelChoiceField(models.Organisation.objects, required=False)

    def __init__(self, *args, **kwargs):
        super(ActivitySearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].widget.attrs['class'] = 'form-control'
        self.fields['reporting_organisation'].widget.attrs['class'] = 'form-control'
        self.fields['sector'].widget.attrs['class'] = 'form-control'
        self.fields['participating_organisation'].widget.attrs['class'] = 'form-control'

    def search(self):
        search_queryset = SearchQuerySet()
        if not self.is_valid():
            return self.no_query_found()

        q = self.cleaned_data['q']
        search_queryset = search_queryset.filter(SQ(name=q) | SQ(sectors=q) | SQ(locations=q) | SQ(people=q) | SQ(title=q))

        # Check to see if an organisation was chosen
        if self.cleaned_data['reporting_organisation']:
            search_queryset = search_queryset.filter(reporting_organisation=self.cleaned_data['reporting_organisation'])

        # Check to see if a sector was chosen.
        if self.cleaned_data['sector']:
            search_queryset = search_queryset.filter(sectors__contains=self.cleaned_data['sector'].code)

        if self.cleaned_data['participating_organisation']:
            search_queryset = search_queryset.filter(participating_organisations__contains=self.cleaned_data['participating_organisation'].name)

        return search_queryset.order_by('-django_ct')

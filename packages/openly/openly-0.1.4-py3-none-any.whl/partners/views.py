from collections import defaultdict

from django.conf import settings
from django.urls import reverse
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from aims.utils import render
from aims.models import Area, Partner, Sector, ActivityStatus
from aims import models as aims


class PartnersPageView(TemplateView):
    """ View for the partners page, a directory for all program partners with
    basic filtering on the partners and their associated activities.

    The view's main responsibility is embedding all Partners and
    their associated activities in the context. Additionally all relevant
    static data structures are serialized and embedded (e.g. languages,
    sectors, etc...). The View additionally provides a focus_area method that
    can be overridden when the program is only active in a subtree of the
    overall Area tree.
    """
    template_name = "partners/partners.html"

    def get_context_data(self, **kwargs):
        """ Find all program Partner models, serialize them and their
        associated activities, and embed in the context. Additionally include
        the available languages, activity statuses, areas, and sectors.
        """
        context = super(PartnersPageView, self).get_context_data(**kwargs)
        context['page_title'] = _('Partners Page')

        def partners():
            """
            Serialize all Partner models
            Includdes lists of activity sector and location for clientside filtering
            """

            partners = Partner.objects.all()
            profiles = aims.Organisation.profile.get_queryset().filter(organisation__in=partners)
            profile_logo = dict((a.organisation_id, a.logo.url) for a in profiles if a.logo)
            activity_participating = aims.ActivityParticipatingOrganisation.objects.filter(organisation__in=partners)

            values = ('pk', 'name', 'code', 'abbreviation', 'type__code')
            models = dict((partner.pop('pk'), partner) for partner in partners.values(*values).order_by('name'))

            activity_sectors = defaultdict(list)
            for category_pk, activity_pk in aims.SectorCategory.objects.values_list('pk', 'sector__activitysector__activity__pk'):
                if category_pk not in activity_sectors[activity_pk]:
                    activity_sectors[activity_pk].append(category_pk)

            activity_locations = defaultdict(list)
            for activity_pk, adm_code in aims.Location.objects.values_list('activity__pk', 'adm_code'):
                activity_locations[activity_pk].append(adm_code)

            activity_list = defaultdict(list)
            for activity_pk, status_code in aims.Activity.objects.values_list('pk', 'activity_status__code'):
                activity_list[activity_pk] = {
                    'status': status_code,
                    'sectors': activity_sectors.get(activity_pk, []),
                    'locations': activity_locations.get(activity_pk, [])
                }

            organisation_activity_sets = defaultdict(list)

            for opk, apk in activity_participating.values_list('organisation_id', 'activity_id'):
                organisation_activity_sets[opk].append(apk)
            for apk, opk in aims.Activity.objects.values_list('pk', 'reporting_organisation'):
                organisation_activity_sets[opk].append(apk)

            for opk, activity_ids in organisation_activity_sets.items():
                if opk not in models:
                    continue
                for apk in set(activity_ids):
                    if 'activities' not in models[opk]:
                        models[opk]['activities'] = []
                    if apk in activity_list:
                        models[opk]['activities'].append(activity_list.get(apk))

            for opk, model in models.items():
                model['type'] = model.pop('type__code')
                model['abbrev'] = model.pop('abbreviation')
                model['logo'] = profile_logo.get(opk, '')
                model['profile'] = reverse('organisation_profile', args=[opk])
                if 'activities' not in model:
                    model['activities'] = []

            return models.values()

        context['partners'] = render(partners())
        context['languages'] = render({k: {'language_name': v} for (k, v) in settings.LANGUAGES})
        context['choices'] = render(self.model_choices)

        return context

    @property
    def model_choices(self):
        """ Returns a dictionary choice name -> choices. Each choice is a tuple (db_value, human_value).
        """
        choices = {}
        choice_name_to_queryset = {'activity_status': ActivityStatus.objects.filter(code__lte=3),
                                   'sectors': Sector.objects.filter(code=F('category_id')),
                                   }

        for choice_name, queryset in choice_name_to_queryset.items():
            choices[choice_name] = [{'value': obj.code, 'name': obj.name} for obj in queryset]

        choices['locations'] = self.location_choices

        return choices

    @property
    def location_choices(self):
        """ Returns the choices list for locations. The first element of each
        tuple is a primary key.
        """
        area_choices = []
        full_area_names_by_pk = {}

        for area in self.focus_area():
            # TODO: it may be better to store this as a property on Area models
            # The full name is a '|' delimited list of an area and its
            # ancestors area type and name
            full_name = area.kind.name + ' ' + area.name
            if area.parent_id is None or area.parent_id not in full_area_names_by_pk:
                full_area_names_by_pk[area.pk] = full_name
            else:
                parent_full_name = full_area_names_by_pk[area.parent_id]
                full_area_names_by_pk[area.pk] = "{} | {}".format(parent_full_name,
                                                                  full_name)
            serialized_area = {
                'full_name': full_area_names_by_pk[area.pk],
                'descendants': tuple(area.get_descendants().values_list('pk', flat=True)) + (area.pk,),
                'name': area.name,
                'kind': area.kind.name,
                'code': area.pk,
            }
            area_choices.append(serialized_area)

        return area_choices

    def focus_area(self):
        """ Returns a queryset of the Area objects to be embedded in the
        Partner's page context listed in tree order. Defaults to all areas but
        child classes should override if necessary.
        """
        try:
            return Area.objects.first().get_root().get_family()
        except Exception:
            return []

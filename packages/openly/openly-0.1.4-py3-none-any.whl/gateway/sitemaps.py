from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from aims import models as aims


class ActivityProfileSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5  # default
    i18n = True

    def items(self):
        return aims.Activity.objects.all()

    def location(self, activity):
        return reverse('activity_profile', kwargs={'activity_id': activity.id})


class OrganisationProfileSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5  # default
    i18n = True

    def items(self):
        return aims.Organisation.objects.all()

    def location(self, organisation):
        return reverse('donor_profile', kwargs={'iati_identifier': organisation.code})


# sitemaps dict should be used by a sitemap.xml view
# ex: url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap')
sitemaps = {
    'activity_profiles': ActivityProfileSitemap,
    'organisation_profiles': OrganisationProfileSitemap
}

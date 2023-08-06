from modeltranslation.translator import register, TranslationOptions
from .models import OrganisationProfile


@register(OrganisationProfile)
class OrganisationProfileTranslationOptions(TranslationOptions):
    fields = ('background',)

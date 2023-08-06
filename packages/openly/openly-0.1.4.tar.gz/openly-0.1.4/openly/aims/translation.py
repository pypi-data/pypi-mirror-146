from modeltranslation.translator import register, TranslationOptions

from .models import Organisation, Sector, SectorCategory, AidType, AidTypeCategory, ActivityStatus, ResourceType, Tag, TagVocabulary, DocumentCategory


@register(AidType)
class AidTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(AidTypeCategory)
class AidTypeCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Sector)
class SectorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(SectorCategory)
class SectorCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Organisation)
class OrganisationTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ActivityStatus)
class ActivityStatusTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ResourceType)
class ResourceTypeTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(TagVocabulary)
class TagVocabularyTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(DocumentCategory)
class DocumentCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

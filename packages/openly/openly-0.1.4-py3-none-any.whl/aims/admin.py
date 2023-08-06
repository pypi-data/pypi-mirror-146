from urllib.parse import quote_plus
from datetime import date

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from . import models as aims


admin.site.site_header = '{} administration'.format(settings.OPENLY_SITE_CONTEXT['site_name'])
admin.site.site_title = '{} administration'.format(settings.OPENLY_SITE_CONTEXT['site_name'])


class UserOrganisationInline(admin.StackedInline):
    model = aims.UserOrganisation
    verbose_name_plural = 'Organisations'
    filter_horizontal = ('organisations',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'organisations':
            kwargs['queryset'] = aims.Organisation.objects.exclude(name='').order_by('name')
        return super(UserOrganisationInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class ReadOnlyPasswordWidget(forms.Widget):
    def render(self, name, value, attrs, renderer=None):
        return format_html('<p>{}</p>'.format(_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        )))


class ReadOnlyPasswordField(forms.Field):
    widget = ReadOnlyPasswordWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super(ReadOnlyPasswordField, self).__init__(*args, **kwargs)


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordField(
        label=_('Password'),
    )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        return self.initial['password']


class UserAdmin(DefaultUserAdmin):
    form = UserChangeForm
    inlines = (UserOrganisationInline, )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Admin access'), {'fields': ('is_active', 'is_staff', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('username', 'email', 'name', 'title', 'group_names', 'date_joined', 'is_staff')
    list_filter = ('is_staff',)

    def get_fieldsets(self, request, user=None):
        if user is None:
            return DefaultUserAdmin.add_fieldsets
        if request.user.is_superuser:
            # show extra fields to the superuser, like the permissions and groups
            return DefaultUserAdmin.fieldsets
        return self.fieldsets

    def title(self, instance):
        if instance.userorganisation:
            return instance.userorganisation.title

    def get_inline_instances(self, request, user=None):
        if user is None:
            return []
        return super(UserAdmin, self).get_inline_instances(request, user)

    def get_actions(self, request):
        return []

    def get_queryset(self, request):
        ''' exclude superusers from the admin user list if the user is not a superuser '''
        queryset = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return queryset.exclude(is_superuser=True)
        return queryset.prefetch_related('groups').select_related('userorganisation')

    def name(self, user):
        return user.get_full_name()

    def group_names(self, user):
        return ', '.join([g.name for g in user.groups.all()])

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ActivityAdmin(admin.ModelAdmin):
    model = aims.Activity
    list_display = ('id', 'title', 'activity_status', 'reporting_partner', 'date_modified_')
    fields = (('id', 'iati_identifier', 'date_modified'), 'title', 'reporting_organisation',
              ('activity_status', 'openly_status'),
              ('start_planned', 'start_actual', 'end_planned', 'end_actual'),
              ('link_to_editor', 'link_to_profile'))
    readonly_fields = ('id', 'iati_identifier', 'title', 'activity_status', 'openly_status', 'date_modified',
                       'start_planned', 'start_actual', 'end_planned', 'end_actual',
                       'link_to_editor', 'link_to_profile')
    search_fields = ['id', 'iati_identifier']

    def get_queryset(self, request):
        return aims.Activity.objects.all_openly_statuses()\
                                    .prefetch_related('title_set')\
                                    .select_related('reporting_organisation', 'activity_status') \
                                    .annotate(date_modified_null=Coalesce('date_modified', Value(date(year=1900, month=1, day=1))))

    def link_to_editor(self, activity):
        if activity.openly_status == aims.Activity.OPENLY_STATUS_IATIXML:
            return 'Cannot be edited'
        return format_html('<a href="{}" target="_blank">Editor for {}</a>',
                           reverse('edit_activity', kwargs={'pk': activity.pk}),
                           activity.pk
                           )

    def link_to_profile(self, activity):
        # check openly_status because profile only allows Activity.objects.with_drafts()
        if activity.openly_status in [aims.StatusEnabledLocalData.OPENLY_STATUS_IATIXML,
                                      aims.StatusEnabledLocalData.OPENLY_STATUS_ARCHIVED]:
            return 'Activity is {}, no profile available'.format(activity.openly_status)
        return format_html('<a href="{}" target="_blank">Profile for {}</a>',
                           reverse('activity_profile', kwargs={'activity_id': activity.id}),
                           activity.pk
                           )

    def date_modified_(self, activity):
        return activity.date_modified

    date_modified_.admin_order_field = 'date_modified_null'

    def get_actions(self, request):
        """ Remove the delete action from the admin list. """
        actions = super(ActivityAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'reporting_organisation':
            kwargs['queryset'] = aims.Organisation.objects.order_by('name')
        return super(ActivityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def lookup_allowed(self, lookup, value):
        return True


admin.site.register(aims.Activity, ActivityAdmin)


class OrganisationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganisationAdminForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = True

    def clean_code(self):
        code = self.cleaned_data['code']
        if code != quote_plus(code):
            raise forms.ValidationError('Code cannot contain the following characters: ; / ? : @ & = + $ , space')
        return code


class OrganisationAdmin(admin.ModelAdmin):
    model = aims.Organisation
    form = OrganisationAdminForm
    search_fields = ('code', 'abbreviation', 'name')
    list_display = ('code', 'abbreviation', 'name', 'type', 'reporting_activities', 'participating_activities',
                    'providing_transactions', 'receiving_transactions')

    def get_queryset(self, request):
        return aims.Organisation.objects.select_related('type')\
                                        .prefetch_related('transaction_providing_organisation',
                                                          'transaction_receiving_organisation',
                                                          'activity_reporting_organisation',
                                                          'activityparticipatingorganisation_set',)

    def get_actions(self, request):
        """ Remove the delete action from the admin list. """
        actions = super(OrganisationAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_fields(self, request, organisation=None):
        """ Hide the activities and transactions counts from the "Add organisation" form. """
        fields = ['code', 'abbreviation', 'type', 'name', 'parent']
        if organisation is not None:
            fields.extend(['reporting_activities', 'participating_activities', 'providing_transactions', 'receiving_transactions'])
        return fields

    def get_readonly_fields(self, request, organisation=None):
        """ Allow specifying the code of a new org, but not editing the code of an existing org. """
        if organisation is None:
            return ('reporting_activities', 'providing_transactions', 'receiving_transactions', 'participating_activities')
        return ('code', 'reporting_activities', 'providing_transactions', 'receiving_transactions', 'participating_activities')

    def reporting_activities(self, organisation):
        return format_html('<a href="{}" target="_blank">{}</a>',
                           reverse('admin:aims_activity_changelist') + '?reporting_organisation_id={}'.format(organisation.pk),
                           organisation.reporting_activities_count
                           )

    def participating_activities(self, organisation):
        return format_html('<a href="{}" target="_blank">{}</a>',
                           reverse('admin:aims_activity_changelist') + '?participating_organisation={}'.format(organisation.pk),
                           organisation.participating_activities_count
                           )

    def providing_transactions(self, organisation):
        return format_html('<a href="{}" target="_blank">{}</a>',
                           reverse('admin:aims_activity_changelist') + '?transaction__provider_organisation_id={}'.format(organisation.pk),
                           organisation.activities_with_providing_transactions_count
                           )

    def receiving_transactions(self, organisation):
        return format_html('<a href="{}" target="_blank">{}</a>',
                           reverse('admin:aims_activity_changelist') + '?transaction__receiver_organisation_id={}'.format(organisation.pk),
                           organisation.activities_with_receiving_transactions_count
                           )

    def has_delete_permission(self, request, organisation=None):
        return organisation is not None and \
            organisation.reporting_activities_count == 0 and \
            organisation.participating_activities_count == 0 and \
            organisation.activities_with_providing_transactions_count == 0 and \
            organisation.activities_with_receiving_transactions_count == 0


class TranslatedOrganisationAdmin(OrganisationAdmin, TranslationAdmin):
    pass


admin.site.register(aims.Organisation, TranslatedOrganisationAdmin)


class AidTypeAdmin(TranslationAdmin):
    pass


class AidTypeCategoryAdmin(TranslationAdmin):
    pass


admin.site.register(aims.AidType, AidTypeAdmin)
admin.site.register(aims.AidTypeCategory, AidTypeCategoryAdmin)


class SectorAdmin(TranslationAdmin):
    pass


admin.site.register(aims.Sector, SectorAdmin)


class SectorCategoryAdmin(TranslationAdmin):
    pass


admin.site.register(aims.SectorCategory, SectorCategoryAdmin)


class MonthYearListFilter(admin.SimpleListFilter):
    """
    Filter to a given month and year
    """
    title = "time"
    parameter_name = "time"
    default_value = None

    def lookups(self, request, model_admin):
        return set([(s.strftime('%Y-%m'), s.strftime('%B %Y')) for s in sorted(aims.CurrencyExchangeRate.objects.values_list('date', flat=True).distinct())])

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        year, month = self.value().split('-')
        queryset = queryset.filter(date__year=year, date__month=month)
        return queryset


class CurrencyListFilter(admin.SimpleListFilter):
    """
    Filter to any currency which is already utilised as a base_currency or currency
    """
    title = "currency"
    parameter_name = "currency"
    default_value = None

    def lookups(self, request, model_admin):
        return sorted(
            set(aims.CurrencyExchangeRate.objects.values_list('base_currency__code', 'base_currency__name').distinct()) |
            set(aims.CurrencyExchangeRate.objects.values_list('currency__code', 'currency__name').distinct())
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        queryset = queryset.filter(Q(base_currency=self.value()) | Q(currency=self.value()))
        return queryset


@admin.register(aims.CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    model = aims.CurrencyExchangeRate
    ordering = ('-date',)
    list_display = ('base_currency', 'currency', 'rate', 'date')
    add_form_template = 'aims/admin/change_form_exchange_rate.html'
    change_form_template = 'aims/admin/change_form_exchange_rate.html'
    list_filter = (CurrencyListFilter, MonthYearListFilter)

    class Media:
        js = ('js/jquery-1.10.2.js', 'select2/select2.min.js',)
        css = {'all': ['select2/select2-bootstrap.css', 'select2/select2.css']}


class ActivityStatusAdmin(TranslationAdmin):
    list_display = ('code', 'order', 'name',)
    ordering = ('order', 'code')
    fields = ('code', 'order', 'name')

    def get_readonly_fields(self, request, status=None):
        if status:
            return ('code',)
        else:
            return ()


class ResourceTypeAdmin(TranslationAdmin):
    pass


admin.site.register(aims.ActivityStatus, ActivityStatusAdmin)
admin.site.register(aims.ResourceType, ResourceTypeAdmin)


class TagVocabularyAdmin(TranslationAdmin):
    pass


class TagAdmin(TranslationAdmin):
    pass


@admin.register(aims.ActivityLogmessage)
class ActivityLogmessageAdmin(admin.ModelAdmin):
    list_display = [
        "activity",
        "body",
        "tstamp",
        "user",
        "organisation",
        "title",
        "message",
        "user_organisations",
        "activity",
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def title(self, object: aims.ActivityLogmessage):
        return object.title

    def message(self, object: aims.ActivityLogmessage):
        msg, params = object.message()
        return msg.format(**params)


admin.site.register(aims.TagVocabulary, TagVocabularyAdmin)
admin.site.register(aims.Tag, TagAdmin)
admin.site.register(aims.Location, admin.ModelAdmin)


class DocumentCategoryAdmin(TranslationAdmin):
    pass


admin.site.register(aims.DocumentCategory, DocumentCategoryAdmin)

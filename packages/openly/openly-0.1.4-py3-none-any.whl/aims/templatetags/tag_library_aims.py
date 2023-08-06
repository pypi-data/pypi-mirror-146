from django import template
from django.urls import reverse
from editor.permissions import user_is_admin_or_superuser

register = template.Library()


@register.filter
def create_actvity_url(user, page_organisation):
    if user_is_admin_or_superuser(user) or user.organisation_count > 1:
        return reverse('choose_activity_organisation')
    elif user.organisation:
        return reverse('create_activity', args=[user.organisation.code])
    return False

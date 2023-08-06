from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS

from aims import models as aims


def user_is_admin_or_superuser(user):
    if user.is_superuser:
        return True
    if user.is_anonymous:
        return False
    if user.organisations and user.organisations.filter(is_admin=True).exists():
        return True


class ActivityPermission(BasePermission):
    def has_permission(self, request, view):
        """ Permission for creating a new activity.

        * always allow superusers
        * users can only create activities for their organisation.
        """
        user = request.user
        if user_is_admin_or_superuser(user):
            return True
        if 'reporting_organisation' in request.data:
            org_code = request.data['reporting_organisation']['code']
            try:
                if org_code not in user.userorganisation.organisations.values_list('code', flat=True):
                    return False
            except aims.UserOrganisation.DoesNotExist:
                return False
        # the serializer will throw a validation error when there's no reporting organisation
        return True

    def has_object_permission(self, request, view, instance):
        """ Permission for updating an existing activity or related instance

        * always allow superusers
        * users can only update activities reported by their organisation.
        * when the model instance is not itself an 'Activity', try to use the model's 'activity' attr
        """
        user = request.user

        # When used for a "related" model, such as deleting a DocumentLink,
        # check that the related activity would allow this deletion
        activity = None
        if isinstance(instance, aims.Activity):
            activity = instance

        # When "activity" is optional, allow editing by all
        # TODO: do Organisation check too
        elif hasattr(instance, 'activity') and (getattr(instance, 'activity')) is None:
            return True
        elif isinstance(getattr(instance, 'activity', None), aims.Activity):
            activity = instance.activity
        else:
            raise TypeError('The model provided is not an activity - or, cannot work out its relationship')
        if user.is_anonymous:
            # Anonymous user never has UserOrganisation and throws an AttributeError
            # if we ask for it.
            return False
        if user_is_admin_or_superuser(user):
            return True
        try:
            user_organisation_codes = user.userorganisation.organisations.values_list('code', flat=True)
        except aims.UserOrganisation.DoesNotExist:
            return False
        if activity.reporting_organisation_id in user_organisation_codes:
            return True
        if getattr(settings, 'ENDORSEMENT_ENABLED', False):
            accountable_organisations_codes = [apo.organisation_id for apo in
                                               aims.OrganisationHelper.find_organisations_in_role(activity.participating_orgs, 'accountable')]
            if set(user_organisation_codes) & set(accountable_organisations_codes):
                return True
        return False


class ActivityPermissionWithView(ActivityPermission):
    """
    Adds read-only GET requests for anonymous user
    """
    def has_object_permission(self, request, view, instance):
        return (
            request.method in SAFE_METHODS or (
                not request.user.is_anonymous
                and super().has_object_permission(request, view, instance)
            )
        )

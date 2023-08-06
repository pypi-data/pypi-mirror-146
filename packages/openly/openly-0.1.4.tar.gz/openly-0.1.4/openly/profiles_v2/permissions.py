# pylint: disable=W0221
from rest_framework import permissions

from aims import models as aims


class OrganisationProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, profile):
        """ Permission for accessing an organisation's profile.

        * always allow safe (non-altering) requests
        * always allow superusers
        * users can only edit their organisation's profile
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user.is_superuser:
            return True

        try:
            if profile.organisation_id not in user.userorganisation.organisations.values_list('code', flat=True):
                # user is attached to a different organisation.
                return False
        except aims.UserOrganisation.DoesNotExist:
            # user is not attached to any organisations
            return False
        return True


class OrganisationContactInfoPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, contact_info):
        """ Permission for accessing an organisation's contact information.

        * always allow safe (non-altering) requests
        * always allow superusers
        * users can only edit their organisation's profile
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user.is_superuser:
            return True

        try:
            if contact_info.profile.organisation_id not in user.userorganisation.organisations.values_list('code', flat=True):
                # user is attached to a different organisation
                return False
        except aims.UserOrganisation.DoesNotExist:
            # user is not attached to any organisation
            return False
        return True


class PersonPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Permission for accessing the people (read/create) in an organisation's profile

        * always allow safe (non-altering) requests
        * always allow superusers
        * users can only add to their organisation
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user.is_superuser:
            return True

        if 'organisation_profile' in request.data:
            profile_id = int(request.data['organisation_profile'])
            try:
                if profile_id not in user.userorganisation.organisations.values_list('profile__id', flat=True):
                    # user is attached to a different organisation
                    return False
            except aims.UserOrganisation.DoesNotExist:
                # user is not attached to any organisation
                return False

        # the serializer will throw a validation error when there's no profile
        return True

    def has_object_permission(self, request, view, person):
        """ Permissions for updating/deleting an organisation's person

        * always allow superusers
        * users can only update/delete people in their organisation
        """
        user = request.user
        if request.user.is_superuser:
            return True

        try:
            if person.organisation_profile.pk not in user.userorganisation.organisations.values_list('profile__id', flat=True):
                # user is attached to a different organisation
                return False
        except aims.UserOrganisation.DoesNotExist:
            # user is not attached to any organisation
            return False

        return True

from collections import OrderedDict

from dateutil.parser import parse
from django.utils.translation import ugettext as _

from aims import models as aims


def functionally_unique_title(obj):
    ''' returns a human readable title which is functionally unique for any object
        example : Consider 2 activities a1 and a2
                    a1 has titles t11(lang=en, title=hello), t12(lang=tet, title=bondia)
                    a2 has titles t21(lang=en, title=helloworld), t22(lang=fra, title=bonjour)
                    title t11 and title t21 should be considered functionally identical - with a differing title
                    t12 is a title only a1 has, t22 is a title only a2 has
    '''
    if isinstance(obj, aims.Transaction):
        return "Transaction {type} from {org}".format(
            type=obj.transaction_type.name,
            org=obj.provider_organisation
        )
    if isinstance(obj, aims.Title):
        return "{language} {objtype}".format(
            language=obj.language.name if obj.language else _("Default"),
            objtype=_('Title')
        )
    if isinstance(obj, aims.Description):
        return "{language} {objtype}".format(
            language=obj.language.name if obj.language else _("Default"),
            objtype=_('Description') if obj.type_id == 1 else _('Objective')
        )
    if isinstance(obj, aims.ActivitySector):
        return "Sector {sector}".format(
            sector=obj.sector.name if obj.sector else obj.sector.alt_sector_name,
        )
    if isinstance(obj, aims.ActivityPolicyMarker):
        return "Policy Marker {policy}".format(
            policy=obj.policy_marker.name if obj.policy_marker else obj.policy_marker.alt_policy_marker,
        )
    if isinstance(obj, aims.ActivityParticipatingOrganisation):
        return "Participating Org : {role}".format(
            role=obj.role.name)
    if isinstance(obj, aims.Location):
        return "Location: {loc}".format(
            loc=obj.adm_country_adm1)
    if isinstance(obj, aims.Budget):
        return "{type} budget".format(
            type=obj.type.name)
    if isinstance(obj, aims.Result):
        return "{type} result".format(
            type=obj.type.name)
    if isinstance(obj, aims.ContactInfo):
        return "Contact {name}".format(
            name=obj.person_name if obj.person_name else "un-named")


def get_diff_data(obj):
    ''' returns a dict containing the humanly readable information from an iati object '''

    data = obj.__dict__.copy()
    remove_keys = ['_state', 'id', 'remote_data_id', 'activity_id', 'date_created', 'date_modified', 'openly_status', '_activity_cache', 'sector_id']
    if isinstance(obj, aims.Activity):
        remove_keys.append('activity_status_id')
        data['activity_status'] = obj.activity_status
        remove_keys.append('collaboration_type_id')
        data['collaboration_type'] = obj.collaboration_type

    for key in remove_keys:
        if key in data:
            del data[key]
    return data


def get_properties_diffs(obj1, obj2):
    ''' returns a set of diffs where values differ
        NOTE Assumes all keys are the same in both dicts
    '''
    diffs = {}
    dict1, dict2 = get_diff_data(obj1), get_diff_data(obj2)
    for key in iter(dict1):
        if not key.startswith('_') and dict1[key] != dict2[key]:
            diffs[key] = (dict1[key], dict2[key])

    return diffs


def get_linked_object_diffs(queryset_left, queryset_right):
    ''' return items not in both, or different
       NOTE Assumes objects are the same in both querysets
    '''
    diffs = {}

    list_right = list(queryset_right)

    # deal with left list
    for left in queryset_left:
        # look for match in list2 based on key_func
        right = None
        left_title = functionally_unique_title(left)
        for try_right in list_right:
            right_title = functionally_unique_title(try_right)
            if left_title == right_title:
                right = try_right
                break

        if right:
            # found match - add dict_diffs to diffs and remove right from list
            match_diffs = get_properties_diffs(left, right)
            if match_diffs:
                diffs[left_title] = {
                    'is_sub_diffs': 1,
                    'diffs': get_properties_diffs(left, right)
                }
            list_right.remove(right)
        else:
            # no match found add diff on whole object
            diffs[left_title] = (left, None)

    # deal with right list
    for right in list_right:
        right_title = functionally_unique_title(right)
        if right_title not in diffs:
            diffs[right_title] = (None, right)

    return diffs


def activity_differences(base, other):
    ''' compares two activities returning an iterable collection of differences '''

    diffs = OrderedDict()
    diffs.update(get_properties_diffs(base, other))
    diffs.update(
        get_linked_object_diffs(base.title_set.all(), other.title_set.all())
    )
    diffs.update(
        get_linked_object_diffs(base.description_set.filter(type_id=1), other.description_set.filter(type_id=1))
    )
    diffs.update(
        get_linked_object_diffs(base.description_set.filter(type_id=2), other.description_set.filter(type_id=2))
    )
    diffs.update(
        get_linked_object_diffs(base.sectors.all(), other.sectors.all())
    )
    diffs.update(
        get_linked_object_diffs(base.activitypolicymarker_set.all(), other.activitypolicymarker_set.all())
    )
    diffs.update(
        get_linked_object_diffs(base.participating_organisations.all(), other.participating_organisations.all())
    )
    diffs.update(
        get_linked_object_diffs(base.location_set.all(), other.location_set.all())
    )
    diffs.update(
        get_linked_object_diffs(base.transaction_set.all(), other.transaction_set.all())
    )
    diffs.update(
        get_linked_object_diffs(base.budget_set.all(), other.budget_set.all())
    )
    diffs.update(
        get_linked_object_diffs(base.results.all(), other.results.all())
    )
    diffs.update(
        get_linked_object_diffs(base.contactinfo_set.all(), other.contactinfo_set.all())
    )

    # convert string datetimes to datetimes
    if 'last_updated_datetime' in diffs:
        diffs['last_updated_datetime'] = [parse(value) for value in diffs['last_updated_datetime']]

    return diffs

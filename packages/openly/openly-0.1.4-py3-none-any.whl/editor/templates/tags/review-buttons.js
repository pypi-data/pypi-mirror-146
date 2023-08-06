/* {% load i18n %} */

var tag = this;
var change_activity_status_to;
var get_accountable_organisations_names;
var get_endorser_organisation;

tag.store = stores.reviewStore;
tag.can_publish = window.is_admin_or_superuser;
tag.is_admin_or_donor = (window.is_admin_or_superuser || window.user_organisation_code === stores.activityStore.activity.reporting_organisation.code);

tag.on('before-mount', function () { tag.endorser_organisation = get_endorser_organisation(); });
tag.on('update', function () { tag.endorser_organisation = get_endorser_organisation(); });

tag.show_modal = function (event) {
    tag.active_modal = tag.refs[event.currentTarget.getAttribute('target_modal')];
    tag.store.trigger('refresh_endorsers');

    if (event.currentTarget.getAttribute('check_publish_errors') === null) {
        // no need to check for publish errors, show the modal right away
        tag.active_modal.show();
    } else {
        tag.loading = true;
        tag.store.get_publish_errors(
        ).done(function () {
            tag.active_modal.show();
        }).always(function () {
            tag.loading = false;
            tag.update();
        });
    }
};

tag.change_status = function (event) {
    var target_status = event.currentTarget.getAttribute('target_status');
    event.preventDefault();
    tag.loading = true;

    tag.store.change_activity_status_to(target_status
    ).always(function () {
        tag.loading = false;
        tag.update();
    }).done(function () {
        tag.active_modal.hide();
    });
};

tag.toggle_endorsement = function () {
    var organisation = tag.endorser_organisation;

    if (tag.loading) { return; }
    tag.loading = true;

    tag.store.toggle_endorsement(organisation
    ).done(function () {
        tag.active_modal.hide();
    }).always(function () {
        tag.loading = false;
        tag.update();
    });
};

tag.store.on('endorsements_changed', tag.update);

get_endorser_organisation = function () {
    // if the current user belongs to one of the endorsers, return their organisation
    return _.find(tag.store.endorsers, function (org) { return org.code === window.user_organisation_code; });
};

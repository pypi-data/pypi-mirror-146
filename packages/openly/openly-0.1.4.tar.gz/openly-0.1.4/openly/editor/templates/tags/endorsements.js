var tag = this;
tag.store = tag.parent.store;
tag.can_endorse_on_behalf = window.is_admin_or_superuser;

tag.on('update', function () {
    tag.openly_status = stores.activityStore.activity.openly_status;
    tag.store.trigger('refresh_endorsers');
});

tag.store.on('review_cancelled', function () {
    tag.store.remove_stored_endorsements();
    tag.update();
});

tag.toggle_endorsement = function (event) {
    var organisation = event.item.organisation;

    if (tag.loading) { return; }
    tag.loading = true;

    tag.store.toggle_endorsement(organisation
    ).done(tag.update
    ).always(function () {
        tag.loading = false;
        tag.update();
    });
};

var tag = this;

tag.open_delete_modal = function () {
    $('#deleteActivityModal').modal('show');
};

tag.on('before-mount', function () {
    if (stores.reviewStore === undefined) {
        tag.can_delete = true;
        return;
    }
    // endorsers cannot delete an activity
    tag.can_delete = (window.is_admin_or_superuser || window.user_organisation_code === stores.activityStore.activity.reporting_organisation.code);
});

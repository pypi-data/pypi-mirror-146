/* global stores */

function updateDeleteButton(activity_id) {
    /* Hide the Delete button if the activity hasn't been created. */
    // Uses jQuery rather than Riot because the Delete button lives in gateway/**/base.html
    var delete_form;
    if (stores.activityStore.activity.id !== undefined) {
        delete_form = $('#deleteActivityForm');
        delete_form.prop('action', delete_form.prop('action').replace('replaceme', activity_id));
        $('#deleteActivity').show();
        $('.origin_indicator').show();
    } else {
        $('#deleteActivity').hide();
        $('.origin_indicator').hide();
    }
}

$(document).ready(function () {
    updateDeleteButton();
});

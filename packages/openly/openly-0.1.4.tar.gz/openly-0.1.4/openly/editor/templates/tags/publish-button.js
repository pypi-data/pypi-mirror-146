// {% load i18n %}
/* globals gettext stores, $ */
var tag = this;

var PUBLISH_SUCESS_MESSAGE = '{% blocktrans %}Successfully published the {{ activity_singular }}{% endblocktrans %}';
var DRAFT_SUCESS_MESSAGE = '{% blocktrans %}Successfully set the {{ activity_singular }} to draft{% endblocktrans %}';

tag.activity = stores.activityStore.activity;
tag.is_published = (tag.activity.openly_status === 'published');

tag.toggle_publish = function () {
    /* Sends a PUT request to the update_activity API with the new openly_status.
     * If there are publish errors, shows a popover that lists whast prevents the publishing.
     */
    var xhr;
    var data = { openly_status: tag.is_published ? 'draft' : 'published' };

    // toggle is_published now to animate the slider correctly
    tag.is_published = !tag.is_published;
    tag.update();

    xhr = $.ajax({
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        method: 'PUT',
        url: stores.activityStore.urls().update,
        headers: { 'X-CSRFTOKEN': '{{ csrf_token }}' }
    });

    xhr.done(function () {
        var message = tag.is_published ? PUBLISH_SUCESS_MESSAGE : DRAFT_SUCESS_MESSAGE;
        window.banner_message.show(message, gettext('success'));
        tag.update();
    });
    xhr.fail(function (error_response) {
        if (error_response.responseJSON){
            tag.show_error_popover(error_response.responseJSON.openly_status);
        }
        tag.is_published = !tag.is_published;
        tag.update();
    });
    xhr.always(function () {
        stores.activityStore.activity.openly_status = tag.is_published ? 'published' : 'draft'
        stores.activityStore.trigger('activity_status_changed');
    })
    return true;
};

tag.show_error_popover = (function () {
    // wrapped in a closure to only declare error_key_to_message once
    var error_key_to_message = {
        title: '{% blocktrans %}Set the {{ activity_singular }} Title{% endblocktrans %}',
        description: '{% blocktrans %}Set the {{ activity_singular }} Description{% endblocktrans %}',
        status: '{% blocktrans %}Set the {{ activity_singular }} Status{% endblocktrans %}',
        start_date: gettext('Set the Start Date'),
        sector: gettext('Add a sector'),
        any_sector: gettext('Add a sector'),
        location: gettext('Add a location'),
        commitment: gettext('Add a transaction of type Commitment'),
        end_date: gettext('Set the End Date'),
    };

    var show_error_popover = function (error_keys) {
        var popover_options;
        tag.error_messages = [];
        error_keys.forEach(function (error_key) {
            tag.error_messages.push(error_key_to_message[error_key]);
        });
        tag.update();
        popover_options = {
            title: gettext('Sorry, you cant publish just yet.'),
            placement: 'bottom',
            template: $('#publish_popover_template').html(),
            html: true
        };
        $('#publish-error-popover').popover(popover_options);
        $('#publish-error-popover').popover('show');
        $('.publish_popover_cancel').click(function () {
            $('#publish-error-popover').popover('destroy');
        });
    };
    return show_error_popover;
}());

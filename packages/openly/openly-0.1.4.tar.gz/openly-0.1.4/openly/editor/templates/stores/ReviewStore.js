
    /* commented for editor highlighting - content is required - django templates in translations for use in Javascript
     * {% load i18n %}
     *
     * {% blocktrans asvar publish_error_title %}Set the {{activity_singular}} Title{% endblocktrans %}
     * {% blocktrans asvar publish_error_description %}Set the {{activity_singular}} Description{% endblocktrans %}
     * {% blocktrans asvar publish_error_status %}Set the {{activity_singular}} Status{% endblocktrans %}
     * {% trans "Set the Planned or Actual Start Date" as publish_error_dates %}
     * {% trans "Set the Planned or Actual End Date" as publish_error_end_date %}
     * {% trans "Add a Sector" as publish_error_sector %}
     * {% trans "Add a Location" as publish_error_location %}
     * {% trans "Add a Transaction of type Commitment" as publish_error_transaction %}
     * {% trans "Error saving your comment, please try again" as message_save_error %}
     * {% blocktrans asvar message_review_submit %}{{activity_singular}} submitted for review{% endblocktrans %}
     * {% blocktrans asvar message_reset_draft %}{{activity_singular}} reset to draft{% endblocktrans %}
     * {% blocktrans asvar message_published %}{{activity_singular}} published{% endblocktrans %}
     * {% blocktrans asvar message_reset_review %}{{activity_singular}} reset to review{% endblocktrans %}
     * {% blocktrans asvar message_change_status_error %}Error changing the {{activity_singular}} status, please try again{% endblocktrans %}
    */
function ReviewStore(endorsements) {
    var store = this;
    var activity_log_url = '{% url "activitylog" activity_pk=activity.id %}';
    var refresh_logs;
    var possible_publish_errors;
    riot.observable(store);

    store.activity_logs = [];
    store.publish_errors = [];
    store.openly_status = stores.activityStore.activity.openly_status;
    store.endorsers = get_endorsers();

    possible_publish_errors = {
        title: '{{ publish_error_title|escape }}',
        description: '{{ publish_error_description|escape }}',
        status: '{{ publish_error_status|escape }}',
        start_date: '{{ publish_error_dates|escape }}',
        sector: '{{ publish_error_sector|escape }}',
        location: '{{ publish_error_location|escape }}',
        commitment: '{{ publish_error_transaction|escape }}',
        end_date: '{{publish_error_end_date|escape}}',
    };

    function get_endorsers() {
        var accountable_organisations = _(stores.activityStore.activity.participating_organisations).filter(function (organisation) {
            return (organisation.name && organisation.role.code === 'Accountable');
        }).value();
        return _.map(accountable_organisations, function (organisation) {
            return {
                code: organisation.organisation.code,
                name: organisation.name,
                endorsed: endorsements[organisation.organisation.code]
            };
        });
    }
    store.on('refresh_endorsers', function () { store.endorsers = get_endorsers(); });

    refresh_logs = function () {
        if (store.request_in_progress) { return; }
        store.request_in_progress = true;

        $.ajax({
            dataType: 'json',
            url: activity_log_url,
            beforeSend: function (xhr) { xhr.setRequestHeader('If-none-match', store.activity_logs_etag); }
        }).done(function (data, _, xhr) {
            if (xhr.status === 304) {
                store.trigger('activity_logs_updated');
                return;
            }
            store.activity_logs_etag = xhr.getResponseHeader('etag');
            if (data.activitylogmessages.length > store.activity_logs.length) {
                store.activity_logs = data.activitylogmessages;
                store.trigger('activity_logs_updated');
            }
        }).always(function () {
            store.request_in_progress = false;
        });
    };
    store.on('refresh_logs', refresh_logs);

    store.post_comment = function (comment_data) {
        var xhr = $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(comment_data),
            method: 'POST',
            url: activity_log_url,
            headers: { 'X-CSRFTOKEN': window.csrf_token }
        }).done(function (new_activity_log) {
            window.banner_message.hide('danger');
            store.activity_logs.unshift(new_activity_log);
            store.trigger('activity_logs_updated');
        }).fail(function () {
            window.banner_message.show('{{message_save_error|escape}}', 'danger');
        });
        return xhr;
    };

    store.get_publish_errors = function () {
        var xhr = $.ajax({
            method: 'GET',
            url: '{% url "publish_errors" activity_pk=activity.id %}'
        }).done(function (error_keys) {
            store.publish_errors = _(possible_publish_errors).pick(error_keys).values().value();
        });
        return xhr;
    };

    store.change_activity_status_to = function (status) {
        return $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({ openly_status: status }),
            method: 'PUT',
            url: stores.activityStore.urls().update,
            headers: { 'X-CSRFTOKEN': window.csrf_token }
        }).done(function (activity) {
            window.banner_message.hide('danger');
            if (store.openly_status === 'draft' && status === 'review') {
                window.banner_message.show('{{message_review_submit|escape}}', 'success');
            } else if (status === 'draft') {
                window.banner_message.show('{{message_reset_draft|escape}}', 'success');
                store.trigger('review_cancelled');  // used to hide existing endorsements
            } else if (status === 'published') {
                window.banner_message.show('{{message_published|escape}}', 'success');
            } else if (store.openly_status === 'published' && status === 'review') {
                window.banner_message.show('{{message_reset_review|escape}}', 'success');
            }
            stores.activityStore.activity.openly_status = activity.openly_status;
            store.openly_status = activity.openly_status;
            store.trigger('refresh_logs');  // a log has been created in the db for status change
            store.trigger('activity_status_changed');
        }).fail(function () {
            window.banner_message.show('{{message_change_status_error|escape}}', 'danger');
        });
    };

    store.toggle_endorsement = function (organisation) {
        var method = organisation.endorsed ? 'DELETE' : 'PUT';

        return $.ajax({
            method: method,
            url: '{% url "endorsement" activity_pk=activity.id org_pk="XXXX" %}'.replace('XXXX', organisation.code),
            headers: { 'X-CSRFTOKEN': '{{ csrf_token }}' }
        }).done(function () {
            store.trigger('refresh_logs');
            endorsements[organisation.code] = !organisation.endorsed;
            store.endorsers = get_endorsers();
            store.trigger('endorsements_changed');
        });
    };

    store.remove_stored_endorsements = function () {
        endorsements = {};
        store.trigger('refresh_endorsers');
    };
}

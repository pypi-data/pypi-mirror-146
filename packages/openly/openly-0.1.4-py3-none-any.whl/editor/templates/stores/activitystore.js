/**
 * The ActivityStore is a RiotControl store holding a single Activity object
 *
 * @class ActivityStore
 * @param source {Object} An object to use as the "source", usually a JSON array or object passed in by Django or loaded by AJAX: {id: "1", name: "my activity"}
 * @param choices {Object} Defines choices for fields where there may be a select field or similar
 * @constructor
 * @static load
 * @listens RiotRestMixin.trigger:create_element
 * @listens RiotRestMixin.trigger:delete_element
 * @listens RiotRestMixin.trigger:toggle_delete_element
 * @listens RiotRestMixin.trigger:restore_deleted_element
 * @listens RiotRestMixin.trigger:restore_element
 */

/* jslint browser: true*/
/* global $, jQuery, console, RiotControl urls */

function ActivityStore(source, choices) {
    var store = this;
    riot.observable(this);
    store.el = 'activity';
    store.choices = choices || {};
    store.load(source);
    store.requesthistory = [];
    store.fieldvalidation = {
        'activity.activity_status': { validate_code_not_null: true }
    };
    store.root_element_type = 'object';

    store.requestopts = {
        create_fail: 'activity_fail',
        update_done: 'activity_updated',
        update_fail: 'activity_update_failed',
        validation: 'activity_validation_error'
    };

    var dird_finances = document.getElementById("dird_finances");
    if (dird_finances) {
        store.dird_finances = JSON.parse(dird_finances.textContent);
        store.dird_project_completion = JSON.parse(dird_project_completion.textContent);
        store.dird_compliance = JSON.parse(dird_compliance.textContent);
    }

    /**
     * Returns the URLS to use for an activity update or create
     * @method urls
     * @memberof ActivityStore
     */
    store.urls = function () {
        return { update: urls.update_general };
    };

    store.on('route', function (route) { store.trigger('route_tab', route); });

    store.on(store.requestopts.update_done, function (data, returned_data) {
        if (_.isUndefined(returned_data)) {
            console.error('No data is provided. This would empty the data in the store'); // eslint-disable-line no-console
        } else {
            store.trigger('reload_activity', returned_data);
            store.trigger('update_activity_completion', returned_data);
        }
    });
    store.on(store.requestopts.validation, function (tag) { store.validationFailed(tag); });
    store.on('toggle_delete_activity', function (tag) { store._add_delete_tag(tag); });
    store.on('toggle_delete_path_activity', function (path) { store._toggle_delete_path(path); });
    store.on('update_activity', function (tag) { store._add_update_path(tag); });
    store.on('create_', function (tag) { store._add_create_path(tag); });
    store.on('reload_activity', function (data) {
        if (data.budget_set.length && data.default_currency.code !== store._initial.default_currency.code) {
            store.showDefaultCurrencyWarning = true;
        }
        store.load(data);
    });
    store.on('restore_activity', function () { store.restore(); });
    store.on('refresh_completion', function () {
        var completion_url = '{% url "activitycompletion-detail" "XXXXXX"  %}'.replace('XXXXXX', store.activity.id);
        $.getJSON(completion_url, function (response) {
            RiotControl.trigger('update_activity_completion', response);
        });
    });
    store.clean_data = function (tag) {
        var data = _.cloneDeep(store[store.el]);
        var return_data = {};
        // Only submit data from the tab passed to "store.save"!

        var child_tags = tag.list_child_tags();
        var child_paths = _.compact(_.map(child_tags, 'path'));
        _.pull(child_paths, store.el);
        _(child_paths).each(function (p) {
            _.set(return_data, p, _.get(store, p));
        });
        if (_.has(return_data, 'participating_organisations')) {
            return_data.participating_organisations = _.reject(data.participating_organisations, { organisation: { code: undefined } });
        }
        return return_data[store.el];
    };

    store.get_title = function () {
        var title_in_page_langage;
        var title_in_english;
        var title_set = store.activity.title_set;
        var get_title_in_language = function (language_code) {
            var title_object = _.find(title_set, function (title) {
                return title.language === language_code;
            });
            return (title_object === undefined) ? '' : title_object.title;
        };

        title_in_page_langage = get_title_in_language(window.page_language);
        if (title_in_page_langage) { return title_in_page_langage; }

        title_in_english = get_title_in_language('en');
        if (title_in_english) { return title_in_english; }

        if (title_set.length) { return title_set[0].title; }
        return '';
    };
}

/* {% load i18n %} */
/* global stores opts */
var tag = this;

function store() { return stores.activityStore; }
function activity() { return store().activity; }
function initial() { return store()._initial; }

tag.mixin('SerializerMixin'); // Provides serialization functions
tag.mixin('TabMixin'); // Provides modal for nagivation between tags
tag.mixin('ValidationMixin');

tag.store = store();
tag.activity = activity();

// tell btn-grp-editor to always try to save this tab's contents. Done as a
// fix to more complex, mult-lang, description fields not detecting changes
tag.save_tab_always = true;

tag.classes = {
    date: {
        date_label: 'control-label',
        date: ''
    },
    dropdown: {
        label: 'control-label'
    }
};

tag.on('mount', function set_riotcontrol_listener() {
    RiotControl.on('activity_updated', function set_tag_state() {
        window.banner_message.show('Saved', 'success');
        tag.validated = true;
        tag.update();
    });

    RiotControl.on('tag_validationstate_changed', function validate_if_activityfield(info) {
        if (_.startsWith(info.tag.path, 'activity') && store === info.tag.store) {
            tag.validate();
        }
    });
});

tag.on('updated', function () {
    if (_.isUndefined(tag._validated_loudly)) {
        tag._validated_loudly = 'done';
        tag.fn_validate._validate_loudly(tag);
    }
});


tag.on('before-mount', function () {
    /**
     * given an IATI code type, return the associated date
     * @param code
     * @returns {string}
     * @private
     */
    function date_from_code(code) {
        var data = activity().activity_dates;
        var language_index = data.map(function dateindex(date, index) {
            if (date.type.code === code) {
                return index;
            }
            return undefined;
        }).filter(function defined_index_only(index) {
            return index !== undefined;
        });

        if (language_index.length === 0) {
            language_index = data.push({ iso_date: null, type: { code: 1 } }) - 1;
        }

        return '.activity_dates[' + language_index[0] + '].iso_date';
    }
    tag.dates = {
        start_planned: date_from_code(1),
        start_actual: date_from_code(2),
        end_planned: date_from_code(3),
        end_actual: date_from_code(4)
    };
    tag.activity = activity();
});


function reset_general_tag() {
    store().trigger('reload_activity', initial());
    tag.update();
}
tag.reset_general_tag = reset_general_tag;

tag.on('update', function set_badge() {
    // Set the badge display to show whether this activity is locally created or an IATI import
    var ref = tag.bystring('activity.xml_source_ref', {});
    tag.local = ref === 'mohinga' || ref === 'Myanmar' || !ref;
    tag.badge = tag.local ? { class: 'local_badge', text: '{% trans "Created Locally" %}' } : {
        class: 'iati_badge',
        text: '{% trans "Imported from IATI" %}'
    };
});

tag.has_changed = function () {
    /* Handling of this tab should not bother about empty title and narrative fields */
    /* Comparison everything except titles, descriptions, participating organisations */
    if (!_.isEqual(
        _.omit(initial(), ['title_set', 'descriptions', 'participating_organisations', 'openly_status']),
        _.omit(activity(), ['title_set', 'descriptions', 'participating_organisations', 'openly_status'])
    )) { return true; }

    /* Comparison of titles and descriptions */
    if (!_.isEqual(
        _.reject(activity().title_set, function (e) { return e.title === ''; }),
        _.reject(initial().title_set, function (e) { return e.title === ''; })
    )) { return true; }

    if (!_.isEqual(
        _.reject(activity().descriptions, function (e) { return e.description === ''; }),
        _.reject(initial().descriptions, function (e) { return e.description === ''; })
    )) { return true; }
    return false;
};

tag.save = function () {
    tag.validate();
    if (tag.validated){return store().save(tag);}
};

// Functions for "Unsaved Changes" modal
// tag.save: tag.save,
tag.discard = reset_general_tag;

// {% block project_js_code %}
/* {# Project specific code can be inclcuded here #} */
// {% endblock project_js_code %}

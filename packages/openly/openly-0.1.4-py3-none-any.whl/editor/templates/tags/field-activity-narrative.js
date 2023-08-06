/*
 {% load i18n %}
 {% get_current_language as LANGUAGE_CODE %}
 */
/** @class field-narrative */
var tag = this;
var opts = tag.opts;
tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');

tag.narrative_type_text = opts.narrative_type_text || 'narrative';
tag.helptext = opts.helptext || 'This is help text';

tag.narrative_type_text = opts.narrative_type_text || 'narrative';
tag.helptext = opts.helptext || 'This is help text';

tag.classes = {
    title: {
        input: '', label: 'control-label'
    }
};

/** returns the path to the narrative which matches the current narrative type
 * and the currently selected language
 * @param language_code {string}
 */

function set_narrative(language_code) {
    var descriptions = tag.store[tag.store.el].descriptions;
    var find = { language: language_code, type: { code: _.toInteger(tag.opts.narrative_type) } };
    var index;
    var language_path;
    function get_or_create_index() {
        function create_index() { var create = _.clone(find); create.description = ''; return descriptions.push(create) - 1; }
        function get_index() { return _.findIndex(tag.data, find); }
        index = get_index();
        return index === -1 ? create_index() : index;
    }
    language_path = '[' + get_or_create_index() + '].description';

    /* Return if an update is NOT required. An update can be necessary because the order of elements 
    changes in the array of narratives or the user chooses a different language to display. */
    if (language_path === tag.language_path && tag.language === language_code){return}
    tag.update({ language: language_code, language_path: language_path });
}

/* Set the initial language when the tag is mounted */
tag.on('mount', function () {
    tag.languages = tag.opts.languages || tag.parent.opts.languages || tag.opts.store.languages;
    set_narrative('{{ LANGUAGE_CODE }}');
});

tag.on('update', function (){
    set_narrative(tag.language);
});

tag.select_narrative = function select_narrative(e) { set_narrative(e.item.language_code); };

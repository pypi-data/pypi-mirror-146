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
        input: ''
    }
};

/** returns the path to the narrative which matches the current narrative type
 * and the currently selected language
 * @param language_code {string}
 */

function set_narrative(language_code) {
    var index;
    var narrative;
    var fieldname = opts.fieldname || 'description';
    var language_path;
    narrative = _.get(tag.store, tag.absolute_path());
    if (_.isUndefined(narrative)) { _.set(tag.store, tag.absolute_path(), []); narrative = _.get(tag.store, tag.absolute_path()); }
    index = _.findIndex(narrative, { language: language_code });
    if (index === -1) { index = narrative.push({ language: language_code }) - 1; }
    language_path = '[' + index + '].' + fieldname;

    /* Return if an update is NOT required. An update can be necessary because the order of elements 
    changes in the array of narratives or the user chooses a different language to display. */
    if (tag.language_path === language_path && tag.language === language_code) { return }
    tag.update({ language: language_code, language_path: language_path});
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

/* {% load i18n %} */
/* global opts */

var tag = this;
var path = 'title_set';

function activity() { return tag.store.activity; }
function title_set() { return _.get(activity(), path, []); }

tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');

tag.title = opts.title || 'Set the title';
tag.helptext = opts.helptext || 'This is help text';

tag.classes = { title: { input: '', label: 'control-label' } };

function select_language(language_code) {
    var data = title_set();
    var index;
    var text;
    var language_path;
    var title = _.find(data, { language: language_code });
    if (!_.isUndefined(title)) {
        text = title.title;
        index = _.indexOf(data, title);
    } else {
        text = '';
        index = data.push({ language: language_code, title: text }) - 1;
    }
    language_path = '[' + index + '].title'

    /* Return if an update is NOT required. An update can be necessary because the order of elements 
    changes in the activity titles or the user chooses a different language to display. */
    if (tag.language_path === language_path && tag.language === language_code){
        return;
    }
    tag.update({
        language: language_code,
        language_path: language_path,
    });
}
/**
 * sets the path to be linked to the input field
 * @param e
 */
tag.select_language = function (e) {
    return select_language(e.item.language_code);
};

/* Set the initial language when the tag is mounted */
tag.on('mount', function () {
    select_language(window.page_language);
});

tag.on('update', function(){
    select_language(tag.language);
})

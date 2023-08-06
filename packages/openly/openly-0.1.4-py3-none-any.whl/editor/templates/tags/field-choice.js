/** @class field-choice */
var tag = this;
tag.$sel = undefined;


tag.classes = tag.classes || {};
tag.data = tag.data || {};
tag.choices = tag.choices || [];

tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');
// tag defaults
tag.store.choices = tag.store.choices || {};

function getPlaceholder() {
    var placeholder = _.get(tag, 'opts.select2_opts.placeholder') || _.get(tag, 'opts.select_placeholder') || '------';
    return placeholder;
}


function convert_tuple_to_object(tuple) {
    return { value: tuple[0], text: tuple[1] };
}

function selectize() {
    var select_tag_selector;
    var placeholder = getPlaceholder();
    if (Boolean(tag.opts.select2) === true) {
        // repeating the <if> logic already in the HTML is necessary because Riot has not worked through the if attributes yet
        select_tag_selector = tag.opts.has_optgroup ? 'select.select-with-optgroup' : 'select.select-without-optgroup';
        _.set(tag, 'opts.select2_opts.placeholder', placeholder);
        tag.$sel = $(select_tag_selector, tag.root);
        tag.$sel.val(tag.data.code || '')
            .select2(tag.opts.select2_opts)
            .on('change', tag.change_select); // trigger a jQuery event: https://github.com/riot/riot/issues/2182
    }
}

tag.on('updated', function () {
    selectize();
});

tag.on('update', function () {
    /** Massage on update for tags that need to be updated when tags of the same family are updated.
     * Ex: sectors, locations, and sector working groups.
     */
    var categorized = _.clone(tag.opts.choices);
    var solo_options = [];
    tag.placeholder = getPlaceholder();
    if (tag.opts.choices !== undefined && tag.opts.has_optgroup !== undefined) {
        if (!_.isEqual(tag.opts.last_choices, tag.opts.choices)) {
            tag.opts.last_choices = _.clone(tag.opts.choices);
            tag.opts.choices.forEach(function (category, index) {
                var soloize = category.choices === undefined || (_.isArray(category.choices) && category.choices.length === 0);
                if (soloize) {
                    solo_options.push(category);
                    return;
                }
                categorized[index] = {
                    choices: category.choices,
                    text: _.toString(category.text)
                };
            });
            if (!_.isEqual(solo_options, tag.solo_options)) {
                tag.solo_options = solo_options;
            }
            // tag.solo_options = solo_options;
            if (!_.isEqual(tag.categorized, categorized)) {
                tag.categorized = categorized;
            }
        }
    } else if (tag.opts.no_data_transform && !tag.opts.has_optgroup) {
        tag.choices = tag.input_choices;
    }
});

tag.show_null = function () {
    var is_select2 = !_.isUndefined(tag.opts.select2);
    var cannot_reselect_null = !_.isUndefined(tag.opts.cannot_reselect_null);
    var not_set = _.isNull(tag.data.code) || _.isUndefined(tag.data.code) || tag.data.code === '';
    if (is_select2) { return false; }
    if (!cannot_reselect_null) { return true; }
    return !!not_set;
};

tag.on('before-mount', function () {
    /**
     * Reformat the Choices passed to the tag, a tuple of tuples, to a list of {value : text} pairs
     * @param original_choices
     */
    tag.placeholder = getPlaceholder();
    tag.input_choices = tag.opts.choices || tag.store.choices[tag.opts.choice_fieldname || tag.opts.fieldname];

    if (!tag.opts.no_data_transform) {
        tag.choices = tag.input_choices.map(convert_tuple_to_object);
    }
});

tag.on('mount', function () {
    tag.update(); /* This update is necessary as the tag may otherwise not inherit parent opts */
});

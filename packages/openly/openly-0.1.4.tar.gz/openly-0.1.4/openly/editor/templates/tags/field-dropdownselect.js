var tag = this;
tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');
tag.dropdown_open = false;


/**
 * Show less options
 * For example, only the top 10 curencies in use
 */
function show_less() {
    tag.opts.short_list = true;
    tag.dropdown_open = true;
    tag.get_choices();
    tag.update();
}
/**
 * Show more options
 */
function show_more() {
    tag.opts.short_list = false;
    tag.get_choices();
    tag.update();
}
/**
 * Toggle the dropdown
 */
function toggle_dropdown() {
    if (tag.dropdown_open === false) {
        tag.dropdown_open = true;
        tag.get_choices();
        tag.one('updated', function () {
            $('input[ref="search"]', tag.root).focus();
        });
    } else {
        tag.choose = {};
        tag.dropdown_open = false;
        tag.update();
    }
}

/**
 * Define the input choices in descending order of preference for
 * specific field names set in options
 * @returns {*}
 */
function get_choices() {
    var c = tag.store.choices || window.choices || {};
    var inputChoices;
    var outputChoices;
    var expression;
    var opts = tag.opts;
    var choices_length = parseInt(opts.max_length || '100', 10);

    if (tag.refs.search !== undefined && tag.refs.search.value !== '') {
        expression = new RegExp(_.escapeRegExp(tag.refs.search.value), 'gi');
    } else {
        expression = null;
    }
    opts.short_list = !!((opts.short_list === undefined || opts.short_list === true || opts.short_list === 'true') && _.isArray(opts.short_list_codes) && opts.short_list_codes.length > 0);
    if (expression) { opts.short_list = false; }

    function create_choice(choice) {
        /** Each selectable choice has a "code" which is generally  pk, a "name" to use as a label
         * and optionally "group" and "search" fields
        */
        var returned_choice;

        function getGroup(_choice) {
            var group;
            var default_group = 'solo';
            group = _.isArray(_choice) ? _choice[2] : _.get(_choice, tag.opts.groupfield || 'group');
            return group || default_group;
        }
        if (_.isArray(choice)) {
            returned_choice = {
                code: choice[0],
                name: choice[1] || choice[0],
                search: choice[3] // If exists
            };
        } else {
            returned_choice = {
                code: _.get(choice, tag.opts.codefield || 'code'),
                name: _.get(choice, tag.opts.namefield || 'name') || _.get(choice, tag.opts.codefield || 'code'),
                search: _.get(choice, tag.opts.searchfield || 'search')
            };
        }

        returned_choice.meta = {
            group: getGroup(choice),
            enabled: _.indexOf(opts.disabled_choices, (choice[0] || choice.code)) === -1,
            hidden: false
        };

        /* Hide option if there are many options to list (for performance reasons) or if there is a search string provided which does not match the search field */
        if (expression !== null) {
            returned_choice.meta.hidden = true;
            if (_.isArray(choice)) {
                if (expression.test(choice[0])) { returned_choice.meta.hidden = false; } else if (expression.test(choice[1])) { returned_choice.meta.hidden = false; } else if (expression.test(choice[3])) { returned_choice.meta.hidden = false; }
            } else if (_.isObject(choice)) {
                if (expression.test(choice.code)) { returned_choice.meta.hidden = false; } else if (expression.test(choice.name)) { returned_choice.meta.hidden = false; } else if (expression.test(choice.search)) { returned_choice.meta.hidden = false; }
                /* #2432 Show all sub areas when the parent area name matches */
                if (expression.test(choice.full_name)) { returned_choice.meta.hidden = false; }
            }
        }

        if (opts.short_list && opts.short_list_codes && _.indexOf(opts.short_list_codes, returned_choice.code) === -1) {
            returned_choice.meta.hidden = true;
        }
        return returned_choice;
    }

    if (opts.choice_fieldname !== undefined) {
        inputChoices = c[opts.choice_fieldname];
    } else if (opts.fieldname !== undefined) {
        inputChoices = c[opts.fieldname];
    } else (inputChoices = [[1, 'one'], [2, 'two']]);

    tag.choice_count = _.isArray(inputChoices) ? inputChoices.length : undefined;
    tag.choice_count = _.isObject(inputChoices) ? _.size(inputChoices) : undefined;

    /* Reformat a choice list of 2, 3, 4-element lists/tuples to an object for iteration */
    outputChoices = _(inputChoices).map(create_choice)
        .filter(function (choice) { return !choice.meta.hidden; })
        .groupBy('meta.group')
        .value();

    outputChoices.solo = outputChoices.solo || [];
    if (outputChoices.solo.length > choices_length) {
        outputChoices.solo = _(outputChoices.solo).slice(0, choices_length).value();
        tag.choose = outputChoices;
        opts.too_many_options = true;
    } else {
        tag.choose = outputChoices;
        opts.too_many_options = false;
    }
}

tag.on('updated', function wrap() {
    var expression;
    var content;
    var replacement = '<span class="matched-search">$&</span>';

    if (!tag.refs.search || !tag.refs.search.value) {
        return;
    }
    expression = new RegExp(tag.refs.search.value, 'gi');

    $('a[data-code]', tag.root).each(function () {
        content = $(this).text();
        if (expression.test(content)) {
            $(this).html(content.replace(expression, replacement));
        }
    });
});

function handleClickOutside(e) {
    /* Click outside the dropdown to close it, unless the target of the click is a "show_more" or "show_less" button */
    if (
        !tag.root.contains(e.target) && tag.dropdown_open && !($(e.target).hasClass('show_more') || $(e.target).hasClass('show_less'))) {
        tag.toggle_dropdown();
    }
    tag.update();
}

tag.on('mount', function () {
    document.addEventListener('click', handleClickOutside);
    tag.update();
});

tag.on('unmount', function () {
    document.removeEventListener('click', handleClickOutside);
});

tag.on('before-mount', function () {
    var fn = {
        display_name: function () {
            var label;
            var data = tag.chosen || tag.data || (tag.initial_dropped ? undefined : tag.opts.initial) || {};
            if (!_.isObject(data) && tag.store && _.isFunction(tag.store.get_choice)) { return tag.store.get_choice(tag.opts.choice_fieldname || tag.opts.fieldname, data); }
            label = data.name || tag.opts.select_name || data.code || tag.opts.placeholder;
            return label;
        },
        display_code: function () {
            return (tag.chosen || tag.data || {}).code;
        },
        display_search: function () {
            return (tag.chosen || tag.data || {}).search;
        },
        display_code_and_search: function (choice) {
            var string = '';
            if (choice.code) { string += choice.code; }
            if (choice.code && choice.search && (choice.code !== choice.search)) { string += ' / '; }
            if (choice.search && (choice.code !== choice.search)) { string += choice.search; }
            return '(' + string + ')';
        },
        choose: function (e) {
            var data;
            if (_.isString(tag.data)) { data = e.item.choice.code; } else (data = { code: e.item.choice.code, name: e.item.choice.name });
            if (_.includes(tag.opts.disabled_choices, data.code || data)) { return; }
            if (_.has(tag.opts, 'onchoose')) {
                /* React on user choosing an option by triggering a named event on the parent tag */
                e.preventDefault();
                data = _.clone(e.item.choice);
                tag.parent.trigger(tag.opts.onchoose, e, data, tag);
                tag.toggle_dropdown();
                tag.update({ chosen: data });
            } else {
                /* When no trigger name is included, the mixin-formfield set_dropdown_select function is called */
                tag.set_dropdown_select(e, data);
            }
        },
        nullify_dropdown_select: function (e) {
            if (_.has(tag.opts, 'onchoose')) {
                /* React on user choosing an option by triggering a named event on the parent tag */
                e.preventDefault();
                tag.parent.trigger(tag.opts.onchoose, e, null, tag);
                tag.toggle_dropdown();
                tag.update({ chosen: { name: '' } });
            } else {
                tag.nullify_dropdown_select();
            }
        }
    };
    tag.fn = fn;
});
// tag.fn = fn;
tag.show_more = show_more;
tag.get_choices = get_choices;
tag.toggle_dropdown = toggle_dropdown;
tag.show_less = show_less;

/* globals gettext */
/* exported ValidationMixin */

var ValidationMixin = {

    /**
     * Set up the paths a tag will listen to changes for and establishes
     * RiotControl listening for the tag instance
     */
    init: function () {
        var tag = this;
        var on_path_updated;
        var index_re_find = '\\[\\d+\\]'; // Regex fragmant to find any element of an array
        var establish_listeners;
        var validations = _(tag.opts)
            .keys()
            .filter(function (key) { return _.startsWith(key, 'validate_'); })
            .value();

        tag.on('before-mount', function () { tag.validated = true; });
        tag.on('mount', function () {
            this.validate();
        });

        tag.opts.ValidationMixin = {};
        RiotControl.on('path_updated', function (changed_tag) { if (tag === changed_tag) { tag.validate(); } });

        /* Troubleshooting code */
        if (_.isUndefined(tag.store) || tag.store === {}) {
            console.warn(tag, 'Tag store is not defined'); // eslint-disable-line no-console
            if (_.isUndefined(tag.parent.store) || tag.store === {}) {
                tag.store = tag.parent.store;
                console.warn('Using the store from the parent tag. Explicity setting the store is recommended, e.g. store={opts.store}'); // eslint-disable-line no-console
            } else {
                console.warn(tag, 'Parent Tag store is also not defined'); // eslint-disable-line no-console
            }
        }
        /**
         * After a tag value has changed, all tags which "listen" to it will also have
         * their "value_has_changed" flag set and will have their own validation routine run.
         * @param triggering_tag
         */
        on_path_updated = function (triggering_tag) {
            /* Early return if the triggering tag is from a different store */

            if (tag.store !== triggering_tag.store) {
                return;
            }
            if (tag === triggering_tag) {
                return;
            }

            if (_.has(tag, 'opts.ValidationMixin.listener_regex')) {
                if (triggering_tag.path.match(tag.opts.ValidationMixin.listener_regex)) {
                    if (triggering_tag.value_has_changed) { tag.value_has_changed = true; }
                    tag.validate();
                }
            }
            if (_.has(tag, 'opts.ValidationMixin.listener_list')) {
                if (_.includes(tag.opts.ValidationMixin.listener_list, triggering_tag.path)) {
                    if (triggering_tag.value_has_changed) { tag.value_has_changed = true; }
                    tag.validate();
                }
            }
            if (_.has(tag, 'opts.ValidationMixin.listener_startswith')) {
                if (_.startsWith(triggering_tag.path, tag.opts.ValidationMixin.listener_startswith)) {
                    if (triggering_tag.value_has_changed) { tag.value_has_changed = true; }
                    tag.validate();
                }
            }
        };

        /**
        Functions in this object will establish tag listeners based on the name of the validation to be applied
         */
        establish_listeners = {

            current_edit: function () {
                tag.opts.ValidationMixin.listener_startswith = '';
                RiotControl.on('path_updated', on_path_updated);
            },

            store: function () {
                tag.opts.ValidationMixin.listener_startswith = '';
                RiotControl.on('path_updated', on_path_updated);
            },

            date_order: function () {
                tag.opts.ValidationMixin.listener_list = _.map(tag.opts.validate_date_order.split(' '), function (triggering_path) {
                    return tag.absolute_path() + triggering_path;
                });
                RiotControl.on('path_updated', on_path_updated);
            },
            dates_valid: function () {
                tag.opts.ValidationMixin.listener_list = _.map(tag.opts.validate_dates_valid.split(' '), function (triggering_path) {
                    return tag.absolute_path() + triggering_path;
                });
                RiotControl.on('path_updated', on_path_updated);
            },
            sum: function () {
                var valops = tag.opts.ValidationMixin;
                valops.target = _.get(tag, 'opts.validate_sum');
                valops.accumulate = valops.target.split(',')[0];
                valops.path_to_property = valops.target.split(',')[1];
                valops.target_value = _.toNumber(valops.target.split(',')[2]);
                valops.listener_regex = valops.accumulate + index_re_find;// + valops.path_to_property;
                RiotControl.on('path_updated', on_path_updated);
            },
            banner: function () {
                tag.opts.ValidationMixin.listener_startswith = tag.opts.path || '';
                RiotControl.on('tag_validation_state_changed', on_path_updated);
            },
            title_not_null: function () {
                tag.opts.ValidationMixin.listener_startswith = tag.absolute_path();
                RiotControl.on('path_updated', on_path_updated);
            },
            unique_in_array: function () {
                tag.opts.ValidationMixin.listener_regex = tag.absolute_path() + index_re_find;// + tag.opts.validate_unique_in_array.split('.')[0];
                RiotControl.on('path_updated', on_path_updated);
            },
            policy_marker: function () {
                tag.opts.ValidationMixin.listener_startswith = tag.absolute_path();
                RiotControl.on('path_updated', on_path_updated);
            },
            number_not_in: function () {
                var valops = tag.opts.ValidationMixin;
                valops.target = _.get(tag, 'opts.validate_number_not_in');
                valops.accumulate = valops.target.split(',')[0];
                valops.path_to_property = valops.target.split(',')[1];
                valops.excludes = _.toNumber(valops.target.split(',')[2]);
                valops.listener_regex = valops.accumulate + index_re_find;// + valops.path_to_property;
                RiotControl.on('path_updated', on_path_updated);
            },
            array_not_null: function () {
                // Initialize this validator with a string of paths.
                // An error will be raised if there are a mixture of NULL and NOT NULL's in the array of objects
                // Requires two specifications on the tag: validate_array_not_null and validation_array_fields
                var valops = tag.opts.ValidationMixin;
                valops.validate_array = tag.opts.validate_array_not_null;
                valops.validate_paths = tag.opts.validation_array_fields.split(' ');
                valops.listener_regex = valops.validate_array + index_re_find;
                RiotControl.on('path_updated', on_path_updated);
            }
        };

        /**
         * Tags can register to be validated when another tag changes here.
         * Validation triggering is based on the 'path' of the triggering tag, and
         * the path match can be made based on a list, regex or path starting with.
         */
        _(validations).each(function (validator) {
            _.invoke(establish_listeners, validator.replace('validate_', ''));
        });
    },


    list_child_tags: function () {
        var tag = this;
        var child_returns;
        var returns = _(tag.tags).values().flatten().value();
        _.remove(returns, _.isUndefined);
        _.each(returns, function (child) {
            if (_.isFunction(child.list_child_tags)) {
                child_returns = child.list_child_tags();
                returns = _.concat(returns, child_returns);
            }
            return returns;
        });
        return _.flatten(_.concat(returns));
    },

    validate_child_tags: function () {
        _.each(this.list_child_tags(), function (child) {
            if (_.isFunction(child.validate)) {
                child.validate();
            }
        });
    },

    failed_child_tags: function () {
        var filter_deleted_tags = function (child_tags) {
            return _.filter(child_tags, function (child_tag) {
                return !_(child_tag.store._delete_paths).some(function (i) {
                    return _.startsWith(child_tag.path, i);
                });
            });
        };
        var tag = this;
        var child_tags = tag.list_child_tags();
        child_tags = _(child_tags).filter(function (t) {
            return t.validated === false;
        }).value();
        return filter_deleted_tags(child_tags);
    },

    child_tags_validated: function () {
        var tag = this;
        return tag.failed_child_tags().length === 0;
    },

    get_validation_state: function (tag) {
        var path = _.invoke(tag, 'absolute_path');
        var initial_path = path.replace(tag.store.el, '_initial');
        return {
            value: _.get(tag.store, path),
            initial: _.get(tag.store, initial_path),
            changed: tag.value_has_changed,
            validated: tag.validated
        };
    },

    get_data: function (tag, path) {
        if (_.startsWith(tag.opts.path, 'this.')) {
            return _.get(tag.parent, _.replace(tag.opts.path, 'this.', ''));
        }
        return _.get(tag.store, (tag.opts.root_el || tag.store.el || tag.store.root_element) + (path || tag.opts.path));
    },

    refresh_data: function (tag) {
        tag.data = tag.get_data(tag);
        return tag.data;
    },

    validate_current_edit: function (tag) {
        var child_tags;
        if (!_.isFunction(tag.list_child_tags)) {
            /* Dev - might want to check this */
            console.warn('A tag is missing list_child_tags function', tag);
            return true;
        }
        if (tag.current_edit === -1) {
            tag.current_edit_validated = true;
            return tag.current_edit_validated;
        }
        child_tags = _.filter(tag.list_child_tags(), function (child_tag) {
            return _.startsWith(child_tag.path, tag.path + '[' + tag.current_edit + ']');
        });

        tag.current_edit_validated = !_.includes(_.map(child_tags, 'validated'), false);
        return tag.current_edit_validated;
    },

    validate: function () {
        var tag = this;
        var tagname = this.root.tagName.toLowerCase().replace(/-/g, '_');
        var validation_rules = _.pickBy(this.opts, function (value, key) { return _.startsWith(key, 'validate_'); });
        var store_rules = _.get(tag, 'store.fieldvalidation.' + this.opts.path);
        var validation_results = {};
        var former_state_errors = _.cloneDeep(tag.errors) || {};
        var former_state_validated = _.clone(tag.validated);

        if (!_.isUndefined(store_rules) && !_.isObject(store_rules)) {
            console.warn('ValidationMixin: Store-defined rules will be ignored if they are not an object'); // eslint-disable-line no-console
            store_rules = undefined;
        }

        validation_rules = _.defaults(validation_rules, store_rules || {});
        _.each(validation_rules, function runOneValidation(args, validationRule) {
            var func_name = validationRule.replace('validate_', '');
            var path = ['fn_validate', tagname, func_name];
            var func = _.get(tag, path);

            if (!_.isFunction(func)) {
                path = ['fn_validate', 'global', func_name];
                func = _.get(tag, path);
            }

            if (!_.isFunction(func)) {
                console.error('ValidationMixin: Validation function is not defined ' + path.join('.')); // eslint-disable-line no-console
            }
            validation_results[validationRule] = _.invoke(tag, path, tag, args);
        });

        tag.validation_results = validation_results;

        tag.errors = _.pickBy(validation_results, function (value) { return value !== true; });
        tag.error = _.values(tag.errors).join(', '); // Deprecated
        tag.validated = _.keys(tag.error).length === 0;

        if (!_.isEqual(tag.errors, former_state_errors) || !_.isEqual(tag.validated, former_state_validated)) {
            tag.store.trigger('tag_validation_state_changed', tag);
            tag.update();
        }
        return tag.validated;
    },

    validated_with_children: function (tag) {
        var children = tag.list_child_tags();
        var children_failed = _.filter(children, { validated: false });
        var children_changed_failed = _.filter(children_failed, { value_has_changed: true });
        tag.validate();
        return tag.validated && children_changed_failed.length === 0;
    },

    /**
     * Functions within this object are the validation routines to be run. "Private" functions (which may be shared
     * between tags) start with an underscore.
     * Functions are accessed as "field_name.validation_name"
     */
    fn_validate: {
        /* Show child tag failures loudly */
        /* Sets values required for the tag to know it needs to be have "Loud" validation errors */
        _validate_loudly: function (tag) {
            var child_tags_failed = _.filter(tag.list_child_tags(), { validated: false });
            _.set(tag, 'opts.ValidationMixin.validation_class', 'major');
            _.set(tag, 'opts.ValidationMixin.show_as_changed', true);
            _.invokeMap(child_tags_failed, 'validate');
            child_tags_failed = _.filter(tag.list_child_tags(), { validated: false });
            _.each(child_tags_failed, function (ctag) {
                _.set(ctag, 'opts.ValidationMixin.validation_class', 'major');
                _.set(ctag, 'opts.ValidationMixin.show_as_changed', true);
                if (ctag.isMounted) {
                    tag.update();
                }
            });
            if (tag.isMounted) {
                tag.update();
            }
        },

        _isValidDate: function (date_string) {
            var date_regex = /^([0-9]{4})-?(1[0-2]|0[1-9])-?(3[0-1]|0[1-9]|[1-2][0-9])$/;
            return date_regex.test(date_string || '');
        },
        _isValidMomentDate: function (date_string) {
            /* Catches 'February 30' etc */
            return moment(date_string).isValid();
        },
        _pathMustNotBeNull: function (data, property) {
            var check;
            if (!_.isUndefined(property)) {
                check = _.get(data, property);
            } else {
                check = data;
            }
            if (check === '' || _.isUndefined(check) || _.isNull(check)) {
                return gettext('Required');
            }
            return true;
        },
        _banner: function (showorhide, state, message) {
            if (showorhide === 'show' && !_.isUndefined(message)) {
                window.banner_message.show(gettext('There are validation errors on this tab.'), 'warning');
                return;
            }
            window.banner_message.hide('warning');
        },

        _bannerOnCurrentEditChildFailure: function (tag, message) {
            var edit = _.get(tag, 'editing.index', tag.current_edit);
            var child_tags;
            if (_.isUndefined(edit) || edit === -1) { return true; }
            child_tags = _(tag.list_child_tags()).filter(function (child_tag) {
                return _.startsWith(child_tag.path, tag.path + '[' + edit + ']');
            }).value();
            return tag.fn_validate._bannerOnChildFailure(tag, message, child_tags);
        },

        _bannerOnChildFailure: function (tag, message, child_tags) {
            var test_tags = child_tags || tag.list_child_tags();
            var invalid_child_tags;
            var validated;
            _.invokeMap(tag.list_child_tags(), 'validate');
            if (tag.opts.validation_banner_initial === 'true') {
                invalid_child_tags = _.filter(test_tags, { validated: false });
            } else {
                invalid_child_tags = _.filter(test_tags, function (child_tag) {
                    return (child_tag.value_has_changed || _.get(child_tag, 'opts.ValidationMixin.show_as_changed')) && !child_tag.validated;
                });
            }
            validated = invalid_child_tags.length === 0;
            if (!validated) {
                tag.validated = validated;
                tag.fn_validate._banner('show', 'warning', message);
                return message;
            }

            if (tag.validated !== validated) {
                tag.validated = validated;
                tag.update();
            }
            tag.fn_validate._banner('hide', 'warning');
            return true;
        },

        global: {
            current_edit: function (tag, prop) {
                var current_edit_validated;
                if (prop === '') {
                    current_edit_validated = tag.validate_current_edit(tag);
                } else if (prop === 'parent') {
                    current_edit_validated = tag.validate_current_edit(tag.parent);
                }
                if (current_edit_validated !== tag.save_enabled) {
                    tag.save_enabled = current_edit_validated;
                    tag.update();
                }
                return true;
            },
            child_tags: function (tag) {
                var new_state;
                var current_state = tag.validated_with_children;
                var hasChanged = _.isFunction(tag.hasChanged) ? tag.hasChanged() : true;
                // tag.validate_child_tags();
                new_state = tag.child_tags_validated();

                if (new_state !== current_state && hasChanged) {
                    tag.update({
                        validated_with_children: new_state,
                        save_enabled: new_state
                    });
                }
            },
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnChildFailure(tag, message);
            }
        },

        banner_message: {},
        confirm_delete_modal: {},
        discard_modal: {},
        field_choice: {
            /** Ensure that the "code" property of the tag's data is not null */
            code_not_null: function (tag) {
                var data = tag.refresh_data(tag);
                return tag.fn_validate._pathMustNotBeNull(data, 'code');
            }
        },
        field_date: {
            is_valid: function (tag) {
                var data = tag.refresh_data(tag);
                var valid = tag.fn_validate._isValidDate(data);
                if (_.isUndefined(data) || tag.data === '' || _.isNull(tag.data) || !valid) {
                    return gettext('This date is not valid');
                }
                return true;
            },
            not_null: function (tag) {
                var data = tag.refresh_data(tag);
                var valid = tag.fn_validate._isValidDate(data);
                if (_.isUndefined(data) || tag.data === '' || _.isNull(tag.data) || !valid) {
                    return gettext('Required');
                }
                return true;
            },
            past: function (tag) {
                var data = tag.refresh_data(tag);
                var valid = tag.fn_validate._isValidDate(data);
                if (valid) {
                    if (!moment(data).isBefore(moment())) {
                        return gettext('This date cannot be in the future.');
                    }
                }
                return true;
            },
            future: function (tag) {
                var data = tag.refresh_data(tag);
                var valid = tag.fn_validate._isValidDate(data);
                if (valid) {
                    if (!moment(data).isAfter(moment())) {
                        return gettext('This date cannot be in the past.');
                    }
                }
                return true;
            }
        },
        field_dropdownselect: {
            code_not_null: function (tag) {
                var data = tag.refresh_data(tag);
                return tag.fn_validate._pathMustNotBeNull(data, 'code');
            },
            not_null: function (tag) {
                if (tag.opts.validate_not_null === false) { return true; }
                return tag.fn_validate._pathMustNotBeNull(tag.refresh_data(tag));
            }
        },
        field_input: {
            numeric: function (tag) {
                var data = tag.refresh_data(tag);
                var num = _.toNumber(data);
                if (!_.isNumber(num) || _.isNaN(num)) {
                    return gettext('Must be a number');
                }
                return true;
            },

            not_null: function (tag) {
                var data = tag.refresh_data(tag);
                if (_.isUndefined(data) || _.isNull(data) || data === '' || !/\S/.test(data)) {
                    return gettext('Required');
                }
                return true;
            },
            positive: function (tag) {
                var data = tag.refresh_data(tag);
                var num = _.toNumber(data);
                if (_.isUndefined(data) || _.isNull(data) || data === '') { return gettext('Required'); }
                if (_.isNaN(num)) { return gettext('Must be a number'); }
                if (num <= 0) { return gettext('Must be a number greater than zero'); }
                return true;
            }
        },
        field_modifiedspan: {},
        field_narrative: {},
        field_select: {},
        field_textarea: {
            not_null: function (tag) {
                var data = tag.refresh_data(tag);
                return tag.fn_validate._pathMustNotBeNull(data);
            }
        },
        field_title: {
            title_not_null: function (tag) {
                var titles = _.map(_.get(tag.store, tag.path), 'title');
                var valid_title = _.find(titles, function (title) {
                    return _.isString(title) && title !== '';
                });
                if (_.isUndefined(valid_title)) {
                    return gettext('Required');
                }
                return true;
            }
        },
        validate_tag: {
            not_null: function (tag) {
                var data = tag.refresh_data(tag);
                return tag.fn_validate._pathMustNotBeNull(data);
            }
        },
        validate_group: {

            _items: function (tag, path) {
                var items = _(_.get(tag.store, path));
                var get_by;
                var compare;

                if (_.has(tag.opts, 'validator_filter')) {
                    get_by = tag.opts.validator_filter.split(',')[0];
                    compare = tag.opts.validator_filter.split(',')[1];
                    items = _(items).filter(function (item) {
                        return _.get(item, get_by) === compare;
                    });
                }

                if (_.has(tag.opts, 'validator_exclude')) {
                    get_by = tag.opts.validator_exclude.split(',')[0];
                    compare = tag.opts.validator_exclude.split(',')[1];
                    items = _(items).filter(function (item) {
                        var i = _.get(item, get_by);
                        if (compare === 'null') {
                            return !_.isNull(i) && !_.isUndefined(i) && i !== '';
                        }
                        return i !== compare;
                    });
                }
                return items.value();
            },

            dates_valid: function (tag) {
                var dates = _.map(tag.opts.ValidationMixin.listener_list, function (listener) {
                    return _.get(tag.store, listener);
                });
                var valid = _.map(dates, function (date) {
                    return tag.fn_validate._isValidMomentDate(date);
                });
                if (!_.every(valid)) {
                    return gettext('There is an invalid date');
                }
                return true;
            },
            date_order: function (tag) {
                var dates = _.map(tag.opts.ValidationMixin.listener_list, function (listener) {
                    return _.get(tag.store, listener);
                });
                var valid = _.map(dates, function (date) {
                    return tag.fn_validate._isValidDate(date);
                });
                var start_date;
                var end_date;
                if (_.every(valid, function (v) {
                    return v === true;
                })) {
                    start_date = moment(dates[0])
                    end_date = moment(dates[1])
                    if (end_date.isBefore(start_date, 'day')) {
                        return gettext('The start date must occur before the end date');
                    }
                }
                if (valid[1] && !valid[0]) {
                    return gettext('An end date must have a valid start date');
                }

                return true;
            },
            sum: function (tag) {
                /* Called with a "target" of comma separated path tag.store and property to accumulate
                 * For example 'sectors,percentage,100'
                 * */
                var valops = tag.opts.ValidationMixin;
                var items = tag.fn_validate.validate_group._items(tag, valops.accumulate);
                var total;
                var roundedTotal;
                var precision = 3;
                if (items.length === 0 && !_.has(tag.opts, 'validator_allow_empty')) { return true; }
                total = _.reduce(items, function (sum, n) {
                    return sum + _.toNumber(_.get(n, valops.path_to_property));
                }, 0);
                /*
                Prevent false positive for floating point rounding errors - see https://github.com/catalpainternational/openly/issues/2347 
                Round to 3 decimal places
                */
                roundedTotal = _.round(total, precision);
                if (roundedTotal !== valops.target_value) {
                    return gettext('Percentages should add up to 100.');
                }
                return true;
            },
            number_not_in: function (tag) {
                var valops = tag.opts.ValidationMixin;
                var items = tag.fn_validate.validate_group._items(tag, valops.accumulate);

                var values = _.map(_.map(items, valops.path_to_property), _.toNumber);
                if (_.includes(values, valops.excludes)) {
                    return 'A ' + valops.path_to_property + ' cannot be ' + valops.excludes;
                }
                return true;
            },
            unique_in_array: function (tag) {
                var items = tag.fn_validate.validate_group._items(tag, tag.absolute_path());
                var item_values = _(items).map(tag.opts.validate_unique_in_array).value();
                if (!_.isEqual(_.uniq(item_values), item_values)) {
                    return gettext('These must be unique values');
                }
                return true;
            },
            array_not_null: function (tag) {
                // If one "Code" in an array is set, ALL "Code" in the array must be set
                var all_are_null = function (arr) { return _(arr).every(_.isNull); };
                var none_are_null = function (arr) { return !_(arr).includes(null); };
                var all_or_none = function (arr) {
                    return all_are_null(arr) || none_are_null(arr);
                };
                var opts = tag.opts.ValidationMixin;
                var returns = _.map(_.get(tag.store, opts.validate_array), function (array_object) {
                    return all_or_none(_(opts.validate_paths).map(function (field_name) {
                        return _.get(array_object, field_name);
                    }));
                });
                return _.includes(returns, false) ? 'There is a missing value' : true;
            }
        },
        form_activity: {},
        form_completion: {},
        form_navigation: {},
        help_field: {},
        location_edit: {},
        policy_marker_edit: {
            policy_marker: function (tag) {
                var code = _.get(tag.store, tag.path + 'policy_marker.code');
                var validated = !_.isUndefined(code) && !_.isNull(code) && !(code === '');
                return !validated ? 'Policy Marker cannot be empty.' : true;
            },
            significance: function (tag) {
                var code = _.get(tag.store, tag.path + 'significance.code');
                var validated = !_.isUndefined(code) && !_.isNull(code) && !(code === '');

                return !validated ? 'Significance cannot be empty' : true;
            }
        },
        publish_button: {},
        required_field: {},
        sector_edit: {},
        sector_working_group_edit: {},
        tab_contacts: {},
        tab_finances: {},
        tab_general: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnChildFailure(tag, message);
            }
        },
        tab_locations: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnChildFailure(tag, message, tag.tags['validation-group']);
            }
        },
        tab_organisations: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnChildFailure(tag, message);
            }
        },
        tab_results: {},
        tab_sectors: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnChildFailure(tag, message);
            }
        },
        tag_formfunctions: {},
        tab_transactions: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnCurrentEditChildFailure(tag, message);
            }
        },
        tab_budgets: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnCurrentEditChildFailure(tag, message);
            }
        },
        tab_documents: {
            banner: function (tag) {
                var message = gettext('There are validation errors on this tab.');
                return tag.fn_validate._bannerOnCurrentEditChildFailure(tag, message);
            }
        },
        cancel_save_group: {
        },
        field_upload: {
            type: function (tag) {
                var message = gettext('Please choose a different file format');
                var type = _.get(tag, ['refs', 'upload', 'files', 0, 'type']);
                if (_.isUndefined(type)) { return true; }
                if (!_.includes(tag.opts.validate_type, type)) { return message; }
                return true;
            },
            max_size: function (tag) {
                var message = gettext('Please choose a smaller file');
                var size = _.get(tag, ['refs', 'upload', 'files', 0, 'size']);
                if (_.isUndefined(size)) { return true; }
                if (tag.opts.validate_max_size < size) { return message; }
                return true;
            },
            not_null: function (tag) {
                var message = gettext('Required');
                var files = _.get(tag, ['refs', 'upload', 'files']);
                var condition = _.isUndefined(files) ? true : files.length > 0;
                return !condition ? message : true;
            }
        }
    }
};

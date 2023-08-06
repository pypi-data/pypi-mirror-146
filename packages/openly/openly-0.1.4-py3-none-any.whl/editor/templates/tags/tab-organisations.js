/* {% load i18n %} */
/* {% load ifsetting %} */
/* global stores */
/* eslint no-underscore-dangle: 0 */
/* eslint no-param-reassign: ["error", { "props": false }] */
/* {% trans 'IGA' as label %} */
/* {% blocktrans asvar placeholder %}Select the {{label}}{% endblocktrans %} */

var tag = this;
var opts = tag.opts;
tag.show_funding = opts.show_funding;
tag.show_extending = opts.show_extending;

tag.mixin('SerializerMixin');
tag.mixin('TabMixin');
tag.mixin('ValidationMixin');
// TODO: Find out why this is required to make the page load correctly
tag.on('before-mount', function () { tag.validated = undefined; });

tag.classes = {
    dropdownselect: {
        dropdown: 'col-xs-9'
    }
};

tag.template = tag.store.activityorganisation_template;

tag.save_activityorganisations = function () {
    var xhr;
    var data = {};
    window.banner_message.show(gettext('Saving'), 'info');
    _.set(data, tag.path.replace('activity.', ''), tag.clean_data());
    xhr = tag.put(data, { update_done: 'reload_' + tag.path });
    xhr.done(function (returned_data) {
        window.banner_message.show(gettext('Saved'), 'success');
        tag.validated = true;
        if (tag.isMounted) { tag.update(); }
        RiotControl.trigger('update_activity_completion', returned_data);
    });
    return xhr;
};
tag.save = tag.save_activityorganisations;

tag.clean_data = function () {
    var current_organisations = _.cloneDeep(_(tag.store).get(tag.opts.path));
    _(tag.store._delete_paths).each(function (path_to_delete) {
        _.unset(current_organisations, path_to_delete.replace(tag.path, ''));
    });
    // Remove any "undefined" from the array
    current_organisations = _.remove(current_organisations, function (organisation) {
        return organisation !== undefined;
    });
    current_organisations = _.remove(current_organisations, function (organisation) {
        return organisation.organisation.code !== undefined && organisation.organisation.code !== '';
    });
    // Bug in serializer when "name" is required
    _.each(current_organisations, function (organisation) {
        organisation.name = organisation.name || organisation.organisation.code || 'Not named';
    });

    return current_organisations;
};

tag.has_changed = function () {
    var sort_organisation_and_role = function (array) {
        return _(array).map(function (organisation) {
            return ([organisation.organisation.code, organisation.role.code]);
        })
            .sortBy()
            .value();
    };
    var initial = _(tag.store).get(tag.opts.path.replace(tag.store.el, '_initial'));
    var clean_data = tag.clean_data();
    return !_(sort_organisation_and_role(initial)).isEqual(_(sort_organisation_and_role(clean_data)));
};

function onPathUpdated(i) {
    var organisation_name;
    var new_name_path;
    var wants_name;
    var has_name;
    /* Special handler to make data match the specified serializer format */
    /* Copy the organisation "name" from the Organisation model to th ActivityParticipatingOrganisation model */
    if (i.path.length > tag.path.length && _.startsWith(i.path, tag.path)) {
        wants_name = tag.bystring(i.path + '.name');
        new_name_path = _(i.path).replace('.organisation', '.name');
        has_name = tag.bystring(new_name_path);
        if (has_name === wants_name) { return; }
        organisation_name = tag.bystring(i.path).name;
        tag.bystring(new_name_path, { data: organisation_name });
        _.unset(tag.store, i.path + '.name');
        tag.update();
    }
}
function load_returned_activity_data(data, returned_data) {
    /* Trigger a reload of all activity data */
    tag.store.load(returned_data);
}

tag.on('mount', function load_riotcontrol_methods() {
    RiotControl.on('path_updated', onPathUpdated);
    RiotControl.on('reload_' + tag.path, load_returned_activity_data);
    tag.add_empty_rows_for_missing_roles();
});

tag.on('unmount', function () {
    RiotControl.off('path_updated', onPathUpdated);
    RiotControl.off('reload_' + tag.path, load_returned_activity_data);
});

tag.on('update', function () {
    tag.data = tag.data || tag.bystring(tag.absolute_path(tag.path), {});
    tag.add_empty_rows_for_missing_roles();
    tag.categories = {
        Funding: tag.filter_role_code('Funding'),
        Accountable: tag.filter_role_code('Accountable'),
        Implementing: tag.filter_role_code('Implementing'),
        Extending: tag.filter_role_code('Extending')
    };

    tag.disabled_choices = {
        Funding: tag.chosen('Funding'),
        Accountable: tag.chosen('Accountable'),
        Implementing: tag.chosen('Implementing'),
        Extending: tag.chosen('Extending')
    };
});

tag.chosen = function (type) {
    return _(tag.data).filter(function (i, index) {
        var item_path = tag.path + '[' + index + ']';
        var del = _.indexOf(tag.store._delete_paths, item_path) > -1;
        return (i.role.code === type && !del);
    }).map(function (i) {
        return i.organisation.code;
    }).value();
};

tag.is_deleted = function (org) {
    var index = _.indexOf(tag.data, org);
    var org_path;
    if (index !== -1) {
        org_path = tag.path + '[' + index + ']'; // like 'budget_set[0]'
        return _.indexOf(tag.store._delete_paths, org_path) > -1;
    }
    return false;
};

tag.is_created = function (org) {
    var i = _.indexOf(tag.data, org);
    var org_path;
    if (i !== -1) {
        org_path = tag.path + '[' + i + ']'; // like 'budget_set[0]'
        return _.indexOf(tag.store._create_paths, org_path) > -1;
    }
    return false;
};

tag.is_updated = function (org) {
    var index = _.indexOf(tag.data, org);
    var org_path = tag.path + '[' + index + '].organisation';
    if (index !== -1) {
        return _.indexOf(tag.store._update_paths, org_path) > -1;
    }
    return false;
};

tag.delete_organisation = function () {
    var delete_tag = this;
    var code = _.get(delete_tag, 'organisation.organisation.code');
    var role_code = _.get(delete_tag, 'organisation.role.code');
    var search = {
        organisation: { code: code },
        role: { code: role_code }
    };
    var initial = delete_tag.store._initial.participating_organisations;
    var current = delete_tag.store.activity.participating_organisations;

    function inner_delete_function() {
        _.remove(current, search);
        delete_tag.parent.save_activityorganisations();
        tag.store.trigger('path_updated', { store: delete_tag.store, path: delete_tag.absolute_path() + '[0].organisation' });
    }

    if (code === null || code === undefined) { return; }

    if (!_.find(initial, search)) {
        inner_delete_function();
        return;
    }

    delete_tag.store.trigger('confirm-delete', { confirm: inner_delete_function, content: delete_tag.organisation.name + ' will be renoved from this activity permanently.' });
};

tag.add_partner = function (type) {
    var partner;
    partner = _(tag.template).cloneDeep();
    _.set(partner, 'role.code', type);
    stores.activityStore.activity.participating_organisations.push(partner);
    tag.store._create_paths.push(tag.absolute_path() + '[' + tag.data.indexOf(partner) + ']');
};

tag.add_partner_accountable = function () {
    tag.add_partner('Accountable');
};
tag.add_partner_implementing = function () {
    tag.add_partner('Implementing');
};
tag.add_partner_extending = function () {
    tag.add_partner('Extending');
};
tag.add_partner_funding = function () {
    tag.add_partner('Funding');
};

tag.filter_role_code = function (role) {
    var data = tag.bystring(tag.absolute_path(tag.path), {});
    return _.filter(data, function (i, index) {
        var deleted = _.indexOf(tag.store._delete_paths, tag.absolute_path(tag.path) + '[' + index + ']') !== -1;
        return i.role.code === role && !deleted;
    });
};


tag.add_empty_rows_for_missing_roles = function () {
    ['Extending', 'Implementing', 'Accountable', 'Funding'].forEach(function (organisation_role) {
        var organisations = _.filter(tag.data, function (org) { return org.role.code === organisation_role; });
        var add_function_name;
        if (organisations.length === 0) {
            add_function_name = 'add_partner_' + _.lowerCase(organisation_role);
            tag[add_function_name]();
        }
    });
};


tag.discard = function () {
    tag.store.activity.participating_organisations = _.cloneDeep(tag.store._initial.participating_organisations);
    tag.update();
    _.invokeMap(tag.list_child_tags(), 'update');
};

// {% ifsetting EDITOR_HAS_IGA %}
(function IGA_initialise(theTag) {
    /*
    Intended for Projectbank which wants a simpler single-organisation
    picker but similar UI
    */
    var choices = tag.store.choices;
    function getIndex() {
        var orgs = _(theTag.store.activity.participating_organisations);
        var replaceOrg = orgs.find({ role: { code: 'Accountable' } });
        var indexOfOrg = orgs.indexOf(replaceOrg);
        return indexOfOrg;
    }

    theTag.iga_organisation_index = function () {
        var i = getIndex();
        if (i === -1) {
            theTag.add_partner_accountable();
            i = getIndex();
        }
        return i;
    };

    theTag.on('before-mount', function () {
        /* Save the results of our nesting so we don't repeat later */

        if (!theTag.store.choices.nested_organisation) {
            theTag.governmentChoices = {
                text: gettext('Region/State Governments'),
                value: '',
                choices: _(choices.organisation).filter(function (o) {
                    return _.indexOf(choices.organisation_region_govt, o[0]) !== -1;
                }).map(function (o) {
                    return { text: o[1], value: o[0] };
                }).value()
            };

            theTag.choices = _.concat(
                _.map(choices.organisation, function (o) { return { text: o[1], value: o[0] }; }),
                theTag.governmentChoices
            );
            theTag.lookup = _.keyBy(theTag.choices, 'value');
            _.each(choices.organisation_parent.filter(function (o) { return o[1]; }), function (op) {
                var parent = theTag.lookup[op[1]];
                var child = theTag.lookup[op[0]];
                if (!parent.choices) { parent.choices = [parent]; }
                /* Append the parent's acronym to the choice (projectbank #195) */
                child.text = child.text + ' (' + parent.value + ')'
                parent.choices.push(child);
            });
            theTag.store.choices.nested_organisation = theTag.choices;
        }
        /* Show only those with child ministries */
        theTag.choices = _.filter(theTag.store.choices.nested_organisation, function (o) { return !_.isUndefined(o.choices); });
    });
}(tag));

tag.select2_opts_iga = { placeholder: '{{placeholder}}' };
// {% endifsetting %}

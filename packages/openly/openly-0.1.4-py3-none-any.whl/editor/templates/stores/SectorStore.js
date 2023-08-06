/* global _ riot */
/* exported SectorStore */

function SectorStore(activity, choices) {
    var store = this;
    riot.observable(store);
    // property set up unrelated to the activity data
    store.group_names = ['sectors', 'sector_working_groups', 'policy_markers'];
    store.load_data = load_data;
    store.add_row = add_row;
    store._delete = [];  // array of elements to be deleted

    // property set up that use the activity data
    store.activity_id = activity.id;
    store.choices = choices;
    massage_choices(store.choices);
    store.duplicate_sector_names = get_duplicate_sector_names(store.choices.dac_5s);
    store.load_data(activity);

    store.on('sectors_update_done', function (activity_data) {
        store.load_data(activity_data);
    });

    store.urls = function () {
        return {
            update: '{% url "activity_update_general" "XXXXX" %}'.replace('XXXXX', activity.id)
        };
    };

    // an error occurs when this is not set
    store.fieldvalidation = {
        '.significance': ''
    };

    function load_data(activity_data) {
        /** Set the `sectors`, `sector_working_groups` and `policy_markers` keys on the sector.
         * Also stores the initial activity data under `_initial`.
         */
        store.group_names.forEach(function (group_name) {
            store[group_name] = _.cloneDeep(activity_data[group_name]);
        });
        store._initial = _.cloneDeep(_.pick(store, store.group_names));
        store._initial_ids = _.chain(store._initial).values().flatten().map(function (sector) { return sector.id; }).value();
        store.trigger('sectors_updated');

        add_empty_rows_if_necessary();
    }

    /* BEGIN: initialization functions. */

    function massage_choices(choices) {
        /** Make the sector choices suitable for consumption by the field-choice tags.
         *
         * For all 3 types of sectors, we pass the array of choices to the field-choice tag,
         * as opposed to other parts of the editor where the field-choices tag massages the data itself.
         * That is because the choices are dynamically generated to guarantee uniqueness.
         */
        choices.dac_3s = group_dac5s_under_dac3s(choices.dac_3s, choices.dac_5s);

        ['sector_working_group', 'policy_marker'].forEach(function (group_name) {
            choices[group_name] = _.map(choices[group_name], function (choice) {
                return { 'value': choice[0], 'text': choice[1] };
            });
        });
        // policy marker is not a select2, so add a choice as placeholder
        choices.policy_marker.splice(0, 0, { value: null, text: '------' });
    }

    function group_dac5s_under_dac3s(dac_3s, dac_5s) {
        /** Iterate over the dac5 sectors, and puts in a `choice` property of their respective dac3,
         * so that the dac_3s can be fed to the field-choice tag.
         */
        var dac3_index;

        // sort dac_3s and dac_5s by category_id
        dac_3s = _.sortBy(dac_3s, 0);
        dac_5s.map(function(dac5) {dac5.category_id = Number(String(dac5[0]).slice(0, 3));});
        dac_5s = _.sortBy(dac_5s, 'category_id');

        // add the dac_5s under each dac3.choices
        dac_3s = _.map(dac_3s, function (dac3) {
            return {
                value: dac3[0],
                text: dac3[1],
                choices: [{ value: dac3[0], text: dac3[1] + ' [unspecified]' }]
            };
        });
        dac3_index = 0;
        dac_5s.forEach(function (dac5) {
            while (dac5.category_id !== dac_3s[dac3_index].choices[0].value) {
                dac3_index += 1;
            }
            dac_3s[dac3_index].choices.push({
                value: dac5[0],
                text: dac5[1]
            });
        });

        return dac_3s;
    }

    /* END: initialization functions. */

    function add_empty_rows_if_necessary() {
        /* If there are no rows in one of the 3 groups, then add an empty one ready to be filled out. */
        store.group_names.forEach(function (group_name) {
            if (store[group_name].length === 0) {
                store.add_row(group_name);
            }
        });
    }

    function get_duplicate_sector_names(dac_5s) {
        var all_names = _.map(dac_5s, function (dac5) { return dac5[1]; });
        var sorted_names = _.sortBy(all_names);
        return _.filter(sorted_names, function (name, index, iteratee) { return _.includes(iteratee, name, index + 1); });
    }

    function add_row(group_name) {
        if (group_name === 'sectors') {
            store.sectors.push({ 'sector': {'code': null}, 'percentage': '0.00' });
        } else if (group_name === 'sector_working_groups') {
            store.sector_working_groups.push({'sector_working_group': {'code': null}, 'percentage': '0.00'});
        } else if (group_name === 'policy_markers') {
            store.policy_markers.push({'policy_marker': {'code': null}, 'significance': {'code': null}});
        } else {
            throw 'The SectorStore does not know how to add a ' + group_name;
        }
    }

}

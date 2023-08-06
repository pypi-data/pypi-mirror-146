/* global _ RiotControl */
/* exported SectorMixin */

function SectorMixin() {
    this.init = function () {
        var tag = this;
        tag.on('mount', function () {
            $('[rel="popover"]', tag.root).popover();
        });
    };

    this.delete_sector = function () {
        var tag = this;
        var sector = tag.opts.sector || tag.opts.policy_marker;
        var store = tag.store;
        // // if the sector hasn't been pushed to the API, delete it right away
        // if (store._initial_ids.indexOf(sector.id) === -1) {
        //     store.group_names.forEach(function (group_name) {
        //         _.pull(store[group_name], sector);
        //     });
        //     tag.store.trigger('path_updated', { store: tag.store, path: tag.path + '.percentage' });
        //     return;
        // }

        function inner_delete_function() {
            store.group_names.forEach(function (group_name) {
                var pulled = _.pull(store[group_name], sector);
                if (pulled !== []) {
                    tag.store.trigger('path_updated', { store: tag.store, path: tag.path + '.percentage' });
                }
            });
            if (_.has(sector, 'id')) {
                tag.parent.save();
            }
        }
        if (!_.has(sector, 'id')) {
            setTimeout(inner_delete_function(),100);
        } else {
            tag.store.trigger('confirm-delete', { confirm: inner_delete_function, content: 'This sector will be deleted permanently.' });
        }
    };

    this.get_relevant_choices = function (sector_property_name, sortby) {
        /** Return a choice list that exludes sectors selected in other dropdowns. */
        var tag = this;
        var store_property_name = sector_property_name + 's';
        var selected_sector = tag.opts.sector || tag.opts.policy_marker;
        var store = tag.store;
        var other_selected_sectors_ids = _.map(store[store_property_name], function (sector) {
            return Number(sector[sector_property_name].code);
        });
        var cloned_choices;
        var duplicate_sector_names = _.clone(store.duplicate_sector_names);
        var selected_sector_code = Number(selected_sector[sector_property_name].code);
        _.pull(other_selected_sectors_ids, selected_sector_code);

        // separate logic for sector than SWGs and policy markers because we have optgroups in the select tag
        if (sector_property_name === 'sector') {
            // copy each reference to the dac3s
            cloned_choices = _(store.choices.dac_3s).map(_.clone).value();
            // copy the choices array in each dac3
            cloned_choices.forEach(function (dac3) {
                dac3.choices = _.clone(dac3.choices);
                _.remove(dac3.choices, function (dac5) {
                    // remove sectors selected in other dropdowns
                    if (other_selected_sectors_ids.indexOf(dac5.value) > -1) {
                        return true;
                    }
                    // remove duplicates, but only if they are not selected
                    if (duplicate_sector_names.indexOf(dac5.text) > -1 && dac5.value !== selected_sector_code) {
                        _.pull(duplicate_sector_names, dac5.text);
                        return true;
                    }
                    // remove [ unspecified ] dac3 choice only if not selected
                    if (dac5.value === dac3.value && dac5.value !== selected_sector_code) {
                        return true;
                    }
                    return false;
                });
            });
        } else {
            cloned_choices = _.clone(store.choices[sector_property_name]);
            _.remove(cloned_choices, function (choice) {
                return (other_selected_sectors_ids.indexOf(choice.value) > -1);
            });
        }
        if (!_.isUndefined(sortby)) { cloned_choices = _.sortBy(cloned_choices, sortby); }
        return cloned_choices;
    };
}

{% load static %}

// Returns an object whose keys are the "intersection" of the truthy keys in
// objA and objB
function intersection(objA, objB) {
    var obj = new Object()
    _.concat(Object.keys(objA), Object.keys(objB)).forEach(function(k) {
    if (!!objA[k] && !!objB[k]) obj[k] = true;
    });
    return Object.keys(obj);
}

var tag = this;
tag.filter_displayed = false;
tag.store = opts.store;
tag.locations = opts.locations;
tag.location_descendants = {};
tag.locations.forEach(function(l) {
    tag.location_descendants[l.code] = _.zipObject(l.descendants, l.descendants.map(function() { return true; }));
});
tag.filter_locations = [];
tag.search_locations = [];
tag.sectors = opts.sectors;
tag.sectors.splice(0, 0, {value: -1, name: '----'});
tag.statuses = opts.statuses;
tag.filtered_statuses = {};
tag.statuses.forEach(function(s) { tag.filtered_statuses[s.value] = false; });
tag.active_status_filters = tag.statuses.filter(function(s) { return tag.filtered_statuses[s.value]; });

// Load partners from store and populate logo with default image if not present
tag.partners = tag.store[tag.store.el];
tag.partners.sort(function(o1, o2) { return o1.name.localeCompare(o2.name); });
tag.gos = tag.ngos = [];
tag.org_name_filter = '';
tag.sector_filter = -1;
tag.location_filter = '';
tag.location_code = -1;

tag.on('mount', function() {
    tag.update_displayed_partners();
    $('[data-toggle="popover"]').popover();
});

toggle_filter(e) {
    $('#partner_filter').toggleClass('collapsed');
    $('#partner_cards_section').toggleClass('partner-cards-wide');
    tag.filter_displayed = !tag.filter_displayed;
}

tag.update_displayed_partners = function() {
    // Uncomment to display governmental organisations
    var status_filter_inactive = (tag.active_status_filters.length == 0);
    tag.gos = tag.partners.filter(function(p) {
        return (
            p.type == 10
            && p.name.toUpperCase().indexOf(tag.org_name_filter.toUpperCase()) != -1
            && p.activities.findIndex(function(a) {
                return (
                    (tag.sector_filter == -1 || a.sectors.indexOf(tag.sector_filter) != -1)
                    && (tag.location_code == -1 || tag.location_filter_codes.intersection(new Set(a.locations)).size > 0)
                    && (status_filter_inactive || tag.filtered_statuses[a.status])
                );
            }) != -1
        );
    });

    tag.ngos = tag.partners.filter(function(p) {
        return (
            p.type != 10
            && (p.name.toUpperCase().indexOf(tag.org_name_filter.toUpperCase()) != -1
                || p.code.toUpperCase().indexOf(tag.org_name_filter.toUpperCase()) != -1
                || p.abbrev.toUpperCase().indexOf(tag.org_name_filter.toUpperCase()) != -1)
            && ((tag.sector_filter == -1 && tag.location_code == -1 && status_filter_inactive)
                || p.activities.findIndex(function(a) {
                return ((tag.sector_filter == -1 || a.sectors.indexOf(tag.sector_filter) != -1)
                    && (tag.location_code == -1 || !_.isEmpty(intersection(tag.location_filter_codes, _.zipObject(a.locations, a.locations.map(function() { return true; })))))
                    && (status_filter_inactive || tag.filtered_statuses[a.status])
                   );
            }) != -1)
        );
    });
    tag.num_matches = tag.gos.length + tag.ngos.length;
    tag.update();
}

org_name_keyup(e) {
    tag.org_name_filter = e.target.value;
    tag.update_displayed_partners();
}

clear_org_name_filter() {
    tag.org_name_filter = '';
    tag.update_displayed_partners();
}

filter_by_sector(e) {
    tag.sector_filter = Number(e.target.value);
    tag.update_displayed_partners();
}

clear_sector_filter() {
    tag.sector_filter = -1;
    tag.update_displayed_partners();
}

location_filter_keyup(e) {
    tag.location_filter = e.target.value;
    if (tag.location_filter.length >= 3) {
        tag.filter_locations = tag.locations.filter(function(l) {
            return l.name.toUpperCase().indexOf(tag.location_filter.toUpperCase()) != -1;
        });
    } else {
        tag.filter_locations = [];
    }
    tag.update_displayed_partners();
}

clear_location_filter() {
    tag.location_filter = '';
    tag.location_code = -1;
    tag.location_filter_codes = undefined;
    tag.filter_locations = [];
    tag.update_displayed_partners();
}

select_location(e) {
    tag.location_filter = e.target.name;
    tag.location_code = e.target.value;
    tag.location_filter_codes = tag.location_descendants[e.target.value];
    tag.filter_locations = [];
    tag.update_displayed_partners();
}

toggle_status(e) {
    tag.filtered_statuses[e.target.value] = !tag.filtered_statuses[e.target.value];
    tag.active_status_filters = tag.statuses.filter(function(s) { return tag.filtered_statuses[s.value]; });
    tag.update_displayed_partners();
}

clear_status_filters() {
    tag.statuses.forEach(function(s) { tag.filtered_statuses[s.value] = false; });
    tag.active_status_filters = tag.statuses.filter(function(s) { return tag.filtered_statuses[s.value]; });
    tag.update_displayed_partners();
}

clear_filters() {
    tag.clear_org_name_filter();
    tag.clear_location_filter();
    tag.clear_sector_filter();
    tag.clear_status_filters();
}

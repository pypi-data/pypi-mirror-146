/* eslint-disable strict */
/* exported activityStore */

/* This is mainly a framework to provide
efficient reliable filtering via riotjs trigger events */

function activityStore(opts) {
    var store = this;
    riot.observable(store);
    store.on('init', function () {
        store.activities = JSON.parse(document.getElementById('activities-data').textContent);
        store.set_pagination(opts);
        store.lookups = JSON.parse(document.getElementById('lookups-data').textContent);
        store.lookups.government_agency = [];
        store.activities.forEach(function (activity) {
            /* create a unique list of government agencies for lookup */
            if (store.lookups.government_agency.indexOf(activity.government_agency) === -1) { store.lookups.government_agency.push(activity.government_agency); }
            activity.show = true;
            activity.sort_budget = _.toNumber(activity.total_budget_raw);
        });
        store.trigger('activities_ready');
        // Filtering - listen for requests from project-list-filter

        store.search_text = '';
        store.filters = [
            {
                id: 'IGA',
                name: 'Implementing Government Agency',
                options: store.lookups.government_agency.map(function (o) { return { display: o, value: o }; }),
                visible: true,
                field: 'government_agency',
                filter_function: 'includes'
            },
            {
                id: 'funding_sources',
                name: 'Financing Type',
                options: store.lookups.funding_sources.map(function (o) { return { display: o.name, value: o.code }; }),
                visible: true,
                field: 'funding_sources',
                filter_function: 'intersects'
            },
            {
                id: 'status',
                name: 'Status',
                options: store.lookups.statuses.map(function (o) { return { display: o.name, value: o.name }; }),
                visible: true,
                field: 'status',
                filter_function: 'includes'
            }
        ];
        store.trigger('clear_filters');
        store.trigger('filters_ready');
    });

    /* Pagination functions */
    store.set_pagination = function (function_opts) {
        var combined_opts = _.defaults(function_opts, opts);
        var current_pagination = store.pagination || {};
        var pagination = {
            page: current_pagination.page || 1,
            per_page: combined_opts && combined_opts.per_page ? combined_opts.per_page : current_pagination.per_page || 50,
            total_count: _(store.activities).size(),
            count: _(store.activities).filter({ show: true }).size()
        };
        pagination.num_pages = _.ceil(pagination.count / pagination.per_page);
        pagination.start_showing_at = (pagination.page - 1) * pagination.per_page;
        pagination.end_showing_at = pagination.start_showing_at + pagination.per_page;
        store.pagination = pagination;
    };

    store.apply_pagination = function () {
        /* Make "paged" true only for activities which fall within this page */
        store.set_pagination();
        _(store.activities).each(function (a) { a.paged = false; });
        _(store.activities).filter({ show: true }).slice(store.pagination.start_showing_at, store.pagination.end_showing_at).each(function (a) {
            a.paged = true;
        });
        store.trigger('applied_pagination');
    };

    store.on('paginate', function (page) {
        store.pagination.page = page;
        store.trigger('apply_filters');
    });

    /* Show or hide different filtering options */
    store.apply_filter_to_activities = function (filter) {
        var selected = filter.selected;
        var func = filter.filter_function;

        if (!filter.visible || !selected.length) { return; }

        store.activities.forEach(function (a) {
            var test_value = a[filter.field];
            /* already hidden by a previous filter */
            if (!a.show) {
                /* do nothing */
            } else if (func === 'intersects') {
                a.show = _.intersection(selected, test_value).length !== 0;
            } else if (func === 'includes') {
                a.show = _.includes(selected, test_value);
            } /* specify other comparison functions here */
        });
    };

    store.apply_text_filter = function (text /* str */, properties /* array of str fieldnames */) {
        /* filter by a number of fields for a text match */
        store.activities.forEach(function (a) {
            var show = false;
            if (!a.show) { return; }
            if (text.length === 0) { return; }
            properties.forEach(function (property) {
                if (_.lowerCase(a[property]).indexOf(text) > -1) {
                    show = true;
                }
            });
            a.show = show;
        });
    };

    store.reset_filtering = function () {
        store.activities.forEach(function (a) { a.show = true; });
    };

    store.get_filter = function (id) {
        return _.find(store.filters, { id: id });
    };

    store.get_selected = function (id) {
        return store.get_filter(id).selected;
    };

    store.on('clear_filters', function () {
        store.filters.forEach(function (filter) { filter.selected = []; });
        store.trigger('apply_filters');
    });

    store.on('toggle_filter', function (id) {
        var filter = _.find(store.filters, { id: id });
        filter.visible = !filter.visible;
        store.trigger('apply_filters');
    });

    /* Change the 'search text' to filter options by */
    store.on('search_text', function (search_text) {
        store.search_text = search_text;
        store.trigger('apply_filters');
    });

    store.on('set_filters', function (filter_id, selected) {
        store.get_filter(filter_id).selected = selected;
        /* Triggering the pagination will also trigger "apply_filters" */
        store.trigger('paginate', 1);
    });

    store.on('apply_filters', function () {
        /* Run through active filters and hide things which don't match */
        store.reset_filtering();
        store.apply_filter_to_activities(_.find(store.filters, { id: 'IGA' }), 'government_agency');
        store.apply_filter_to_activities(_.find(store.filters, { id: 'funding_sources' }), 'funding_sources');
        store.apply_filter_to_activities(_.find(store.filters, { id: 'status' }), 'status');
        store.apply_text_filter(store.search_text, ['title', 'government_agency']);
        store.apply_pagination();
        store.trigger('activities_filtered');
        store.trigger('filters_updated');
    });

    store.on('sort', function (sort_key) {
        var old_sort_key = store.sort_key;
        store.sort_key = sort_key;

        if (old_sort_key === store.sort_key) {
            store.order = store.order === 'desc' ? 'asc' : 'desc';
        } else {
            store.order = 'asc';
        }
        store.activities = _.orderBy(store.activities, store.sort_key, store.order);
        /* On sorting, return to page 1 */
        store.trigger('paginate', 1);
        store.trigger('objects_sorted', store.sort_key, store.order);
    });
}

// {% load i18n %}
// {% load static %}
// {% get_current_language as LANGUAGE_CODE %}

var tag = this;
var language = "{{ LANGUAGE_CODE }}";
var maxDescriptionLength = 600;

tag.on('mount', function() {
    tag.store = tag.opts.store;
    tag.language = language;
    tag.orderBy = [
        {field: 'title asc', label: 'Title'},
        {field: 'start_actual desc', label: 'Start date (latest date first)'},
        {field: 'start_actual asc', label: 'Start date (earliest date first)'},
        {field:'commitment_total asc', label:'Total commitment (lowest to highest)'},
        {field:'commitment_total desc', label: 'Total commitment (highest to lowest)'},
        {field:'completion asc', label: 'Data completion (lowest to highest)'},
        {field:'completion desc', label: 'Data completions (highest to lowest)'},
    ],
    tag.update({loading:true})
    tag.load_data(tag.store[opts.store.el]);
    tag.update();
});

opts.store.on('organisation_activities_set_requested', function() {
    tag.update({loading: true});
    console.log('loading')
})

opts.store.on('organisation_activities_set_restored', function() {
    tag.load_data(tag.store[tag.store.el]);
    tag.update({loading: false});
    opts.store.trigger('organisation_activities_set_ready')
})

/**
 * Pull the correct field values based on language from the activity (e.g. title) and
 * set character limits
 * where appropriate.
 */
function load_data(data) {
    var urls = {
        profile: "{% url 'activity_profile' 'XXXXXX' %}",
        edit: "{% url 'edit_activity' 'XXXXXX' %}",
        org: "{% url 'organisation_profile' 'XXXXXX' %}",
    }
    tag.all_activities = _.map(data, function(a){
        var activity = _.clone(a)
        var modified_date = moment(a['date_modified'])
        var created_date = moment(a['date_created'])

        if (activity.start_actual) {
            activity.duration_start = moment(activity.start_actual).format('MMM YYYY');
        } else {
            activity.duration_start = moment(activity.start_planned).format('MMM YYYY');
        }

        if (activity.end_actual) {
            activity.duration_end = moment(activity.end_actual).format('MMM YYYY');
        } else if (activity.end_planned) {
            activity.duration_end = moment(activity.end_planned).format('MMM YYYY');
        } else {
            activity.duration_end = "None";
        }

        activity.date_modified = modified_date.isValid() ? modified_date.format('DD MMM YYYY') : false;
        activity.date_created = created_date.isValid() ? created_date.format('DD MMM YYYY') : false;
        activity.title = a['title_'+tag.language] ||  a['title_'+'en'] ||  a['title'] || 'Untitled'
        activity.description = a['description_'+tag.language] ||  a['description_'+'en'] ||  a['description'] || 'No description'
        activity.sectors = _(a.sector_category_names).join(', ');
        activity.implementing_partners = tag.store.implementing_partners[activity.pk];
        if (activity.description.length > maxDescriptionLength) {
            activity.description = activity.description.slice(0, maxDescriptionLength) + '...';
        }
        activity.status = a.activity_status;
        if (activity.status == 2) {
            activity.icon = "{% static 'img/activity_implementing.svg' %}";
        } else if (activity.status == 3) {
            activity.icon = "{% static 'img/activity_completed.svg' %}";
        } else {
            activity.icon = "{% static 'img/activity_pipeline.svg' %}";
        }
        activity.profile = urls.profile.replace('XXXXXX', a.pk)
        activity.edit = urls.edit.replace('XXXXXX', a.pk)
        activity.reporting_org_url = urls.org.replace('XXXXXX', a.reporting_organisation__pk)
        activity.commitment_total = _.toNumber(a.commitment_total);
        activity.commitment_total_display = accounting.compactFormatMoney(activity.commitment_total)
        return activity;
    });

    tag.onFilterChange();
}

tag.load_data = load_data;

tag.onFilterChange = function(){
    /* Array of selected 'status' checkboxes */
    function getFilters(){
        var filters = {};
        /* Set some sensible defaults */
        filters.page = _.get(tag, ['filters','page'], 1)
        filters.pageSize = _.get(tag, ['filters','pageSize'], 10);
        filters.showAll = _.get(tag, ['filters','showAll'], false);

        if (_.keys(tag.refs).length == 0){
            /* Filter form is not yet loaded; set the initial values */
            filters.status = [2] /* Magic number for 'implementation' */
            filters.orderBy = 'commitment_total desc' /* Initial order of the list */
            filters.role = []
            filters.organisation = [opts.organisation]
            filters.iati_sync = []

        } else {
            filters.organisation = _(tag.refs.filterFormReporting).filter('selected').map('value').value()
            if (filters.organisation.length == 0) {filters.organisation = ['__all__']}
            filters.status = _(tag.refs.filterFormStatus).filter('selected').map('value').map(_.toInteger).value()
            filters.role = _(tag.refs.filterFormRole).filter('selected').map('value').value()
            filters.orderBy = _(tag.refs.orderBy).filter('selected').map('value').value()
            filters.iati_sync = _(tag.refs.filterFormIati).filter('selected').map('value').value()
        }

        // Chain filters
        return filters;
    }
    var filters = getFilters();
    var activities = _(tag.all_activities);

    if (filters.status.length > 0){activities = activities.filter(function(a){return _.includes(filters.status, a.status)})}
    if (!_.includes(filters.organisation, '__all__')){ activities = activities.filter(function(a){return a.reporting_organisation__name == tag.opts.organisation_name})}
    if (!_.includes(filters.role, '__all__')) {
        if (filters.role.length == 0) {
            activities = activities.filter(function(a) {return a.reporting_organisation__name == tag.opts.organisation_name})
        } else {
            activities = activities.filter(function(a){return _.includes(filters.role, a.role)})
        }
    }
    if (_.includes(filters.iati_sync, 'synced')){
        activities = activities.filter(function(a){return !_.isNull(a.iati_sync)})
    } else if (_.includes(filters.iati_sync, 'notsynced')) {
        activities = activities.filter(function(a){return _.isNull(a.iati_sync)})
    }
    // If ordered

    if (filters.orderBy.length > 0){
        activities = activities.orderBy(
            _.split(filters.orderBy, ' ')[0],
            _.split(filters.orderBy, ' ')[1]
        )
    }

    // Settings for pagination
    var activityList = activities.value();
    var activityCount = activityList.length
    var sliceStart = 0
    var sliceEnd = 0
    var slicedActivityList = []
    var pagination = {}

    // Update the summary numbers above the Activities List
    if (activityCount == 0) {
        tag.byStatus = 0;
        tag.byStatusCounts = 0;
        tag.byStatusCountLabels = 0;
    } else {
        tag.byStatus = _.groupBy(activityList, 'status');
        tag.byStatusCounts = _.mapValues(tag.byStatus, 'length');
        tag.byStatusCountLabels = _.mapKeys(tag.byStatusCounts, function(k, s){return _(tag.store.choices.status).find({pk: _.toInteger(s)}).name});
    }

    if (!filters.showAll){
        sliceStart = (filters.page-1) * filters.pageSize
        if (sliceStart > activityCount){
            sliceStart = 0
            filters.page = 1
        }
        sliceEnd = filters.page * filters.pageSize;
        slicedActivityList = activityList.slice(sliceStart, sliceEnd);
    } else {
        sliceStart = undefined
        sliceEnd = undefined
        slicedActivityList = activityList
    }

    pagination = {itemCount: activityCount, page: filters.page, pageSize: filters.pageSize, showAll: filters.showAll};
    tag.update({
        filters: filters,
        activities:slicedActivityList,
        pagination: pagination
    })
}

tag.on('paginationChangeSignal', function(opts){
    /* opts
    page: Page to display
    pageSize: Items per page to display
    showAll: Turn off pagination
    */
    tag.filters = tag.filters || {};
    tag.pagination = tag.pagination || {};
    _.extend(tag.filters, opts);
    tag.onFilterChange();
    tag.update();
})

{% load i18n %}

var tag = this;
tag.activity = opts.activity;
if (tag.activity.date_modified != null) {
    var modified_date = moment(opts.activity['date_modified']);
    tag.activity.date_modified = modified_date.isValid() ? modified_date.format('DD MMM YYYY') : false;
}
if (tag.activity.date_created != null) {
    var created_date = moment(opts.activity['date_created']);
    tag.activity.date_created = created_date.isValid() ? created_date.format('DD MMM YYYY') : false;
}
tag.organisation_profile = opts.organisation_profile;
tag.partners = opts.partners;
tag.mounted = false;

{% get_current_language as LANGUAGE_CODE %}
tag.language = "{{ LANGUAGE_CODE }}";

tag.on('mount', function() {
    tag.mounted = true;
    tag.set_title();
    tag.set_dates();
    tag.set_descriptions();

    tag.update();
});

tag.set_title = function() {
    tag.activity.title_set.forEach(function(t, i) {
        if (t.language == tag.language) {
            tag.title = t.title;
            return;
        } else if (i == 0) {
            tag.title = t.title;
        }
    });
}

tag.set_dates = function() {
    // Activity contains an array of dates [planned start, actual start, planned end, actual end].
    // We prefer the actual date if it exists for both start/end
    tag.start_date = (tag.activity.activity_dates[1].iso_date ? tag.activity.activity_dates[1] : tag.activity.activity_dates[0]);
    tag.end_date = (tag.activity.activity_dates[3].iso_date ? tag.activity.activity_dates[3] : tag.activity.activity_dates[2]);
}

tag.set_descriptions = function() {
    // TODO: How she would pass description type -> description code encoding
    var ds = _.filter(tag.activity.descriptions, function(d){return d.description && d.description != '' && !_.isNull(d.description) && !_.isUndefined(d.description)})
    var description_for_type = function(type_code){
        var fallback_language = 'en'
        /* Return the current language OR fallback_language OR the first one we find */
        return (
            _.find(ds, function(d){return d.type.code === type_code && d.language === tag.language}) ||
            _.find(ds, function(d){return d.type.code === type_code && d.language === fallback_language}) ||
            _.find(ds, function(d){return d.type.code === type_code}) || 
            {}
        ).description
    };

    tag.description = description_for_type(1)
    tag.objectives = description_for_type(2)
    tag.target_groups = description_for_type(3)
}

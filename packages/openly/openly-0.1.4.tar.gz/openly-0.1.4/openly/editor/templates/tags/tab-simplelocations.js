/* {% load i18n %} */
/* {% load ifsetting %}
/* globals gettext */
var tag = this;

// {% ifsetting EDITOR_SHOW_HELPTEXT_ABOVE %}
tag.EDITOR_SHOW_HELPTEXT_ABOVE = true
// {% else %}
tag.EDITOR_SHOW_HELPTEXT_ABOVE = false
// {% endifsetting %}

tag.mixin('SerializerMixin');
tag.mixin('TabMixin');
tag.mixin('ValidationMixin');
tag.store = tag.opts.store;
tag.locations = tag.store.locations; /* Locations which are already selected */
tag.all_locations = tag.opts.store.choices.locations;
tag.search_locations = tag.all_locations
tag.location_ids = [];
tag.keyword = '';
tag.select_hidden = true;
tag.modal_options = { tab_name: 'Locations' };

function setTagLocationIds() { 
    var new_location_ids = _.map(tag.locations, function (l) { return l.location.code; });
    if (!_.isEqual(_.orderBy(new_location_ids), _.orderBy(tag.location_ids))){
        tag.update({location_ids: new_location_ids});
    };
};


function load_locations_from_store() {
    tag.locations = tag.store.locations;
    setTagLocationIds();
}

tag.hide_select =  function(){
    tag.update({select_hidden: true})
}
tag.show_select = function(){
    tag.update({select_hidden: false})
}


tag.clearSearch = function () {
    tag.keyword = '';
    tag.search_locations = tag.all_locations
    tag.update();
}

tag.on('mount', function () {
    load_locations_from_store();
});

tag.store.on('locations_updated', function () {
    load_locations_from_store();
    tag.clearSearch();
});


tag.searchKeyup = function (e) {
    tag.keyword = e.target.value;
    if (tag.keyword.length >= 3) {
        tag.search_locations = tag.all_locations.filter(function (l) {
            return (l.name.toUpperCase().indexOf(tag.keyword.toUpperCase()) !== -1)
        });
    } else {
        tag.clearSearch();
    }
};

tag.add_location = function (e) {
    tag.locations.push({ location: { code: e.target.value, name: e.target.name }, percentage: 0.0 });
    setTagLocationIds();
    tag.update({ value_has_changed: true });
    tag.hide_select();
    tag.clearSearch();
};

tag.save = function () {
    /** Serialize the tags and send the serialized object to the activity update API.
    */
    var xhr;
    var serializeObject = function () {
        var locations = _.clone(tag.store.locations);
        // remove the elements that have a null code
        _.remove(locations, function (location) { return !location.location.code; });
        return { locations: locations, id: tag.store.activity_id };
    };
    var serialized_object = serializeObject();

    window.banner_message.show(gettext('Saving the Locations'), 'warning');
    tag.update();
    xhr = tag.put(serialized_object, { update_done: 'locations_update_done' });
    xhr.done(function (activity) {
        window.banner_message.show(gettext('Successfully saved the Locations'), 'success');
        RiotControl.trigger('reload_activity', activity);
        tag.clearSearch();
    });
};


tag.delete_location = function (e) {
    _.pullAllWith(tag.locations, [e.target.value], function (lhs, rhs) {
        return lhs.location.code === rhs;
    });
    tag.update({ value_has_changed: true });
    setTagLocationIds();
};

tag.has_changed = function () {
    /* Handle case where one 'dummy' is added to the tag */
    function noNullCodes(location) {
        return !_.isNull(location.location.code);
    }
    return !_.isEqual(_.filter(tag.store.locations, noNullCodes), tag.store._initial.locations);
};

tag.child_tags_validated = function () { return true; };

tag.discard = function(){
    tag.store.locations = _.cloneDeep(tag.store._initial.locations);
}
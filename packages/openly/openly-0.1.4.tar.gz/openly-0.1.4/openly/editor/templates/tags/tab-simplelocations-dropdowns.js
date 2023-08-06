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
    var new_location_ids = _.map(tag.store.locations, function (l) { return l.location.code; });
    if (!_.isEqual(_.orderBy(new_location_ids), _.orderBy(tag.location_ids))){
        try {
            tag.update({location_ids: new_location_ids, location_ids_numeric: _(new_location_ids).map(_.toNumber).value()});
        } catch(e) {
            setTimeout(function(){setTagLocationIds()}, 100)
        }
    };
};

function load_locations_from_store() {
    tag.locations = tag.store.locations;
    setTagLocationIds();
    /* Trigger another update as names sometimes don't show */
    setTimeout(function(){tag.update()}, 100)
}

tag.on('mount',function(){
    (function setLocationChoices(c, choice_name){
        /* Alter the choices available to the dropdowns */
        var by_id;
        if (c[choice_name]){return}

        /* Lookup for areas by ID */
        by_id = _.keyBy(c.locations, 'code');
        function decorate(i){
            if (i.parent == 1){
                i.parent_name = i.name;
            } else {
                i.parent_name = _.get(by_id, [i.parent, 'name']);
            }
        }
        c[choice_name] = _.each(_.cloneDeep(c.locations), decorate)
    })(tag.store.choices, 'locations_by_parent');
})

function hide_select(){
    tag.update({select_hidden: true, open_search: null})
}

function show_select(e){
    tag.update({select_hidden: false, open_search: e.item.enum})
}

function defaultObject(e){
    return { location: { code: null, name: null }, percentage: 0.0 };
}

function clearSearch() {
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
        tag.clearSearch();
    }).fail(function(){
        window.banner_message.show(gettext('Error while saving'), 'danger');
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

add_object = function(){
    tag.value_has_changed = true;
    tag.locations.push(defaultObject());
}

drop_object = function(e){
    tag.value_has_changed = true;
    tag.locations.splice(e.item.index, 1);
    setTagLocationIds();
}

tag.add_object = add_object
tag.drop_object = drop_object
tag.hide_select =  hide_select
tag.show_select = show_select
tag.clearSearch = clearSearch

tag.store.on('path_updated', setTagLocationIds) // {# Disabled choices need to be refreshed on tag update #}

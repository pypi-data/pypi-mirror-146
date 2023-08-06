/* global _ riot */
/* exported LocationStore */

function LocationStore(activity, choices) {
    var store = this;

    function add_empty_location() {
        store.locations.push({ location: { code: null }, percentage: '0.00' });
    }

    function load_data(activity_data) {
        store.locations = activity_data.locations;

        store._initial = { locations: _.cloneDeep(store.locations) };
        store._initial_ids = _.map(store._initial.locations, 'id');

        if (store.locations.length === 0) {
            store.add_empty_location();
        }
        store.trigger('locations_updated');
    }

    riot.observable(store);
    store._delete = []; // array of elements to be deleted
    store.fieldvalidation = {};

    // property set up that use the activity data
    store.activity_id = activity.id;
    store.choices = choices;

    store.on('locations_update_done', function (activity_data) {
        store.load_data(activity_data);
    });

    store.urls = function (activity_data) {
        return {
            update: '{% url "activity_update_general" "XXXXX" %}'.replace('XXXXX', activity_data.id)
        };
    };

    function add_empty_location() {
        store.locations.push({ location: { code: null }, percentage: '0.00' });
        store.trigger('locations_updated');
    }

    function load_data(activity_data) {
        store.locations = activity_data.locations;

        store._initial = { locations: _.cloneDeep(store.locations) };
        store._initial_ids = store._initial.locations.map(function (location) { return location.id; });

        if (store.locations.length === 0) {
            store.add_empty_location();
        }
        store.trigger('locations_updated');
    }

    store.load_data = load_data;
    store.add_empty_location = add_empty_location;
    store.load_data(activity);
}

/**
 * A OrganisationActivityStore instance is a RiotControl store holding an array of OrganisationActivity
 *
 * @class OrganisationActivityStore
 * @param source {Object} An object to use as the "source", usually a JSON array or object passed in by Django or loaded by AJAX
 * @param choices {Object} Defines choices for fields where there may be a select field or similar
 * @constructor
 */

/* global $, RiotControl, stores, moment */
/* exported OrganisationActivityStore */

function OrganisationActivityStore(source, choices, organisation_pk) {
    var el = 'organisation_activity_set';
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.languages = { en: { language_name: 'English' }, tet: { language_name: 'Tetum' } };
    store.load(source);
    store.root_element = el;
    store[el] = source || { organisation_activity_set: [] };
    store._initial = _.cloneDeep(source);
    store.requesthistory = [];

    store.fetch = function(){
        var url = "{% url 'organisation_activities' 'XXXXXX' %}".replace('XXXXXX', organisation_pk)
        store.loading = true;
        store.trigger('organisation_activities_set_requested')
        return $.getJSON(url).then(function(json){
            store[el] = json.activities;
            store.implementing_partners = json.implementing_partners;
            /* Replace or augment store's choices from JSON */
            store.choices = store.choices || {};
            _.each(json.choices, function(v,k){
                store.choices[k] = v;
            })
            store.trigger('organisation_activities_set_restored');
            store.loading = false;
            return store[el]
        })
    }

    store.urls = function () {
        return {
        };
    };
}

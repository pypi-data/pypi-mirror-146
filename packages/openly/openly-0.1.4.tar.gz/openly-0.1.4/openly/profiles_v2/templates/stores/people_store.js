/**
 * A PeopleStore instance is a RiotControl store holding an array of serialized representations
 * of the people associated with an organisation's profile 
 *
 * @class PeopleStore
 * @param source {Object} An object to use as the "source", usually a JSON array or object passed in by Django or loaded by AJAX
 * @param choices {Object} Defines choices for fields where there may be a select field or similar
 * @param organisation_pk {String} The primary key associated with the store's organisation
 * @constructor
 */

/* jslint browser: true*/
/* global $, jQuery, RiotControl, stores, moment */

function PeopleStore(source, choices, organisation_profile_pk) {
    var el = 'people_set';
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.languages = { en: { language_name: 'English' }, tet: { language_name: 'Tetum' } };
    store.load(source);
    store.root_element = el;
    store[el] = source || { people_set: [] };
    store._initial = _.cloneDeep(source);
    store.requesthistory = [];

    store.tag_registry = {};
    store.fieldvalidation = {
    };

    store.method = 'PUT';
    store.prune = true;

    store.requestopts = {
	create_done: el + '_created',
	create_fail: el + '_failed',
	update_done: el + '_updated',
	update_fail: el + '_update_failed',
	delete_done: el + '_deleted',
    };

    store.urls = function() {
        return {
	    create: "{% url 'organisation_people-list' %}",
	    update: "{% url 'organisation_people-detail' pk='XXXXX' %}",
	    get_update_url: function(pk) {
		return this.update.replace('XXXXX', pk);
	    },
        };
    };

    store.deleted = function(person) {
	store[el] = store[el].filter(function(p) { return p.id != person.id; });
    }
}

/**
 * An OrganisationContactInfoStore instance is a RiotControl store holding a serialized representation of an organisation's ContactInfo model
 *
 * @class OrganisationContactInfoStore
 * @param source {Object} An object to use as the "source", usually a JSON array or object passed in by Django or loaded by AJAX
 * @param choices {Object} Defines choices for fields where there may be a select field or similar
 * @param organisation_pk {String} The primary key associated with the store's organisation
 * @constructor
 */

/* jslint browser: true*/
/* global $, jQuery, RiotControl, stores, moment */

function OrganisationContactInfoStore(source, choices, organisation_pk) {
    var el = 'organisation_contact_info';
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.languages = { en: { language_name: 'English' }, tet: { language_name: 'Tetum' } };
    store.load(source);
    store.root_element = el;
    store[el] = source || { organisation_contact_info: {} };
    store._initial = _.cloneDeep(source);
    store.requesthistory = [];

    store.tag_registry = {};
    store.fieldvalidation = {
    };

    store.method = 'PUT';
    store.prune = true;

    store.urls = function () {
        return {
	    update: "{% url 'organisation_contact_info' 'XXXXX' %}".replace('XXXXX', organisation_pk),
        };
    };

    store.requestopts = {
	update_done: el + '_updated',
    };
}


/**
 * A PartnersStore instance is a RiotControl store holding an array of Partners
 *
 * @class PartnersStore
 * @param source {Object} An object to use as the "source", usually a JSON array or object passed in by Django or loaded by AJAX
 * @param choices {Object} Defines choices for fields where there may be a select field or similar
 * @constructor
 */

/* global $, RiotControl, stores, moment */
/* exported PartnersStore */

function PartnersStore(source, choices) {
    var el = 'partners_set';
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.languages = JSON.parse("{{ languages|escapejs }}");
    store.load(source);
    store.root_element = el;
    store[el] = source || { partners: [] };
    store._initial = _.cloneDeep(source);
    store.requesthistory = [];

    store.urls = function () {
        return {};
    };
}

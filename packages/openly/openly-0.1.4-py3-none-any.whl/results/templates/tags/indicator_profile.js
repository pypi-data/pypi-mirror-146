/* global stores */

var tag = this;
var store = stores.results_store;

tag.indicator = {};

function getItem(id) {
    tag.indicator = store.getRichItem('resultindicator', _.toNumber(id));
    tag.organisation_link = _.replace("{% url 'organisation_profile' 'XXXXXX' %}", 'XXXXXX', tag.indicator.organisation);
}

tag.on('route', getItem);
/* {% load i18n %} */
/* global stores */

var tag = this;
var store = stores.results_store;

function getContent(content_type) {
    return store.getRichItems({ content_type: content_type });
}

function filterCondition(indicator) {
    return tag.active_sector === 'All' || tag.active_sector === _.get(indicator, 'result_indicator_type.sector');
}

function filterIndicators() {
    return _.filter(getContent('resultindicator'), filterCondition);
}

function filter() {
    var indicators = _.orderBy(filterIndicators(), 'last_updated');

    tag.update({
        indicators: indicators,
        filtered_indicators: _.size(indicators)
    });
}

tag.on('route', function (sector) {
    tag.active_sector = localStorage.getItem('active_sector');
    filter();
});

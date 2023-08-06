/* {% load i18n %} */
/* globals Plotly stores moment */

var tag = this;
var store = stores.results_store;
var results = store.results;

tag.store = store;
tag.indicator = {};

function ellipsize_title() {
    var elements = $('.card-title');

    _.each(elements, function (element) {
        var wordArray = element.innerHTML.split(' ');
        while (element.scrollHeight > element.offsetHeight) {
            wordArray.pop();
            element.innerHTML = wordArray.join(' ') + '...'; // eslint-disable-line no-param-reassign
        }
    });
}

function build_chart() {
    var indicator = (tag.opts.indicator || tag.parent.indicator || {});
    var colors = [ '#ff6b6b', '#ffe66d', '#017ee5' ];
    var y_axis = { target: [] };
    var x_axis = { target: [] };
    var selected_color;
    var data = [];

    var gd = Plotly.d3
        .select('#card-' + indicator.id + '-line-chart')
        .style({ width: 100 + '%', height: 100 + '%' })
        .node();

    var layout = {
        xaxis: { showgrid: false, type: 'date', tickangle: 0, tickformat: '%b %y' },
        margin: { l: 35, r: 35, b: 0, t: 0, pad: 4 },
        legend: { orientation: 'h' },
        showlegend: true
    };

    var options = {
        modeBarButtonsToRemove: ['sendDataToCloud', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian'],
        displaylogo: false
    };

    var addChartValue = function (period) {
        var dimension = _.get(period.resultindicatorperiodactualdimension_set[0], 'value', 'none');

        if (!_.has(y_axis, dimension)) _.set(y_axis, dimension, []);
        if (!_.has(x_axis, dimension)) _.set(x_axis, dimension, []);

        x_axis[dimension].push(period.period_end);
        y_axis[dimension].push(period.actual);
        y_axis['target'].push(period.target);

        if (!_.includes(x_axis['target'], period.period_end)) x_axis['target'].push(period.period_end);
    };

    var addTrace = function (value, key) {
        var trace = {
            x: x_axis[key],
            y: y_axis[key],
            type: 'scatter',
            mode: 'lines'
        };

        if (key === 'target') {
            trace.hoverinfo = 'none';
            trace.name = '{% trans "Target" %}';
            trace.line = { color: '#7fd99b', width: 3, dash: 'dot' };
        } else {
            selected_color = _.pullAt(colors, _.random(colors.length - 1))[0];

            trace.hoverinfo = 'x+y';
            trace.name = _.replace('{% trans "Timor-Leste DIMENSION_TO_REPLACE" %}', 'DIMENSION_TO_REPLACE', key !== 'none' ? '(' + key + ')' : ''); // eslint-disable-line no-useless-concat
            trace.line = { color: selected_color, width: 3 };
        }

        data.push(trace);
    };

    if (!indicator) return;

    _.each(_.orderBy(tag.periods, 'period_end'), addChartValue);
    _.each(y_axis, addTrace);

    Plotly.newPlot(gd, data, layout, options);

    window.onresize = function () { Plotly.Plots.resize(gd); }
}

tag.on('mount', function () {
    /* Get some values related to the indicator */
    var update = {};
    var indicator = tag.opts.indicator || tag.parent.indicator;

    /**
     * Get the content property of the first related model
     * @param filter {object}: This will be something like { content_type: 'resultindicatortitle', result: result_id } for resulttitle
     * @returns {string}
     */
    function get_narrative(filter) {
        /* Search for the through model ID i.e. the "resultindicatortitle" on a "resultindicator" */
        var narrative_links = _.find(results, filter);
        /* return the content of the first narrative on the object */
        return _.get(narrative_links, 'narratives[0].content', 'No narrative content');
    }

    update.indicator = indicator;
    update.type = _.find(results, { content_type: 'resultindicatortype', result_indicator: indicator.id }) || { display: 'Narrative' };
    update.periods = _.filter(results, { content_type: 'resultindicatorperiod', result_indicator: indicator.id });
    update.measure = indicator.measure ? _.find(tag.store.choices.indicatormeasure, { 0: indicator.measure })[1] : null;
    update.title = get_narrative({ content_type: 'resultindicatortitle', result_indicator: indicator.id });
    update.narrative = get_narrative({ content_type: 'resultindicatordescription', result_indicator: indicator.id });
    update.description = get_narrative({ content_type: 'resultindicatorbaselinecomment', result_indicator: indicator.id });
    update.edit_link = tag.store.navigation_urls({ content_type: 'resultindicator', id: _.toNumber(indicator.id), action: 'edit' });

    tag.update(update);

    ellipsize_title();

    if (tag.periods.length > 2) { build_chart(); }
    /* Set the initial state of the tag display */
});

tag.get_year = function (date) {
    return moment(date).format('YYYY');
};

tag.open_indicator_profile = function () {
    route('indicator/' + tag.indicator.id);
}

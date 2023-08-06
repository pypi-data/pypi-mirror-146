/* global stores */
/* eslint no-underscore-dangle: 0 */
function NarrativeStore(el, source, choices) {
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.root_element = el;
    store.load(source);
    store.requesthistory = [];
    store.root_element_type = 'object';
    store.fieldvalidation = {};

    store.requestopts = {
        create_done: el + '_created',
        update_done: el + '_updated',
        validation: el + '_validation_error'
    };

    store.template = {
        activity: _.get(stores, 'activityStore.activity.id', undefined),
        related_object_id: 0,
        content: ''
    };

    store.urls = function () {
        return {
            update: ''
        };
    };


    // Set of functions to return a URL for a list or detail page
    var api_urls = {
        narrative: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-narrative-list' %}"
            }
            return "{% url 'result-api-narrative-detail' 'XXXXXX' %}".replace('XXXXXX', pk)
        }
    };

    /** "New Object" function
     *
     * Example Usage:
     * stores.resultsStore.make_request('result', {title: "Hello World", type: {code: 1}, activity:'MM-FERD-ID6166'})
     * @param opts {object} Has object_type, data, tag
     * returns an xhr from the storemixin
     */
    function make_request(opts){
        var object_type = _.get(opts, 'object_type', 'result');
        var data = _.get(opts, 'data', {});
        var url =  api_urls[object_type](data.id);
        var tag = _.get(opts, 'tag', undefined);
        var method = _.has(data, 'id') && !_.isUndefined(data.id) ? 'PUT' : 'POST'; // "POST" if there's no id in data ie new object else "PUT"
        if (_.has(opts, 'method')) {method = _.get(opts, 'method')}

        return store.save(
            tag, {
                data:data,
                method: method,
                url: url// "list" view if there's no id or "detail" view if there is
            }
        );
    }

    store.make_request = make_request;
}

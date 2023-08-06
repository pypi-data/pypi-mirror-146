/* global stores */
/* eslint no-underscore-dangle: 0 */
/* exported ResultsStore */

function reformat(result){
    return {
        'description': result.description,
        'title': result.title,
        'result_type': _.get(result, ['type','code']),
        'result_type_name': _.get(result, ['type','name']),
        'activity': result.activity,
        'id': result.id
    }
}

function ResultsStore(el, source, choices) {
    var store = this;
    store.reformat = reformat;
    riot.observable(store);
    store.el = el;
    store.choices = choices || {};
    store.root_element = el;
    store.load(_.map(_.orderBy(source, 'id'), store.reformat));
    store.requesthistory = [];
    store.root_element_type = 'array';
    store.fieldvalidation = {};

    store.requestopts = {
        create_done: el + '_created',
        update_done: el + '_updated',
        validation: el + '_validation_error',
        delete_done: el + '_deleted'
    };

    store.template = reformat({
        activity: stores.activityStore.activity.id,
        type: {code: undefined, name:undefined},
        title: '',
        description: '',
        id: undefined
    });

    store.urls = function(data){
        return {
            create: "{% url 'result-api-legacyresult-list' %}",
            update: "{% url 'result-api-legacyresult-detail' 'XXXXXX' %}".replace('XXXXXX', data.id),
            delete: "{% url 'result-api-legacyresult-detail' 'XXXXXX' %}".replace('XXXXXX', data.id),
        }
    };

    

}

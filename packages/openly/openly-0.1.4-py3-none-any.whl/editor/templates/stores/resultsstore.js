/* global stores */
/* eslint no-underscore-dangle: 0 */
function ResultsStore(el, data, choices) { // eslint-disable-line no-unused-vars
    var store = this;
    var api_urls;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.root_element = el;
    store.admin_fields = false;

    store.admin_status_change = function () {
        store.admin_fields = !store.admin_fields;
        store.trigger('admin_status_change');
    };

    // Results are a more complex model set. Rather than using nested serializers,
    // here we opt for a flatter approach.

    _.each(data, function (set, object_name) {
        _.each(set, function (object) {
            var content_type;
            object.content_type = object_name;
            content_type = _.find(data.contenttype, { model: object_name });
            if (!content_type) { return; }
            object.content_type_id = content_type.id;
        });
    });

    store.load(_.flatten(_.values(data)));

    store.requesthistory = [];
    store.root_element_type = 'array';
    store.fieldvalidation = {};

    store.requestopts = {
        create_done: el + '_created',
        update_done: el + '_updated',
        delete_done: el+ '_deleted',
        validation: el + '_validation_error'
    };

    store.template = {
        activity: _.get(stores, 'activityStore.activity.id', undefined),
        type: {
            code: ''
        },
        title: '',
        description: ''
    };

    store.urls = function () {
        return {
            update: ''
        };
    };

    function selectNarrative(set) {
        /* Some day we'll use Narratives to provide multilingual support */
        /* At that time this function will be smarter than just returning the first Narrative found */
        var path = '[0].narratives[0].content';
        return _.get(set, path);
    }

    function makeRich(item) {
        var clonedItem;

        function Nar(content_type) {
            return selectNarrative(_.filter(store.getItems(), { content_type: content_type, result_indicator: item.id }));
        }

        if (!item) { item = {}; }
        if (item.content_type === 'resultindicator') {
            clonedItem = _.clone(item);
            clonedItem.title = Nar('resultindicatortitle');
            clonedItem.description = Nar('resultindicatordescription');
            clonedItem.baseline_comment = Nar('resultindicatorbaselinecomment');
            clonedItem.result_indicator_type = store.getItems({ content_type: 'resultindicatortype', result_indicator: item.id }, true);
            clonedItem.key_progress_statement = Nar('resultindicatorkeyprogressstatement');
            return clonedItem;
        } else if (item.content_type === 'result') {
            clonedItem = _.clone(item);
            clonedItem.title = selectNarrative(_.filter(store.getItems(), { content_type: 'resulttitle', result: item.id }));
            clonedItem.description = selectNarrative(_.filter(store.getItems(), { content_type: 'resultdescription', result: item.id }));
            return clonedItem;
        } else if (item.content_type === 'resultindicatorperiod') {
            clonedItem = _.clone(item);
            clonedItem.actual = _.toNumber(clonedItem.actual) || clonedItem.actual;
            clonedItem.target = _.toNumber(clonedItem.target) || clonedItem.target;
            return clonedItem;
        }
        return item;
    }

    store.getItems = function (filter, first /* find or filter */) {
        var items = store.results;
        if (_.isUndefined(filter)) {
            return items;
        }
        if (first) {
            return _.find(items, filter) || {};
        }
        return _.filter(items, filter) || [];
    };

    store.getRichItems = function (filter) {
        var items = store.getItems();
        var filteredItems = _.filter(items, filter);
        return _.map(filteredItems, makeRich) || [];
    };

    store.getItem = function (content_type, id) {
        var items = store.getItems();
        return _.find(items, { content_type: content_type, id: id });
    };

    store.getRichItem = function (content_type, id) {
        return makeRich(store.getItem(content_type, id));
    };

    store.selectNarrative = selectNarrative;

    function getActivityId() { return stores.activityStore.activity.id; }
    function getLanguage() { return 'en'; }

    function getContentTypeId(content_type) {
        var content_type_object = _.find(stores.resultsStore.results, { content_type: 'contenttype', model: content_type });
        if (_.isUndefined(content_type_object)) {
            /* If underscores, remove them */
            content_type_object = _.find(stores.resultsStore.results, { content_type: 'contenttype', model: content_type.replace(/_/gi, '') });
            return content_type_object.id;
        }
        return content_type_object.id;
    }
    store.getContentTypeId = getContentTypeId;

    function getContentTypeName(content_type_id) {
        var content_type_object = _.find(stores.resultsStore.results, { content_type: 'contenttype', id: content_type_id });
        if (_.isUndefined(content_type_object)) { return undefined; }
        return content_type_object.model;
    }

    store.getTemplate = function (content_type) {
        if (content_type === 'resultindicator') {
            return {};
        } else if (content_type === 'resultindicatorbaselinecomment') {
            return {
                language: 'en',
                content: ''
            };
        } else if (content_type === 'narrative') {
            /* return new Narrative() */
            return {
                id: undefined,
                language: getLanguage(),
                content: '',
                related_object_id: '?',
                related_content_type: '?',
                activity: getActivityId()
            };
        } else if (content_type === 'result') {
            return {
                activity: getActivityId(),
                type: {code: 1}
            };
        }
        return {};
    };

    store.contentTypeOptions = function (content_type /* :string */, val /* :string */, display /* :string */, exceptions /* :array */) {
        var items = store.getItems({ content_type: content_type });
        var results = [];
        _.each(items, function (item) {
            var code = _.get(item, val || 'code');
            var d;
            if (_.includes(exceptions, code)) { return; }
            d = _.get(item, display || 'name');
            results.push([code, d]);
        });
        return results;
    };

    // Function to return a URL for a given content type and action

    store.navigation_urls = function (parameters) {
        var content_type = parameters.content_type;
        var id = parameters.id;
        var action = parameters.action;
        var item;
        if (content_type === 'resultindicator' && action === 'edit') {
            item = store.getRichItem(content_type, id);
            return '/' + getLanguage() + '/editor/activity/' + item.activity + '/#results/indicator/' + item.id;
        }
        if (content_type === 'resultindicator' && action === 'profile') {
            item = store.getRichItem(content_type, id);
            return '/' + getLanguage() + '/results/#indicator/' + item.id;
        }
        return undefined;
    };

    // Set of functions to return a URL for a list or detail page
    api_urls = {
        indicatormeasure: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-indicatormeasure-list' %}";
            }
            return "{% url 'result-api-indicatormeasure-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        indicatorvocabulary: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-indicatorvocabulary-list' %}";
            }
            return "{% url 'result-api-indicatorvocabulary-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        narrative: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-narrative-list' %}";
            }
            return "{% url 'result-api-narrative-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultdescription: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultdescription-list' %}";
            }
            return "{% url 'result-api-resultdescription-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatordescription: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatordescription-list' %}";
            }
            return "{% url 'result-api-resultindicatordescription-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiodactualcomment: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiodactualcomment-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiodactualcomment-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiodactualdimension: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiodactualdimension-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiodactualdimension-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiodactuallocation: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiodactuallocation-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiodactuallocation-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiodtargetcomment: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiodtargetcomment-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiodtargetcomment-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiodtargetdimension: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiodtargetdimension-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiodtargetdimension-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiodtargetlocation: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiodtargetlocation-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiodtargetlocation-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorperiod: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorperiod-list' %}";
            }
            return "{% url 'result-api-resultindicatorperiod-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorreference: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorreference-list' %}";
            }
            return "{% url 'result-api-resultindicatorreference-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatortitle: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatortitle-list' %}";
            }
            return "{% url 'result-api-resultindicatortitle-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicator: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicator-list' %}";
            }
            return "{% url 'result-api-resultindicator-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resulttitle: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resulttitle-list' %}";
            }
            return "{% url 'result-api-resulttitle-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resulttype: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resulttype-list' %}";
            }
            return "{% url 'result-api-resulttype-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        result: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-result-list' %}";
            }
            return "{% url 'result-api-result-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatortype: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatortype-list' %}";
            }
            return "{% url 'result-api-resultindicatortype-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorbaselinecomment: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorbaselinecomment-list' %}";
            }
            return "{% url 'result-api-resultindicatorbaselinecomment-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        resultindicatorkeyprogressstatement: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-resultindicatorkeyprogressstatement-list' %}";
            }
            return "{% url 'result-api-resultindicatorkeyprogressstatement-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        actualdimensionset: function (pk) {
            if (_.isUndefined(pk)) {
                return "{% url 'result-api-actualdimensionset-list' %}";
            }
            return "{% url 'result-api-actualdimensionset-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        }
    };

    /**
     * Drop an item by content_type and id
     * @param content_type {text}
     * @param id {int}
     */
    function drop_content(content_type, id) {
        _.remove(store.results, { content_type: content_type, id: id });
        store.trigger('removed', content_type, id);
        store.trigger('removed_' + content_type, id);
    }

    function get_content(content_type, id) {
        return _.find(store.results, { content_type: content_type, id: id });
    }

    /* {% comment %}
    One day we'll use Typescript...
     interface INarrativeResponse {
        id: number
        related_content_type: number
        related_object_id: number
        activity: string
        language: string
     }
     {% endcomment %} */

    function assignNarrative(response) {
        /* A "narrative" type object will likely be attached to a container object
         such as a resultindicatorbaselinecomment
         */
        var contentTypeId = response.related_content_type; // :number
        var contentTypeName = getContentTypeName(contentTypeId); // :string
        var narrativeContainerId = response.related_object_id; // :number
        var narrativeContainerObject;
        var narrativeInObject;

        if (!narrativeContainerId || !contentTypeName) { return; }

        narrativeContainerObject = store.getItem(contentTypeName, response.related_object_id);

        if (!_.has(narrativeContainerObject, 'narratives')) { return; }

        /* createOrUpdate narrative based on the response id */
        narrativeInObject = _.find(narrativeContainerObject.narratives, { id: response.id });
        if (!narrativeInObject) {
            narrativeContainerObject.narratives.push(response);
        } else {
            _.assign(narrativeInObject, response);
        }

        store.trigger('updated', contentTypeName, narrativeContainerId, response);
        store.trigger('updated_' + contentTypeName, narrativeContainerId, response);
    }

    function assign_content(content_type, id, response) {
        var content = get_content(content_type, id);

        response.content_type = content_type;
        response.content_type_id = _.find(store.results, { content_type: 'contenttype', model: content_type });

        if (content_type === 'narrative') {
            assignNarrative(response);
            return;
        }

        if (content) { _.assign(content, response); } else {
            content = response;
            store.results.push(content);
        }
        store.trigger('updated', content_type, id, content);
        store.trigger('updated_' + content_type, id, content);
    }

    function add_content(object) {
        return assign_content(object.content_type, object.id, object);
    }


    /** "New Object" function
     *
     * Example Usage:
     * stores.resultsStore.make_request('result', {title: "Hello World", type: {code: 1}, activity:'MM-FERD-ID6166'})
     * @param opts {object} Has object_type, data, tag
     * returns an xhr from the storemixin
     */
    function make_request(opts) {
        var content_type = _.get(opts, 'content_type', _.get(opts, 'object_type')); // Prefer to use "content_type for consistency
        var requestData = _.get(opts, 'data', {});

        var tag = _.get(opts, 'tag', undefined);
        var method = _.has(requestData, 'id') && !_.isUndefined(requestData.id) ? 'PUT' : 'POST'; // "POST" if there's no id in data ie new object else "PUT"

        var url; // :string
        if (!_.isFunction(_.get(api_urls, content_type))) {
            /* Trying to hit an endpoint not "registered" with the store */
            console.error('/* Trying to hit an endpoint not "registered" with the store */'); // eslint-disable-line no-console
        }
        url = api_urls[content_type](requestData.id);
        if (_.has(opts, 'method')) { method = _.get(opts, 'method'); }
        method = _.toUpper(method);

        /** Rename the "id" field if it's actually a one-to-one relationship with a different name */
        if (_.get(opts, 'primary_key_field')) {
            requestData[opts.primary_key_field] = _.remove(requestData, 'id');
        }

        return store.save(tag, {
            data: requestData,
            method: method,
            url: url// "list" view if there's no id or "detail" view if there is
        }).then(function (response) {
            if (method === 'DELETE') {
                drop_content(content_type, requestData.id);
                return undefined;
            } else if (_.has(opts, 'assign')) {
                response.content_type = content_type;
                response.content_type_id = _.find(store.results, { content_type: 'contenttype', model: content_type });
                _.assign(_.get(opts, 'assign'), response);
                store.trigger('updated', content_type, response.id, response);
                store.trigger('updated_' + content_type, response.id, response);
                return response;
            }

            assign_content(content_type, response.id, response);
            return response;
        });
    }

    store.make_request = make_request;
    store.drop_content = drop_content;
    store.add_content = add_content;
    /* To log all events fired by this store uncomment the line below */
    // store.on('*', function(){console.log(arguments)});
}

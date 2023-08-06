/**
 * A TransactionStore instance is a RiotControl store holding an array of Transactions
 *
 * @class TransactionStore
 * @param el {String} The reference to use for the object e.g. "activity"
 * @param source {Object} An object to use as the "source", usually a JSON array or object passed in by Django or loaded by AJAX: {id: "1", name: "my activity"}
 * @param choices {Object} Defines choices for fields where there may be a select field or similar
 * @constructor
 * @listens RiotRestMixin.trigger:create_element
 * @listens RiotRestMixin.trigger:delete_element
 * @listens RiotRestMixin.trigger:toggle_delete_element
 * @listens RiotRestMixin.trigger:restore_deleted_element
 * @listens RiotRestMixin.trigger:restore_element
 */

/* jslint browser: true */
/* global $, RiotControl, stores, moment */
/* exported TransactionStore */

function TransactionStore(source, choices) {
    var el = 'transactions';
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.load(source);
    store._initial = _.cloneDeep(source);
    store.requesthistory = [];

    store.tag_registry = {};

    store.method = 'PUT';
    store.prune = true;

    store.urls = {
        create: function () {
            return "{% url 'editor-api-transaction-list' %}";
        },
        update: function (pk) {
            return "{% url 'editor-api-transaction-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        delete: function (pk) {
            return "{% url 'editor-api-transaction-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        }
    };

    store.requestopts = {
        create_done: el + '_created',
        update_done: el + '_updated',
        delete_done: el + '_deleted'
    };

    store.on(store.requestopts.create_done, function (data, response_data) { store.setOrPushData(response_data); store.trigger(el + '_changed'); });
    store.on(store.requestopts.update_done, function (data, response_data) { store.setOrPushData(response_data); store.trigger(el + '_changed'); });
    store.on(store.requestopts.delete_done, function (data) { store.removeById(data.id); store.trigger(el + '_changed'); });
}

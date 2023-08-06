/* jslint browser: true */
/* exported BudgetStore */

function BudgetStore(source, choices) {
    var store = this;
    var el = 'budgets';

    store.getActivity = function () {
        return stores.activityStore.activity;
    };

    riot.observable(store);
    store.el = el;
    store.choices = choices || {};
    store.load(source);

    store.urls = {
        create: function () {
            return "{% url 'editor-api-budget-list' %}by_activity/?activity=" + store.getActivity().id;
        },
        update: function (pk) {
            return "{% url 'editor-api-budget-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        },
        delete: function (pk) {
            return "{% url 'editor-api-budget-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        }
    };

    store.formatMoney = function (number, currency_id) {
        /* Wrapper around accounting.formatNumber */

        return accounting.formatMoney(number, {
            symbol: currency_id || '',
            precision: 0,
            thousand: ',',
            format: {
                pos: '%v %s ',
                neg: '(%v) %s',
                zero: ''
            }
        });
    };

    store.unformatMoney = function (value) {
        return accounting.unformat(value);
    };
}

/* exported MsdpStore */
function MsdpStore() {
    var store = this;
    riot.observable(this);
    store.el = 'msdp';
    store.choices = {};
    store._initial = {};

    store.urls = function () {
        return { update: "{% url 'editor-api-activitytag-detail' 'XXXXXX' %}".replace('XXXXXX', stores.activityStore.activity.id) };
    };
}

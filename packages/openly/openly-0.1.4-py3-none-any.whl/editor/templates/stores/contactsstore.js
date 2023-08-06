/* global stores */
/* eslint no-underscore-dangle: 0 */
/* exported ContactsStore */
function ContactsStore(el, source, choices) {
    var store = this;
    riot.observable(this);
    store.el = el;
    store.choices = choices || {};
    store.root_element = el;
    store.load(_.orderBy(source, 'id'));
    store.requesthistory = [];
    store.root_element_type = 'array';
    store.fieldvalidation = {};

    store.requestopts = {
        create_done: el + '_created',
        update_done: el + '_updated',
        delete_done: el + '_deleted',
        validation: el + '_validation_error'
    };

    store.template = {
        id: undefined,
        contact_type: { code: null },
        person_name: '',
        organisation: '',
        telephone: '',
        email: '',
        mailing_address: '',
        website: '',
        job_title: '',
        activity: { id: stores.activityStore.activity.id }
    };

    store.urls = function () {
        return {
            update: "{% url 'activitycontacts-detail' pk='XXXXX' %}".replace('XXXXX', stores.activityStore.activity.id)
        };
    };

    store.api_urls = {
        contact: function (pk) {
            if (_.isUndefined(pk) || pk === '') {
                return "{% url 'editor-api-contact-list' %}";
            }
            return "{% url 'editor-api-contact-detail' 'XXXXXX' %}".replace('XXXXXX', pk);
        }
    };
}

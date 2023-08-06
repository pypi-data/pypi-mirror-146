/* jslint browser: true */
/* exported OipaStore */

function OipaStore(source) {
    var store = this;
    riot.observable(store);
    store.el = 'iati';
    store.iati_data = source;
    try {
        store.saved_sync_state = new Set(store.iati_data.link_info.oipa_fields);
        store.curr_sync_state = new Set(store.iati_data.link_info.oipa_fields);
    } catch (err) {
        store.saved_sync_state = new Set();
        store.curr_sync_state = new Set();
    }
}

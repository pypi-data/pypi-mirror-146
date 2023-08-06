/**
* This mixin provides glue functions between a RiotControl store and a tag element
*   to trigger behaviour in the Store
*
*   The tag store (referenced as tag.store) should provide RiotControl trigger
*   hooks as described below
*   for adding, editing, delete/undelete etc and trigger '_changed' to update the tag when necessary
*
* @mixin
* @fires RiotRestMixin.trigger:create_element
* @fires RiotRestMixin.trigger:delete_element
* @fires RiotRestMixin.trigger:toggle_delete_element
* @fires RiotRestMixin.trigger:restore_deleted_element
* @fires RiotRestMixin.trigger:restore_element
* @fires RiotRestMixin.trigger:element_changed
*/
/* eslint no-underscore-dangle: 0, func-names: 0 */
/* exported RiotRestMixin */

var RiotRestMixin = {

    /**
     * @event RiotRestMixin.trigger:element_changed
     */
    init: function () {
        var tag = this;
        var el = this.store.root_element;
        tag.on('mount', function () {
            RiotControl.on(el + '_changed', function () {
                tag.update();
            });
        });
    },

    /**
     * @method rc_update
     * @memberof RiotRestMixin
     * @param e {event} event - The Riot event to listen for
     */
    rc_update: function (e) {
        /**
         * Call this to begin editing an object by setting the tag's current "edit target"
         * Calls update_(object_name) with the tag item as the first parameter
         * @event RiotRestMixin.trigger:update_element
         * @type {object}
         */

        var tag = this;
        var el = this.store.root_element;
        if (tag.store._delete.indexOf(e.item.id) > -1) {
            return;
        }
        if (tag.store[el].indexOf(e.item) === -1) {
            return;
        }
        tag.current_edit = el + '[' + tag.store[el].indexOf(e.item) + ']';// Returns a string like 'transaction[0]'
        tag.store.trigger('update_' + el, e.item);// Mark this as a changed item in the store so that it will be committed
    },

    rc_update_done: function () {
        /* Call this when editing is complete to drop the tag's current "edit target" */
        var tag = this;
        tag.current_edit = undefined;
        tag.update();
    },


    rc_create: function () {
      /**
       * Trigger a call to create a new object.
       *
       * @event RiotRestMixin.trigger:create_element
       * @type {object}
       */
        var el = this.store.root_element;
        var tag = this;
        tag.store.trigger('create_' + el);
    },

    rc_delete_: function (e) {
        /** @event RiotRestMixin.trigger:delete_element */
        /* add an object to the delete queue */

        var el = this.store.root_element;
        var tag = this;
        tag.store.trigger('delete_' + el, e.item);
    },

    rc_restore: function () {
        /** @event RiotRestMixin.trigger:restore_element */
        /* restores all changes to the root element by triggering the store's "restore" function */

        var el = this.store.root_element;
        var tag = this;
        tag.store.trigger('restore_' + el);
    },

    rc_restore_deleted: function (e) {
        /** @event RiotRestMixin.trigger:restore_deleted_element */
        var el = this.store.root_element;
        var tag = this;
        tag.store.trigger('restore_deleted_' + el, e.item);
    },

    /**
     * Trigger a call to add/remove an object to be deleted.
     * @method rc_toggle_delete
     * @event RiotRestMixin.trigger:toggle_delete_element
     * @param e {event}
     */
    rc_toggle_delete: function (e) {
        var el = this.store.root_element;
        var tag = this;
        tag.store.trigger('toggle_delete_' + el, e.item);
    },

    rc_item_status: function (item) {
        var tag = this;
        var id = item.id;
        if ((tag.store._delete || []).indexOf(id) > -1) { return 'delete'; }
        if ((tag.store._update || []).indexOf(id) > -1) { return 'update'; }
        if (id === undefined) { return 'create'; }
        return '';
    }

};

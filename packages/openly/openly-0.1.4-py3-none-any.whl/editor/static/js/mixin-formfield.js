/**
* Mixin for form fields
* @mixin
*
*/
/* exported FormFieldMixin */
var FormFieldMixin = {

    // opts:
    // classes (object): Specify which classes to apply to the form fields
    // formgroup (bool): If False, the tag should not surround its input with <formgroup>.

    /**
     * Register a handler function to be called whenever this tag is updated and default classes for the tag
     */
    init: function () {
        var tag = this;
        var defaults = {
            classes: {
                label: 'control-label',
                select: '',
                outer: '',
                input: 'textarea',
                date_label: 'control-label',
                date: '',
                dropdown: ''
            },
            formgroup: true
        };


        tag.on('before-mount', function () {
            // formgroup = false if you don't want to have formgroup on the surrounding div
            tag.classes = tag.classes || {};
            tag.classes = _.extend(defaults.classes, tag.classes, tag.opts.classes);
            if (tag.opts.formgroup || defaults.formgroup === false) {
                tag.classes.outer = '';
            }

            tag.label = tag.opts.label || 'Choose one';
        });
    },

    /**
     * Change select function:
     * This is currently fired by the "field-choice" tag and changes a select which has attibutes for "name" and "code"
     * @param e {event} Event - This is the event which calls the change of a select option
     */
    change_select: function (e) { // Call from a 'select' field
        var tag = this;
        var data = { code: e.currentTarget.value, name: $('select option:selected', tag.root).text() };
        tag.bystring(tag.path, { data: data, create: true });
    },

    /**
     * set function is called from "field-input" or "date" and directly sets the tag's path to the target value of the field
     * @param e {event} Event - This is the event which calls the change of a select option
     */
    set: function (e) {
        var tag = this;
        if (tag.data === e.currentTarget.value) {
            return;
        }
        tag.bystring(tag.absolute_path(), { data: e.currentTarget.value });
        /* Parent tags may listen to an 'input_set_event' to do various nefarious things */
        if (tag.parent && tag.parent.trigger) {
            tag.parent.trigger('input_set', tag.absolute_path(), e.currentTarget.value);
        }
    },

    /**
     * This field is a complete select2 / select replacement - called field-dropdownselect, it uses loading options only on click to make page operations and navigation faster
     * @param e {event} Event - This is the event which calls the change of a select option
     */
    set_dropdown_select: function (e, data) {
        var tag = this;
        var opts = { data: data, create: true };
        e.preventDefault();
        tag.toggle_dropdown();
        tag.bystring(tag.absolute_path(), opts);
        if (tag.parent && tag.parent.trigger) {
            tag.parent.trigger('input_set', tag.absolute_path(), e.currentTarget.value);
        }
    },

    nullify_dropdown_select: function () {
        var tag = this;
        tag.toggle_dropdown();
        tag.bystring(tag.absolute_path(), { data: _.isObject(tag.data) ? { code: '', name: '' } : null, create: true });
        if (tag.parent && tag.parent.trigger) {
            tag.parent.trigger('input_set', tag.absolute_path(), null);
        }
    },
    /**
     * Ask the store what our current status is: updated, deleted, created or unchanged
     */
    fieldstatus: function () {
        return this.store.path_status(this.absolute_path());
    }

};

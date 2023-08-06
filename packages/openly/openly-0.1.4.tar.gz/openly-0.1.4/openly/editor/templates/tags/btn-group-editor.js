/* globals routeToTag */
var tag = this;
tag.opts.store = tag.parent.store;
tag.store = tag.parent.store;
tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');

function set_disabled() {
    var disable_save = !tag.parent.child_tags_validated();
    if (disable_save !== tag.disable_save) { tag.update({ disable_save: disable_save }); }
}

function set_has_changes() {
    /* Update the tag's "store_has_changes" property if the parent tag
    or any tags in the parent's hierarchy have changed */
    var changed_child_tags = _.find(tag.parent.list_child_tags(), { value_has_changed: true }); // : array|undefined
    var has_changes = !_.isUndefined(changed_child_tags) || tag.parent.value_has_changed; // :bool
    if (has_changes !== tag.store_has_changes) {
        tag.update({ store_has_changes: has_changes });
    }
}

tag.on('update', function () {
    set_disabled();
    set_has_changes();
});

tag.save = function () {
    var request;
    set_disabled();
    set_has_changes();
    if (tag.parent.save_tab_always || (!_.isUndefined(tag.opts.use_parent_save) && !tag.disable_save && tag.store_has_changes)) {
        request = tag.parent.save();
    } else {
        if (!tag.disable_save && !tag.store_has_changes) {
            window.banner_message.show(_.get(tag.store, 'messages.no_changes', 'No changes to save'), 'success');
        }

        if (!tag.disable_save && tag.store_has_changes) {
            if (!_.isFunction(_.get(tag.store, 'save'))) {
                console.warn('This store requires a .save function'); // eslint-disable-line no-console
            } else if (!_.isUndefined(tag.opts.only_save_parent)) {
                request = tag.store.save(tag.parent);
            } else {
                request = tag.store.save();
            }
        }
    }
    return request;
};

tag.next = function () {
    var request;

    if (tag.disable_save) {
        return request;
    }
    request = tag.save();
    _.set(tag, 'parent.opts.ValidationMixin.allow_tab_change', true);
    routeToTag.next();
    _.unset(tag, 'parent.opts.ValidationMixin.allow_tab_change');
    return request;
};

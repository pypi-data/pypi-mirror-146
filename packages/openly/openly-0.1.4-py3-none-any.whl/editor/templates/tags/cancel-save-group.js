var tag = this;

tag.on('mount', function () {
    tag.validate();
});

tag.opts.store = tag.parent.store;
tag.store = tag.parent.store;
tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');

tag.save = function () {
    var xhr;
    if (!_.isFunction(tag.parent.save)) { console.warn('Save function expected', tag.parent); } // eslint-disable-line no-console
    xhr = tag.parent.save();
    // if a request has been triggered, disable that button until it returns
    if (xhr !== undefined && !_.isNull(xhr) && _.isFunction(xhr.always)) {
        tag.saving = true;
        tag.update();
        xhr.always(function () { tag.saving = false; });
    }
    return xhr;
};

tag.cancel = function () {
    tag.fn_validate._banner('hide', 'danger');
    tag.fn_validate._banner('hide', 'warning');
    tag.parent.cancel();
    tag.parent.update();
};

tag.saveAndReturn = function () {
    var xhr = tag.save();
    if (_.has(xhr, 'then')) { xhr.then(tag.parent.onReturn); }
};

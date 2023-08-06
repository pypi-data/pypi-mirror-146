    /** @class field-input */
    var tag = this;
    var default_classes = {
        formgroup: 'form-group',
        label: 'control-label',
        input: ''
      };
    tag.classes = {};
    tag.on('mount', function () {
        tag.update({classes : tag.opts.classes || default_classes})
    });

    tag.block_enter = function (e) { if (e.key === 'Enter') { e.preventDefault(); } };

    tag.mixin('SerializerMixin');
    tag.mixin('FormFieldMixin');
    tag.mixin('ValidationMixin');

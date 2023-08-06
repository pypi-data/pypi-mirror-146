/** @class field-textarea */
var tag = this;

var default_classes = {
    formgroup: 'form-group',
    label: 'control-label',
    input: 'textarea'
  };
  tag.on('mount', function () {
    tag.update({classes : tag.opts.classes || default_classes})
  });

tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');

tag.on('mount', function () {
    tag.update({ classes: tag.opts.classes || default_classes });
});

  tag.resize_area = function () {
      var ta = $('textarea', tag.root);
      var inner;
      ta.height(0);
      if (!_.isUndefined(ta[0])) {
          inner = ta[0].scrollHeight;
          ta.height(_.max([inner, _.toNumber(tag.opts.minheight) || 0]));
      }
  };

tag.on('mount', function () {
    setTimeout(tag.resize_area, 10);
});

tag.resize_area = function () {
    var ta = $('textarea', tag.root);
    var inner;
    ta.height(0);
    inner = ta[0].scrollHeight;
    ta.height(_.max([inner, _.toNumber(tag.opts.minheight) || 0]));
};

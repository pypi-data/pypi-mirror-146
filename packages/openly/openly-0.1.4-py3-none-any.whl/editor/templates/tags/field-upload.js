  /** @class field-upload */
  /* globals gettext */
  var tag = this;

  tag.mixin('SerializerMixin');
  tag.mixin('FormFieldMixin');
  tag.mixin('ValidationMixin');
  tag.request = undefined;
  tag.state = { display: '', progress: undefined, show_progress_bar: false };
  tag.file = { display: {} };

  tag.on('before-mount', function () {
      tag.file.display.name = tag.opts.no_file_display || gettext('No file currently selected');
  });

  (function set(thisTag) {
      thisTag.fn = thisTag.fn || {};
      thisTag.fn.set = function () {
          _.invoke(thisTag, ['fn_validate', '_validate_loudly'], thisTag);
          if (thisTag.validate() !== true) { return; }
          thisTag.bystring(thisTag.path, { data: thisTag.refs.upload.files[0] });
          _.set(thisTag, 'file.display.name', thisTag.data.name);
          _.set(thisTag, 'file.display.size', thisTag.data.size);
          _.set(thisTag, 'file.display.type', thisTag.data.type);
      };
  }(tag));
    // TODO: Tie this into tag store save events
  // function showProgress(evt) {
  //     var percentComplete;
  //     if (evt.lengthComputable) {
  //         percentComplete = 100 * (evt.loaded / evt.total);
  //         _.set(tag, 'state.progress', _.toInteger(percentComplete));
  //         tag.update();
  //     }
  // }

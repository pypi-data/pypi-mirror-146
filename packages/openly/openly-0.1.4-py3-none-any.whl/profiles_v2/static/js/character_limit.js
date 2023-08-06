characterLimit = MediumEditor.Extension.extend({
  name: 'character_limit',
  limit: 1024,
  // ...
  init: function() {
    this.subscribe('editableInput', this.handleInput.bind(this))
    this.content = this.base.getContent()
  },

  handleInput: function(event) {
    // Check whether we are now over the (text) character limit and if so reset the content
    // to its state prior to last input
    if (this.limit < event.target.textContent.length) {
      event.preventDefault();
      event.stopPropagation();
      this.base.setContent(this.content);
    } else {
      this.content = this.base.getContent();
    }
  },
  // ...
});

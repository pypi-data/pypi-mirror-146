{% include 'tags/hide-sensitive-fields-mixin.js' %}

var tag = this;
tag.all_contacts = opts.contacts;
tag.contacts = [];

tag.mixin(new ExpandMixin(tag, 'contacts', 'all_contacts', 3));
tag.mixin(new HideSensitiveFieldsMixin(tag));

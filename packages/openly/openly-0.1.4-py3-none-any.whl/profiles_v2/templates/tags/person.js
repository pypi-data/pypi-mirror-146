{% load static %}
{% include 'tags/hide-sensitive-fields-mixin.js' %}

var tag = this;
tag.mixin(new HideSensitiveFieldsMixin(tag));

edit_person(e) {
    tag.parent.current_person = tag;
    tag.parent.edit_person(opts.data);
}

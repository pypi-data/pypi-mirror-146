{% load static %}

// TODO: the view should dump a JSON of the org profile, and this logic should be in JS
var tag = this;
tag.upload_url = opts.upload_url;
tag.csrf_token = opts.csrf_token;

{% if organisation_profile.banner_image %}
    tag.image_url = "{{ organisation_profile.banner_image.url }}";
{% else %}
    tag.image_url = "{% static 'img/blank_banner.png' %}";
{% endif %}

tag.mixin(new FileUploadMixin(tag, function(response) {
    tag['image_url'] = response.image;
    tag.update();
}));

tag.on('mount', function() {
    // tag.form_id is used in the FileUploadMixin
    tag.upload_container_selector = '#banner-image-modal';
    tag.form_id = '#form-banner_image';
    tag.hide_file_input();
});

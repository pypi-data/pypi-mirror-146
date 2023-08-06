{% load static %}

// TODO: the view should dump a JSON of the org profile, and this logic should be in JS
var tag = this;
tag.upload_url = opts.upload_url;
tag.csrf_token = opts.csrf_token;

{% if organisation_profile.logo %}
    tag.image_url = "{{ organisation_profile.logo.url }}";
{% else %}
    tag.image_url = "{% static 'img/logo_placeholder.svg' %}";
{% endif %}

tag.mixin(new FileUploadMixin(tag, function(response) {
    tag['image_url'] = response.image;
    tag.update();
}));

tag.on('mount', function() {
    tag.upload_container_selector = '#logo-image-modal';
    tag.form_id = '#form-logo_image';
    tag.hide_file_input();
});

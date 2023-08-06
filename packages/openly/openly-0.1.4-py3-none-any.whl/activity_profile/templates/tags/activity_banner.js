{% load static %}

// TODO: the view should dump a JSON of the org profile, and this logic should be in JS
var tag = this;
tag.upload_url = opts.upload_url;
tag.csrf_token = opts.csrf_token;

{% if activity_profile.banner_image %}
tag.image_url = "{{ activity_profile.banner_image.url }}";
{% endif %}

tag.mixin(new FileUploadMixin(tag, function(response) {
    tag['image_url'] = response.image;
    tag.update();
}));

tag.on('mount', function() {
    // tag.form_id is used in the FileUploadMixin
    tag.upload_container_selector = '#activity-banner-modal';
    tag.form_id = '#form-activity_banner';
    tag.hide_file_input();
});

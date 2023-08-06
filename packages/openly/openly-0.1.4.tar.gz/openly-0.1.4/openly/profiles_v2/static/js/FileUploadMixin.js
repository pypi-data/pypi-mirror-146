function FileUploadMixin(tag, cb) {

    this.handle_file_upload = function () {
        var form_data = new FormData(document.querySelector(tag.form_id));

        var xhr = $.ajax({
            data: form_data,
            contentType: false,
            processData: false,
            method: 'POST',
            url: tag.upload_url,
            headers: { 'X-CSRFTOKEN': tag.csrf_token },
        });
	xhr.done(cb)
    }

    this.hide_file_input = function () {
        // hack because browsers don't allow changing the placeholder for input[type="file"]
        var displayed_upload_button = document.querySelector(tag.upload_container_selector + ' .choose-image-display');
        if (displayed_upload_button) {
            displayed_upload_button.onclick = function () {
                document.querySelector(tag.form_id + ' .hidden').click();
            };
        }
    }
};

{% load static %}

var tag = this;
var language = "{{ LANGUAGE_CODE }}";
var maxDescriptionLength = 600;

tag.resources = opts.resources;
tag.resourceCount = parseInt("{{ resource_count }}");

tag.buildExternalUrl = function(url) {
    if (url.slice(0,4) == "http") { return url; }
    else { return "http://" + url; }
}

tag.formatDate = function(iso_date) {
    if (iso_date) {
        try {
            return moment(iso_date).format('MMMM YYYY');
        } catch {
            return " - ";
        }
    } else {
        return " - ";
    }
}

tag.file_size_calc = function(file_size) {
    if (file_size) {
        return (file_size / (1024 * 1024)).toFixed(2) + 'mb';
    } else {
        return ' - ';
    }
}

tag.icon_directory = {
    // Microsoft Office formats
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '{% static "img/text_doc.svg" %}',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '{% static "img/spreadsheets.svg" %}',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '{% static "img/presentation.svg" %}',

    // Old MS Office formats
    'application/msword': '{% static "img/text_doc.svg" %}',
    'application/vnd.ms-excel': '{% static "img/spreadsheets.svg" %}',
    'application/excel': '{% static "img/spreadsheets.svg" %}',
    'application/vnd.ms-powerpoint': '{% static "img/presentation.svg" %}',
    'application/vnd.ms-project': '{% static "img/presentation.svg" %}',

    // OpenOffice or LibreOffice
    'application/vnd.oasis.opendocument.spreadsheet': '{% static "img/spreadsheets.svg" %}',
    'application/vnd.oasis.opendocument.text': '{% static "img/text_doc.svg" %}',
    'application/vnd.oasis.opendocument.presentation': '{% static "img/presentation.svg" %}',

    // OpenOffice
    'application/vnd.sun.xml.calc': '{% static "img/spreadsheets.svg" %}',
    'application/vnd.sun.xml.impress': '{% static "img/presentation.svg" %}',
    'application/vnd.sun.xml.writer': '{% static "img/text_doc.svg" %}',

    // Images (some common formats; not exhaustive)
    'image/png': '{% static "img/images.svg" %}',
    'image/jpeg': '{% static "img/images.svg" %}',
    'image/gif': '{% static "img/images.svg" %}',

    // PDF
    'application/pdf': '{% static "img/pdf.svg" %}',

    // VIDEO (some common formats; not exhaustive)
    'video/avi': '{% static "img/video-2.svg" %}',
    'video/mp4': '{% static "img/video-2.svg" %}',
    'video/mpeg': '{% static "img/video-2.svg" %}',
    'video/quicktime': '{% static "img/video-2.svg" %}',
};

tag.decodeFT = function(file_format) {
    if (file_format) {
        var icon = tag.icon_directory[file_format];
        if (icon) {
            return icon;
        } else if (file_format.slice(0,5) == 'video') {
            return '{% static "img/video-2.svg" %}';
        } else if (file_format.slice(0,5) == 'image') {
            return '{% static "img/images.svg" %}';
        } else {
            return '{% static "img/url-icon.svg" %}';
        }
    } else {
        return '{% static "img/url-icon.svg" %}';
    }
}

tag.on('mount', function() {
    tag.update();
});

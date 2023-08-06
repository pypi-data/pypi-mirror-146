/* {% load static %} */
/* global stores */
/* exported DocumentStore */


function DocumentStore(documents, choices) {
    var store = this;
    store.sortBy = 'id';
    riot.observable(store);
    store.choices = choices;
    store.el = 'documents';
    store.load(documents);

    store.urls = {
        read: function () { return '{% url "documents-list" %}?activity=' + stores.activityStore.activity.id; },
        create: function () { return '{% url "documents-list" %}?activity=' + stores.activityStore.activity.id; },
        update: function (document_id) { return '{% url "documents-detail" "XXXXX" %}'.replace('XXXXX', document_id) + '?activity=' + stores.activityStore.activity.id; },
        delete: function (document_id) { return '{% url "documents-detail" "XXXXX" %}'.replace('XXXXX', document_id) + '?activity=' + stores.activityStore.activity.id; }
    };

    store.on('document-uploaded', function (data) {
        store.load(data);
    });

    store.template = {
        activity: stores.activityStore.activity.id,
        categories: [''],
        date: moment().format('YYYY-MM-DD')
    };

    store.icons = {

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

        // Images
        'image/png': '{% static "img/images.svg" %}',
        'image/jpeg': '{% static "img/images.svg" %}',
        'image/gif': '{% static "img/images.svg" %}',

        // PDF
        'application/pdf': '{% static "img/pdf.svg" %}'
    };
}

{% load static %}

var tag = this;
tag.documents = opts.documents.sort(function(d1, d2) { return d1.last_modified <= d2.last_modified; });

// Dictionary from file_format to (icon, file category)
tag.doc_type_info = {
      // Document
      'application/vnd.sun.xml.writer': ["{% static 'img/text_doc.svg' %}", '.writer'],
      'application/vnd.oasis.opendocument.text': ["{% static 'img/text_doc.svg' %}", '.text'],
      'application/msword': ["{% static 'img/text_doc.svg' %}", '.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ["{% static 'img/text_doc.svg' %}", '.document'],

      // Spreadsheet
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ["{% static 'img/spreadsheets.svg' %}", '.sheet'],
      'application/vnd.ms-excel': ["{% static 'img/spreadsheets.svg' %}", '.xls'],
      'application/excel': ["{% static 'img/spreadsheets.svg' %}", '.xls'],
      'application/vnd.oasis.opendocument.spreadsheet': ["{% static 'img/spreadsheets.svg' %}", '.spreadsheet'],
      'application/vnd.sun.xml.calc': ["{% static 'img/spreadsheets.svg' %}", '.calc'],

      // Presentation
      'application/vnd.ms-powerpoint': ["{% static 'img/presentation.svg' %}", '.ppt'],
      'application/vnd.ms-project': ["{% static 'img/presentation.svg' %}", '.ppt'],
      'application/vnd.sun.xml.impress': ["{% static 'img/presentation.svg' %}", '.impress'],
      'application/vnd.oasis.opendocument.presentation': ["{% static 'img/presentation.svg' %}", '.presentation'],

      // Images
      'image/png': ["{% static 'img/images.svg' %}", '.png'],
      'image/jpeg': ["{% static 'img/images.svg' %}", '.jpeg'],
      'image/jpg': ["{% static 'img/images.svg' %}", '.jpg'],
      'image/gif': ["{% static 'img/images.svg' %}", '.gif'],

      // PDF
      'application/pdf': ["{% static 'img/pdf.svg' %}", '.pdf'], 
}

tag.on('mount', function() {
    tag.documents.forEach(function(d) {
        var default_doctype = ["{% static 'img/text_doc.svg' %}", ''];
        var doctype = tag.doc_type_info[d.file_type] || default_doctype;
        d.size = human_readable_size(d.size);
        d.size = d.size !== '0 KB' ? d.size : null;
        d.last_modified = moment(d.last_modified).format('YYYY-MM-DD')
        d.icon = doctype[0];  // file type is validated on upload
        d.type = doctype[1];
        d.is_image = (d.file_type ? d.file_type.indexOf('image') === 0 : false);
    });
    tag.images = tag.documents.filter(function(d) { return d.is_image; });
    tag.documents = tag.documents.filter(function(d) { return !d.is_image; });
    tag.has_documents = tag.images.length || tag.documents.length;
    tag.update();
});

/** Takes a filesize in bytes and returns the size in MB if the size is greater than 1MB
 *  else returns the size in KB.
 */
function human_readable_size(s) {
    var size_in_mb = s/(1 << 20);
    if (size_in_mb > 1) return size_in_mb.toFixed(2) + " MB";
    else return String(s >> 10) + " KB";
}

// {% load i18n %}
/* global opts characterLimit */

var tag = this;
tag.languages = opts.languages;
tag.collapsed_height = opts.collapsed_height || 0;
tag.hide_text = false;
tag.hide_toggles = true;
tag.editing = false;

// Helper functions for hiding/showing the character and word counts only when editing the text field
function wordcount_publish() {
    var $wordcounter = $('#' + opts.field_text_id + '_counts');
    var $publish = $('publish-button');
    var $cancel = $('cancel-button');
    if ($($publish, $cancel).click()) {
        $($wordcounter).addClass('hidden');
    } else {
        $($wordcounter).removeClass('hidden');
    }
    tag.update();
}

function wordcount_hide() {
    var $wordcounter = $('#' + opts.field_text_id + '_counts');
    var $pencil_editor = $('.icon-pencil');
    if ($($pencil_editor).click()) {
        $($wordcounter).removeClass('hidden');
    } else {
        $($wordcounter).addClass('hidden');
    }
    tag.update();
}

// Helper functions for hiding/showing background text when not enough space in the parent container available
tag.show_overflow = function() {
    var parent_element = $('#' + tag.opts.field_text_id);
    parent_element.css('height', '100%');
    parent_element.css('overflow', 'auto');
    parent_element.children('p').each(function () {
        this.style.display = 'block';
    });
    tag.hide_text = false;
}

tag.hide_overflow = function() {
    var total_height = 0;
    var parent_element = $('#' + tag.opts.field_text_id);
    parent_element.children('p').each(function () {
        total_height += this.clientHeight;
    });
    if (tag.collapsed_height >= total_height) {
        tag.show_overflow();
        tag.hide_toggles = true;
    } else {
        parent_element.css('height', tag.collapsed_height+'px');
        parent_element.css('overflow', 'hidden');
        tag.hide_toggles = false;
        tag.hide_text = true;
    }
}

tag.on('mount', function () {
    // {% get_current_language as LANGUAGE_CODE %}
    _select_language('{{ LANGUAGE_CODE }}');
    tag.hide_overflow();
    this.updateCounts();
});

tag.edit = function () {
    tag.show_overflow();
    tag.hide_toggles = true;
    var character_limit = new characterLimit();
    character_limit.limit = opts.character_limit;

    tag.editor = new MediumEditor('#' + opts.field_text_id, {
        toolbar: {
            buttons: ['orderedlist', 'unorderedlist']
        },
        extensions: {
            character_limit: character_limit
        }
    });

    tag.original_description = tag.editor.getContent();
    tag.editing = true;
    _select_language(tag.language);

    // Listen to editableInput events to update character/word count
    tag.editor.subscribe('editableInput', tag.updateCounts.bind(tag.editor));
    // Word count callout function
    wordcount_hide();
};

tag.save = function () {
    var new_description = tag.editor.getContent();
    // put the new description in the appropriate model
    var data = {};
    data[opts.model_field] = new_description.replace(/&nbsp;/g, ' ');

    data.language_code = tag.language;

    var xhr = $.ajax({
        data: data,
        method: 'PATCH',
        url: opts.update_endpoint,
        headers: { 'X-CSRFTOKEN': '{{ csrf_token }}' }
    });
    xhr.done(function () {
        tag.editor.destroy();
        tag.editing = false;
        opts.field_text[tag.language] = new_description.replace(/&nbsp;/g, ' ');
        _select_language('{{ LANGUAGE_CODE }}');
        tag.update();
    });
    tag.hide_overflow();
    wordcount_publish();
};

tag.discard = function () {
    tag.editor.setContent(tag.original_description);
    tag.editor.destroy();
    tag.editing = false;
    tag.update();
    tag.hide_overflow();
    wordcount_publish();
};

tag.updateCounts = function () {
    // Get the text from the appropriate div and count characters/words
    var current_description = tag.text_elem.text();
    tag.character_count = current_description.length;
    tag.update();
};

tag.select_language = function (e) {
    return _select_language(e.item.language_code);
};

function _select_language(language_code) {
    tag.language = language_code;
    tag.text_elem = $('#' + opts.field_text_id);

    // If there isn't a translation for the current language and not editing, show an arbitrary
    // existing translation.
    if (opts.field_text[tag.language]) {
        if (opts.field_text[tag.language].length > 0 || tag.editing) {
            tag.text_elem[0].innerHTML = opts.field_text[tag.language];
        } else {
            for (var key in opts.field_text) {
                if (opts.field_text[key].length > 0) {
                    tag.text_elem[0].innerHTML = opts.field_text[key];
                    break;
                }
            }
        }
    }
    tag.updateCounts();
    tag.update();
}

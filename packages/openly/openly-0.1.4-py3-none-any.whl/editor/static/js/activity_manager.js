/* eslint-disable vars-on-top */
$(document).ready(function () {
    var has_area_select = document.getElementById('activity-area-select2') !== null
    var area_lookups = has_area_select ? JSON.parse(document.getElementById('areaprojects-data').textContent) : {};
    function filter_activities() {
        var none_msg = $('div.none_msg')[0];
        // hide "No Activities" msg
        none_msg.style.display = 'none';

        var activities = $('#activity-list-card-holder > div:not(:first-child)');
        var title = $('#act-list-search-title')[0];
        var title_filter = title.value.toUpperCase();
        var status = $('#act-list-search-status')[0];
        var status_filter = status.options[status.selectedIndex].text.toUpperCase();
        var openly_status_filter = $('#act-list-search-openly-status')[0].value;
        var area_filter = has_area_select ? $('#activity-area-select2').find(':selected')[0].value : '-';  // value of the area select
        var area_filter_value = (area_filter === '-') ? '' : area_lookups[parseInt(area_filter, 10)] || []
        activities.each(function (index, a) {
            var a_title = a.querySelectorAll('span.card_title')[0];
            var a_status = a.querySelectorAll('span#activity_status_name')[0];
            var a_openly_status = a.querySelector('.card_icon_status .center-icon');
            var a_id = a.querySelectorAll('span.card_id')[0];
            var title_test = (title_filter != '') ? a_title.innerText.toUpperCase().indexOf(title_filter) > -1 : true;
            var status_test = (status.selectedIndex != 0) ? (a_status.innerText.toUpperCase() == status_filter) : true;
            var openly_status_test = (openly_status_filter !== '0') ? a_openly_status.classList.contains(openly_status_filter) : true;
            var area_test = (area_filter_value !== '') ? area_filter_value.indexOf(a_id.innerText) > -1 : true;
            if (title_test && status_test && openly_status_test && area_test) {
                a.style.display = '';
            } else {
                a.style.display = 'none';
            }
        });
        // check if any results left un-hidden
        var visable_activities = $('#activity-list-card-holder > div:not([style*="display: none"])').length;
        if (visable_activities > 0) {
            // hide "No Activities" msg
            none_msg.style.display = 'none';
        } else {
            // show 'No Activities' msg
            none_msg.style.display = '';
        }
    }

    var delay = (function () {
        var timer = 0;
        return function (callback, ms) {
            clearTimeout(timer);
            timer = setTimeout(callback, ms);
        };
    }());

    $('#act-list-search-status,#act-list-search-openly-status').on('change', function () {
        filter_activities();
    });

    $('#act-list-search-title').keyup(function () {
        delay(function () {
            filter_activities();
        }, 100);
    });

    var toggleImport = function () {
        $('#import-iati-btn').toggleClass('active');
        $('#cbp-spmenu-s2').toggleClass('cbp-spmenu-open');
        $('#leftPanel').toggleClass('hidden');
        $('#centrePanel').toggleClass('col-sm-7');
        $('#centrePanel').toggleClass('col-sm-5');
        $('#localTitle').toggleClass('hidden');
        $('#rightPanel').toggleClass('hidden');
    };

    // toggle import panel
    $('#import-iati-btn').click(toggleImport);
    $('#hideImport').click(toggleImport);

    // transfer activity card to left panel
    var importCard = function (card) {
        card.hide(500, function () {
            card.find('.card_title').hide();
            card.find('.card_link').show();
            card.find('.status_display').html('Draft');
            card.find('.import_buttons').hide();
            card.insertAfter($('#localTitle'));
            card.show(500);
        });
    };

    function insertMessage(text, type) {
        var className = 'message bold text-' + type + ' btn-' + type;
        var pMessage = $('<p />').addClass(className)
            .css('padding', '10px')
            .html(text);
        setTimeout(
            function () {
                pMessage.remove();
            },
            10 * 1000
        );
        $('#ajax_messages').append(pMessage);
    }

    // import single activity
    $('.btn-newimport').on('click', function () {
        var clicked = $(this);
        var card = clicked.parents('.activity_card');
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            success: function () {
                importCard(card);
            },
            error: function (data) {
                insertMessage('Import Failed', 'warning');
            }
        });
    });

    // import all activities
    $('.btn-importall').on('click', function () {
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            success: function () {
                var time = 0;
                $('#rightPanel .activity_card').each(function (index, element) {
                    time += 500;
                    setTimeout(function () { importCard($(element)); }, time);
                });
                setTimeout(toggleImport, time);
            },
            error: function (data) {
                insertMessage('Import Failed', 'warning');
            }
        });
    });

    $('a.expand_card').on('click', function () {
        $(this).parent().next('.collapse_card').collapse('toggle');
        if ($(this).text() == 'See Preview') {
            $(this).html('Hide Preview<i class="ion-chevron-up">');
        } else {
            $(this).html('See Preview<i class="ion-chevron-down">');
        }
    });

    $('#compareActivities').on('shown.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var local_id = button.data('local_id');
        var iati_id = button.data('iati_id');
        var local = $('div[data-pk="' + local_id + '"]').clone();
        var iati = $('div[data-pk="' + iati_id + '"]').clone();
        $('#localActivity').empty().html(local);
        $('#iatiActivity').empty().html(iati);
    });

    if (has_area_select){
        $('#activity-area-select2').select2({
            theme: 'bootstrap',
            templateResult: function (data) {
                if (!data.element) { return data.text; }
                var $element = $(data.element);
                var $wrapper = $('<div></div>');
                $wrapper.addClass('select-area-level-'+data.element.dataset.level);
                $wrapper.text(data.text);
                return $wrapper;
            }
        }).on('change.select2', filter_activities);
    }
});

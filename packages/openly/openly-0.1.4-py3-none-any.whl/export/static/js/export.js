function updateMissingDatesDisplay(val) {
    if (val === 'activities_without_date') {
        $('#missing_dates_group').show();
    } else {
        $('#missing_dates_group').hide();
    }
}

function updateDisplay(val) {
    $('#development_partner_group').find(':selected').prop('selected', false);
    $('#sector_working_group_group').find(':selected').prop('selected', false);
    $('#sector_group').find(':selected').prop('selected', false);
    $('#location_group').find(':selected').prop('selected', false);
    $('#id_activity_status').iCheck('check');

    var form_group_toggles = {
        '.input-daterange': 'show',
        '#development_partner_group': 'hide',
        '#sector_working_group_group': 'hide',
        '#sector_group': 'hide',
        '#location_group': 'hide',
        '#report_activitystatus_group': 'hide',
        '#finance_type_group': 'hide',
        '#aid_type_category_group': 'hide',
        '#data_quality_type_group': 'hide',
        '#missing_dates_group': 'hide',
    };

    if (val.match(/summary/)) {
        form_group_toggles['#finance_type_group'] = 'show';
        form_group_toggles['#aid_type_category_group'] = 'show';
    } else if (val.match(/development_partner_report/)) {
        form_group_toggles['#development_partner_group'] = 'show';
        form_group_toggles['#report_activitystatus_group'] = 'show';
        form_group_toggles['#finance_type_group'] = 'show';
        form_group_toggles['#aid_type_category_group'] = 'show';
        form_group_toggles['.input-daterange'] = 'hide';
        form_group_toggles['#aid_type_category_group'] = 'show';
    } else if (val.match(/sector_report/)) {
        form_group_toggles['#sector_group'] = 'show';
        form_group_toggles['#report_activitystatus_group'] = 'show';
        form_group_toggles['#finance_type_group'] = 'show';
        form_group_toggles['#aid_type_category_group'] = 'show';
    } else if (val.match(/location_report/)) {
        form_group_toggles['#location_group'] = 'show';
        form_group_toggles['#report_activitystatus_group'] = 'show';
        form_group_toggles['#finance_type_group'] = 'show';
        form_group_toggles['#aid_type_category_group'] = 'show';
    } else if (val.match(/sector_working_group/)) {
        form_group_toggles['#sector_working_group_group'] = 'show';
        form_group_toggles['#report_activitystatus_group'] = 'show';
        form_group_toggles['#finance_type_group'] = 'show';
        form_group_toggles['#aid_type_category_group'] = 'show';
    } else if (val.match(/annual_breakdown/)) {
        form_group_toggles['#report_activitystatus_group'] = 'show';
        form_group_toggles['#finance_type_group'] = 'show';
        form_group_toggles['#aid_type_category_group'] = 'show';
    } else if (val.match(/data_quality/)) {
        form_group_toggles['.input-daterange'] = 'hide';
        form_group_toggles['#data_quality_type_group'] = 'show';
        if ($('select#id_data_quality_type').val() === 'activities_without_date') {
            form_group_toggles['#missing_dates_group'] = 'show';
        }
    } else if (val.match(/development_partner_profile/)) {
        form_group_toggles['.input-daterange'] = 'hide';
    }

    for (var form_group in form_group_toggles) {
        // equivalent to, for example: $('#data_quality_type_group').hide()
        $(form_group)[form_group_toggles[form_group]]();
    }

}

$(document).ready(function(){
    $('.input-daterange').datepicker({
        format: "M yyyy",
        startView: 1,
        minViewMode: 1
    });
    $('input').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue',
        increaseArea: '20%'
    });
    $('button[type=submit]').on('click', function () {
        var $btn = $(this).button('loading');
        window.setTimeout(function(){
            $btn.button('reset');
        }, 1000);
    });

    updateDisplay($('select#id_report_type').val());
    // on change of report type show extra groups
    $('select#id_report_type').on('change', function() {
        updateDisplay($(this).val());
    });
    $('select#id_data_quality_type').on('change', function() {
        updateMissingDatesDisplay($(this).val());
    });
});

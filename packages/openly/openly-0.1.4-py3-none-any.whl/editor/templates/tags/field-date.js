/** @class field-date */
/* global moment */
var tag = this;
tag.formatted_date = '0000-00-01';

function getDatepickerOpts() {
    var datepicker_opts = $.extend({
        orientation: 'top left',
        startView: 1,
        autoclose: true,
        format: 'yyyy-mm-dd',
        clearBtn: true

    }, tag.opts.datepicker_opts);

    if (tag.opts.validate_date_is_past) {
        tag.datepicker_opts.endDate = '0d';
    }
    return datepicker_opts;
}

function intializeDatePicker() {
    if (!($('p.form-control', tag.root))[0]) { return; }
    tag.datepicker = $('p.form-control', tag.root).datepicker(getDatepickerOpts());
    tag.datepicker.datepicker("setDate", moment(tag.data).format('YYYY-MM-DD'));
    tag.datepicker.on('changeDate', function () {
        var date = $(this).datepicker('getUTCDate');
        var iso_date = date ? moment(date).format('YYYY-MM-DD') : '';
        tag.bystring(tag.path, { data: iso_date });
        setDisplayDate()
    });
    tag.datepicker.on('clearDate', function () {
        tag.bystring(tag.path, { data: '' });
        setDisplayDate()
    });
}

function setDisplayDate(){
    if (_.isUndefined(tag.path)){return};
    var momentized = moment(tag.bystring(tag.path));
    var formatted_date = (momentized.isValid() ? momentized.format('D MMM YYYY') : '');
    if (formatted_date != tag.formatted_date){
        tag.validate();
        tag.update({formatted_date:formatted_date});
    }
    return tag.formatted_date
}

tag.setDisplayDate = setDisplayDate;

tag.mixin('SerializerMixin');
tag.mixin('FormFieldMixin');
tag.mixin('ValidationMixin');

tag.on('mount', function () {  
    if (!tag.datepicker) { 
        intializeDatePicker(); 
        setDisplayDate(); 
    } });
tag.on('updated', function () { if (!tag.datepicker) { intializeDatePicker(); setDisplayDate(); } });

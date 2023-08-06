/* globals moment */

var tag = this;

function get_year() {
    var date = tag.opts.period.period_end;
    return moment(date).format('YYYY');
}

function get_month() {
    var date = tag.opts.period.period_end;
    return moment(date).format('MMMM');
}

function is_positive() {
    var ascending = tag.opts.ascending;
    var period = tag.opts.period;
    var period_set = tag.opts.period_set;
    return (tag.opts.ascending && period.actual >= period_set[0].actual) || (!ascending && period.actual <= period_set[0].actual);
}


tag.on('mount', function () {
    if (_.isUndefined(_.get(tag, 'opts.period'))){ return }
    tag.update({
        value: _.round(_.get(tag.opts, 'period.actual', 0), 2),
        year: get_year(),
        month: get_month(),
        is_positive: is_positive()
    });
});


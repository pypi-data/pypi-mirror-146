{% load i18n %}
{% load profiles_filters %}

var aid_type_category_breakdown = _.orderBy({{aid_type_category_breakdown|js}}, 1, 'asc');
_.each(aid_type_category_breakdown, function(_d) { _d[0].length < 25 ? _d[0]=_d[0] : _d[0]=_d[0].split(' ').slice(0,2) + "..." })
var self = this;

function categoryColor(category) {
    var defaultColor = '#CCC';
    var scale = 'GnBu'; // ColorBrewer codebase
    var length = _.clamp(aid_type_category_breakdown.length, 3,9); // Ensure we stay within the bounds
    var scale = window.colorbrewer[scale][length];
    var index = _.findIndex(aid_type_category_breakdown, function(i){return i[0] === category});
    if (index === -1) return defaultColor;
    return scale[index]
}

function statusColor(statuscode) {
    var colors = {
        'pipeline identification': '#3bafda',
        implementation: '#37bc9b',
        completion: '#ccd1d9',
        'post completion': '#A8D9EA'
    };
    return _.get(colors, _.lowerCase(statuscode), '');
}

function draw_category_donut() {
    c3.generate({
        bindto: '#aid_type_category_breakdown',
        data: {
            columns: _.map(aid_type_category_breakdown, function (_d) {
                return [ _d[0], _d[1] ];
            }),
            type: 'donut',
            color: function (color, code) {
                var colorcode = typeof code === 'string' ? code : code.id;
                return categoryColor(colorcode);
            }
        },
        donut: {
            title: 'Categories',
            label: {
                format: function (value) {
                    return accounting.formatMoney(value, '', 0);
                },
                threshold: 0.04
            }
        }
    });
}

function render_activity_status_percentages() {
    c3.generate({
        bindto: '#activities_status_percentage',
        tooltip: {
            format: {
                name: function (name, ratio, id, index) {
                    return name + ':';
                }
            }
        },
        data: {
            columns: self.activity_status_percentages,
            type: 'donut',
            color: function (color, code) {
                var colorcode = typeof code === 'string' ? code : code.id;
                return statusColor(colorcode);
            }
        },
        donut: {
            title: 'Status'
        }
    });
}

function render_transactions_by_year() {
    var data = self.transactions_by_year;
    c3.generate({
        bindto: '#activities_by_year',
        data: {
            json: data,
            keys: {
                x: 'year',
                value: ["{% trans 'Commitments' %}", "{% trans 'Disbursements' %}", "{% trans 'Expenditures' %}", "{% trans 'Others' %}"]
            },
            type: 'area-spline'
        },
        tooltip: {
            format: {
                value: function (value, ratio, id, index) {
                    return 'USD $' + data[index][id + '_Pretty'];
                }
            }
        },
        axis: {
            x: {
                type: 'categorized'
            },
            y: {
                tick: {
                    format: d3.format('s')
                }
            }
        },
        size: { height: 280 }
    });
}

function render_activity_statuses() {
    var data = self.activity_status_data;
    c3.generate({
        bindto: '#activities_by_status',
        data: {
            json: data,
            type: 'bar',
            keys: {
                x: 'name',
                value: ['value']
            },
            colors: {
                value: function (d) {
                    var d_;
                    var color;
                    if (d.index === undefined) { return false; }
                    d_ = data[d.index];
                    color = statusColor(d_.code);
                    return color;
                }
            }
        },
        legend: {
            show: false
        },
        tooltip: {
            format: {
                name: function (d) { return ''; },
                value: function (value, ratio, id, index) {
                    var d = data[index];

                    return '<b>' + d.activities
                            + "</b> {% trans 'Activities'%} - "
                            + '<b>USD $' + d.pretty+ '</b>';
                }
            }
        },
        axis: {
            x: {
                type: 'categorized',
                tick: {
                    rotate: 35,
                    multiline: false
                }
            },
            y: {
                tick: {
                    format: d3.format('s')
                }
            }
        },
        bar: {
            width: {
                ratio: 0.25
            }
        },
        size: { height: 310
        },
        padding: {
            top: 8,
            bottom: 30,
            right: 60,
            left: 35
        }
    });
}

self.aid_type_category_breakdown = aid_type_category_breakdown;
self.activity_status_data = {};
self.activity_status_percentages = {};
self.transactions_by_year = {};

self.on('mount', function () {
    RiotControl.trigger('request_activities_status_values');
    RiotControl.trigger('request_transactions_by_year');
    $('#status_value').popover({ placement: 'top' });
    $('#category_value').popover({ placement: 'top' });
    $('#status_percent').popover({ placement: 'top' });
    $('#cumulative_com_disb').popover({ placement: 'top' });
    $('#finances').popover({ placement: 'top' });
});

RiotControl.on('show_finances', function () {
    if (self.activity_status_data) { render_activity_statuses(); }
    if (self.activity_status_percentages) { render_activity_status_percentages(); }
    if (self.transactions_by_year) { render_transactions_by_year(); }
    draw_category_donut();
});

RiotControl.on('transactions_by_year', function (transactions_by_year) {
    self.update({ transactions_by_year: transactions_by_year });
    if (self.transactions_by_year) { render_transactions_by_year(); }
});

RiotControl.on('activities_status_values', function (activity_status_data) {
    self.update({
        activity_status_data: activity_status_data,
        activity_status_percentages: _.map(activity_status_data, function (val) { return [val.name, val.value]; }),
        loading: false
    });
    if (self.activity_status_data) { render_activity_statuses(); }
    if (self.activity_status_percentages) { render_activity_status_percentages(); }
    draw_category_donut();
});

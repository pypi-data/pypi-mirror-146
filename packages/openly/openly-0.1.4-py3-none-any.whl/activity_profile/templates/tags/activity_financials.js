/* {% load i18n %} */
/* {% load profiles_filters %} */

var self = this;

self.on('mount', function() {

    c3.generate({
        bindto: '#arcChart',
        data: { columns: [ ['Disbursed', self.opts.percent_disbursed] ], type: 'gauge' },
        size: { height: 250 },
        padding: { bottom: 0 },
        color: { pattern: ['#06aae8', '#01a3e0', '#01a3e0', '#01a3e0'], threshold: { values: [30, 60, 90, 100] } }
    });

    c3.generate({
        bindto: '#transactions_by_month_year',
        data: {
            json: self.opts.transactions_by_month_year,
            keys: {
                x: 'month_year',
                value: ["{% trans 'Commitments' %}", "{% trans 'Disbursements' %}", "{% trans 'Expenditures' %}", "{% trans 'Others' %}"]
            },
            type: 'area-spline'
        },
        tooltip: {
            format: {
                value: function (value, ratio, id, index) {
                    return 'USD $' + self.opts.transactions_by_month_year[index][id + '_Pretty'];
                }
            }
        },
        axis: {
            x: {
                type: 'categorized',
                tick: {
                    rotate: 30
                },
                height: 50
            },
            y: {
                tick: {
                    format: d3.format('s')
                }
            }
        },
        size: { height: 280 }
    });

    self.update();
});

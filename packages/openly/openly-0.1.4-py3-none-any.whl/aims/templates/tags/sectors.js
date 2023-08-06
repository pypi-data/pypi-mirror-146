/* {% load static %} */
var tag = this;
var source = JSON.parse("{{ sectors|escapejs }}");
tag.commitments_help_text = false;

function dac5to3(code) {
    return Number(String(code).substr(0, 3));
}

function load_data() {
    /* opts.sectors is expected to be a set of dac3 or dac5 sectors with "code" and "name" properties */
    if (source.length > 0 && source[0].hasOwnProperty('dollars')) {
        var sectors = _.clone(source);
        // convert string to integer for sorting by dollar values
        sectors = _.map(sectors, function(s){ s.dollars = parseFloat(s.dollars); return s; });
        // sort and reverse to get values from largest to smallest
        sectors = _.sortBy(sectors, 'dollars').reverse();
    } else {
        var sectors = _.sortBy(_.clone(source), 'code');
    }

    _.each(sectors, function (s) {
        if (s.dollars) {
            tag.commitments_help_text = true;
            s.dollars = accounting.formatMoney(s.dollars, '', 0);
        }
        var code = dac5to3(s.code);
        if (code >= 111 && code < 120) {
            s.icon = "{% static 'img/sectors_schooling.svg' %}";
        } else if (code >= 120 && code < 130) {
            s.icon = "{% static 'img/sectors_health.svg' %}";
        } else if (code >= 130 && code < 140) {
            s.icon = "{% static 'img/sectors_population_policies.svg' %}";
        } else if (code >= 140 && code < 150) {
            s.icon = "{% static 'img/sectors_water_sanitation.svg' %}";
        } else if (code >= 150 && code < 160) {
            s.icon = "{% static 'img/sectors_government_society.svg' %}";
        } else if (code >= 160 && code < 170) {
            s.icon = "{% static 'img/sectors_social_infrastructure.svg' %}";
        } else if (code === 210) {
            s.icon = "{% static 'img/sectors_transport.svg' %}";
        } else if (code === 220) {
            s.icon = "{% static 'img/sectors_ict.svg' %}";
        } else if (code >= 230 && code <= 236) {
            s.icon = "{% static 'img/sectors_energy.svg' %}";
        } else if (code === 240) {
            s.icon = "{% static 'img/sectors_banking.svg' %}";
        } else if (code === 250) {
            s.icon = "{% static 'img/sectors_business.svg' %}";
        } else if (code === 311) {
            s.icon = "{% static 'img/sectors_agriculture.svg' %}";
        } else if (code === 312) {
            s.icon = "{% static 'img/sectors_forestry.svg' %}";
        } else if (code === 313) {
            s.icon = "{% static 'img/sectors_fishing.svg' %}";
        } else if (code === 321) {
            s.icon = "{% static 'img/sectors_industry.svg' %}";
        } else if (code === 322) {
            s.icon = "{% static 'img/sectors_extractives.svg' %}";
        } else if (code === 323) {
            s.icon = "{% static 'img/sectors_reconstruction.svg' %}";
        } else if (code === 331) {
            s.icon = "{% static 'img/sectors_trade.svg' %}";
        } else if (code === 332) {
            s.icon = "{% static 'img/sectors_tourism.svg' %}";
        } else if (code === 410) {
            s.icon = "{% static 'img/sectors_general_envrionmental_protection.svg' %}";
        } else if (code === 430) {
            s.icon = "{% static 'img/sectors_multisector.svg' %}";
        } else if (code === 510) {
            s.icon = "{% static 'img/sectors_budget.svg' %}";
        } else if (code === 520) {
            s.icon = "{% static 'img/sectors_food_aid_security.svg' %}";
        } else if (code === 530) {
            s.icon = "{% static 'img/sectors_import.svg' %}";
        } else if (code === 600) {
            s.icon = "{% static 'img/sectors_debt.svg' %}";
        } else if (code === 720) {
            s.icon = "{% static 'img/sectors_food_aid.svg' %}";
        } else if (code === 730) {
            s.icon = "{% static 'img/sectors_reconstruction.svg' %}";
        } else if (code === 740) {
            s.icon = "{% static 'img/sectors_disaster_prevention.svg' %}";
        } else if (code === 910) {
            s.icon = "{% static 'img/sectors_admin.svg' %}";
        } else if (code === 920) {
            s.icon = "{% static 'img/sectors_ngo.svg' %}";
        } else if (code === 930) {
            s.icon = "{% static 'img/sectors_refugee.svg' %}";
        } else if (code === 998) {
            s.icon = "{% static 'img/sectors_general.svg' %}";
        }
    });
    return sectors;
}

tag.on('mount', function () {
    tag.update({ sector_class: tag.opts.sector_class, sectors: load_data() });
});


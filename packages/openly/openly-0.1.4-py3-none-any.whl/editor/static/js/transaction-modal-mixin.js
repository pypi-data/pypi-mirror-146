/* exported TransactionModalMixin */
var TransactionModalMixin = {
    init: function () {
        var m = this;

        var default_classes = {
            label: 'col-xs-3 control-label',
            select: 'col-xs-6',
            outer: 'form-group',
            input: 'col-xs-6',
            date_label: 'col-xs-1 control-label',
            date: 'col-xs-2',
            dropdown: ''
        };

        /* Set organisations as per https://github.com/catalpainternational/openly_mohinga/issues/301 */
        m.organisations = {
            funding_list: _(stores.transactionStore.transactions).map('provider_organisation').uniq().value(),
            accountable_list: _(stores.activityStore.activity.participating_organisations).filter({ role: { code: 'Accountable' } }).map('organisation.code').value(),
            implementing_list: _(stores.activityStore.activity.participating_organisations).filter({ role: { code: 'Implementing' } }).map('organisation.code').value(),
            reporting: stores.activityStore.activity.reporting_organisation.code
        };

        m.organisations.funding_initial = _.first(m.organisations.funding_list);
        m.organisations.accountable_initial = _.first(m.organisations.accountable_list);
        m.organisations.implementing_initial = _.first(m.organisations.implementing_list);

        m.store = stores.transactionStore;
        m._initial = null;
        m.values = {};
        m.validations = {};
        m.classes = _.extend(default_classes, m.classes, m.opts.classes);
        m.on('mount', function () {
            m.modal = $('.modal', m.root);
            m.modal.on('show.bs.modal', function () { m.opts.show = true; m.trigger('show_bs_modal'); });
            m.modal.on('shown.bs.modal', function () { m.opts.show = true; m.trigger('shown_bs_modal'); });
            m.modal.on('hide.bs.modal', function (e) { if (!$(e.target).hasClass('no-hide-bs-modal')) { m.opts.show = false; m.trigger('hide_bs_modal'); } });
        });

        m.on('setdropdown', function (event, data, child_tag) {
            _.set(m.values, child_tag.opts.path, _.has(data, 'code') ? data.code : data);
            m.update();
        });

        m.on('update', function onUpdate() {
            m.setDefaults();
            m.setVisibility();
            m.setSaveEnabled();
        });
        /* Handle events from child tags to "set" a value */
        m.on('set', function setter(field, value) { m.values[field] = value; m.trigger('validate', m.values, field); });

        m.on('shown_bs_modal', function () { m.trigger('validate_all'); });
        m.on('validate_all', function () {
            _.each(_.keys(m.values), function (field) { m.trigger('validate', m.values, field); });
        });
        m.on('validate', function (values, field) { _.invoke(m.validationFunctions, field, values[field], field); m.update(); });
        m.on('setValidation', function (name, level, message) {
            if (!_.isEqual((_.get(m.validations, name)), { level: level, message: message })) {
                m.validations[name] = { level: level, message: message };
                m.setSaveEnabled();
                m.update();
            }
        });
        m.on('unSetValidation', function (name) {
            _.unset(m.validations, name);
            m.setSaveEnabled();
            m.update();
        });
        m.on('createBackup', function () {
            if (_.isNull(m._initial)) {
                m._initial = _.cloneDeep(m.values);
            }
        });

        m.on('restoreBackup', function () {
            if (_.isNull(m._initial)) { return; }
            m.values = _.cloneDeep(m._initial);
            m._initial = null;
        });
    },

    setDefaults: function setDefaults() {
        var a = stores.activityStore.activity;
        var m = this;
        var default_fields = ['currency', 'finance_type', 'flow_type', 'aid_type', 'tied_status'];

        var defaults = {};
        m.values.activity = a.id;

        /* extend the transaction fields with activity defaults */
        _(default_fields).each(function (field) { defaults[field] = a['default_' + field].code; });

        /* if the activity does not have a default currency, assume we're using USD. Currency is a required field for value calculation. */
        defaults.currency = defaults.currency || 'USD';

        /* set the transaction date fields to today */
        _(['value_date', 'transaction_date']).each(function (field) { defaults[field] = ''; });
        /* set organisation fields */
        defaults.provider_organisation = m.organisations.funding_initial;
        defaults.receiver_organisation = m.organisations.implementing_initial;
        _.defaults(m.values, defaults);
    },

    setVisibility: function setVisibility() {
        var m = this;
        var modal_shown = m.modal.hasClass('in');
        if (m.opts.show && !modal_shown) {
            /* Create a backup here */
            m.trigger('createBackup');
            m.modal.modal('show');
        } else if (!m.opts.show && modal_shown) {
            /* Reset fields on hide */
            $('field-dropdownselect', m.root).each(function (t, el) { el._tag.update({ chosen: undefined }); });
            m.modal.modal('hide');
        }
    },

    /* sets a flag for whether save is enabled or not */
    setSaveEnabled: function setSaveEnabled() {
        var m = this;
        var saveEnabled = _.keys(m.validations).length === 0;
        if (!_.isEqual(m.saveEnabled, saveEnabled)) { m.update({ saveEnabled: saveEnabled }); }
    },

    assign: function (data) {
        _.assign(this.values, data);
    },

    toggle: function toggle(data, show) {
        var m = this;
        _.unset(m.values, 'id');
        m.setDefaults();
        if (data) { m.assign(data); }
        m.opts.show = _.isUndefined(show) ? !m.opts.show : show;
        m.update();
    },

    hide: function (data, keep) {
        var m = this;
        m.toggle(data, false);
        if (!keep) { m.trigger('restoreBackup'); }
        m.values = {};
    },

    save: function save(subtag) {
        var m = this;
        var formData = _(subtag.refs).mapValues('value').value();
        var data = _.clone(m.values);
        _.assign(data, formData);

        if (_.has(data, 'id')) {
            m.store.update(m, data); m.hide(undefined, true);
        } else {
            m.store.create(m, data); m.hide(undefined, true);
        }
        m.values = {};
    }
};

riot.mixin('TransactionModalMixin', TransactionModalMixin);

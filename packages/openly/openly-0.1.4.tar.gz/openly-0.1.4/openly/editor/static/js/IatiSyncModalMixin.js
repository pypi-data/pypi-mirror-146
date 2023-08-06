/* exported IatiSyncModalMixin */
var IatiSyncModalMixin = {
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

        m.store = stores.OipaLinkStore;
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
        m.on('set', function setter(field, value) { m.values[field] = value; console.log(field, value); console.log(m.values); m.trigger('validate', m.values, field); });

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
        m.values.openly_iati_id = a.id;
        m.values.B = null;
        m.values.C = null;
        m.values.D = null;
        m.values.O = null;
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
        m.store.update(m, data);
        m.hide(undefined, true);
        m.values = {};
    },

    breakUp: function breakUp(subtag) {
        var m = this;
        var formData = _(subtag.refs).mapValues('value').value();
        var data = _.clone(m.values);
        _.assign(data, formData);
        m.store.delete(m, data);
        m.hide(undefined, true);
    }
};

riot.mixin('IatiSyncModalMixin', IatiSyncModalMixin);

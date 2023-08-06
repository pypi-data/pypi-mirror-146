/* eslint no-underscore-dangle: 0 */
/* eslint no-console: 0 */
/* exported StoreMixin */

// no-console for dev work on groupvalidation
/**
 * @mixin
 */
var StoreMixin = {

    _delete_paths: [],
    _update_paths: [],
    _create_paths: [],
    _validation_failed_paths: [],
    tag_registry: {},
    group_validation: [],

    /**
     * Return the validation paths which have failed
     * @returns {Array}
     */
    get_validation_failed_paths: function return_paths() {
        return this._validation_failed_paths;
    },

    get_validation_failed_paths_startwith: function return_paths(path) {
        var paths = this.get_validation_failed_paths();
        var filtered_paths = _.filter(paths, function is_child_of(child) {
            return _.startsWith(child, path);
        });
        return filtered_paths;
    },

    /**
     * Return an empty element - an Activity is an object, while a Transaction is in an array
     * @returns {object|array}
     */
    get_root_element_type: function () {
        if (this.root_element_type === 'object') {
            return {};
        }

        if (this.root_element_type === 'array') {
            return [];
        }

        return {};
    },

    changed_tags: function () {
        return _.filter(
            _.flatten(_.values(this.tag_registry)),
            { value_has_changed: true }
        );
    },
    reset_tags_changed: function () {
        _.each(this.changed_tags(), function (changed) { changed.value_has_changed = false; });
    },

    /**
     * Loads data into the store
     * @memberof StoreMixin
     * @method load
     */
    load: function (/** object */ data) {
        // Unmount any child tags to prevent validation errors which should not be showing
        if (_.isFunction(this.list_child_tags)) {
            _(this.list_child_tags()).each(function (i) {
                i.unmount();
            });
        }

        // Specify "sortBy" in the Store to sort data by a given property
        if (this.sortBy) {
            data = _.sortBy(data, this.sortBy);
        }
        this._initial = _.cloneDeep(data);
        this[this.el] = _.cloneDeep(data);
        this._delete_paths = [];
        this._update_paths = [];
        this._create_paths = [];
        this._validation_failed_paths = [];
        this.reset_tags_changed();
        this.trigger(this.el + '_restored');
    },

    /** Synonymn for load
     * @param data
     */
    load_data: function (data) {
        return this.load(data);
    },

    /**
     * Loads a "partial" update into the store
     * @memberof StoreMixin
     * @method partial_load
     */
    partial_load: function (/** object */ data) /** callback */ {
        this[this.el] = _.extend(this[this.el], data);
        this._initial = $.extend(true, this.get_root_element_type(), this[this.el]);
        this._delete_paths = [];
        this._update_paths = [];
        this._create_paths = [];
        this._validation_failed_paths = [];
        this.trigger(this.el + '_restored');
    },

    /**
     * Restores the original data of the store, undoing any changes which have not been saved to the server yet
     * @memberof StoreMixin
     * @method restore
     */
    restore: function () {
        this.load(this._initial);
        this.trigger(this.el + '_restored');
        this._delete_paths = [];
        this._update_paths = [];
        this._create_paths = [];
        this._validation_failed_paths = [];
    },

    /**
     * Pass a path instance to check whether a path reference is in one of the create, delete or update queues
     * to the list of failed validation tags.
     * @memberof StoreMixin
     * @method path_status
     * @param path
     * @return {string}
     */
    path_status: function (path) {
        /* Return an indication of whether something is going to be removed, edited or created */
        var a = path.split('.');
        var ancestor_path = '';

        /* Validation errors should take priority */
        while (a.length > 0) {
            ancestor_path += a.shift();
            if (this._validation_failed_paths.indexOf(ancestor_path) !== -1) {
                return 'validation';
            }

            ancestor_path += '.';
        }

        a = path.split('.');
        ancestor_path = '';
        while (a.length > 0) {
            ancestor_path += a.shift();
            if (this._delete_paths.indexOf(ancestor_path) !== -1) {
                return 'delete';
            }

            if (this._create_paths.indexOf(ancestor_path) !== -1) {
                return 'create';
            }

            if (this._update_paths.indexOf(ancestor_path) !== -1) {
                return 'update';
            }

            ancestor_path += '.';
        }

        return 'unchanged';
    },

    /**
     * Add a tag's path to the list of items to be updated
     * @param tag {object} : The tag object to retrieve a path to be updated from
     */
    update_tag: function (tag) {
        return this._add_update_tag(tag);
    },

    /**
     * Add an indication whether ot not this particular path has changed
     * @param path {string} : Path the update for example transaction[0].value
     */
    update_path: function (path) {
        return this._add_update_path(path);
    },

    /**
     * Add an item's index to the list of items to be updated
     * @param item {object} : An item from a RiotJS "each"
     */
    update_item: function (item) {
        var index = this[this.el].indexOf(item);
        var path = this.el + '[' + index + ']';
        this.update_path(path);
    },

    _add: function (array, value) {
        if (_.indexOf(array, value) === -1) {
            array.push(value);
        }
    },

    _toggle: function (array, value) {
        if (_.indexOf(array, value) !== -1) {
            _.pull(array, value);
        } else {
            array.push(value);
        }
    },

    /**
     * Adds or removes a path to the "delete paths" list of elements to be removed from the store before it is saved
     * @param tag
     * @private
     */
    _add_delete_tag: function (tag) {
        this._add_delete_path(tag.absolute_path());
    },

    _add_delete_path: function (path) {
        this._add(this._delete_paths, path);
    },

    _remove_delete_tag: function (tag) {
        this._remove_delete_path(tag.path);
    },

    _remove_delete_path: function (path) {
        _.pull(this._delete_paths, path);
    },

    _toggle_delete_tag: function (tag) {
        this._toggle_delete_path(tag.path);
    },

    _toggle_delete_path: function (path) {
        this._toggle(this._delete_paths, path);
    },

    /**
     * Adds a path to the list of paths to be updated so that we can give a "preview" of modified elements
     * @param tag
     * @private
     */
    _add_update_tag: function (tag) {
        this._add_update_path(tag.absolute_path());
    },

    _add_update_path: function (path) {
        this._add(this._update_paths, path);
    },

    _remove_update_tag: function (tag) {
        this._remove_update_path(tag.path);
    },

    _remove_update_path: function (path) {
        _.pull(this._update_paths, path);
    },

    _toggle_update_tag: function (tag) {
        this._toggle_update_path(tag.path);
    },

    _toggle_update_path: function (path) {
        this._toggle(this._update_paths, path);
    },

    /**
     * Adds a path to the list of paths to be created so that we can give a "preview" of modified elements
     * @param tag
     * @private
     */
    _add_create_tag: function (tag) {
        this._add_create_path(tag.absolute_path());
    },

    _add_create_path: function (path) {
        this._add(this._create_paths, path);
    },

    _remove_create_tag: function (tag) {
        this._remove_create_path(tag.path);
    },

    _remove_create_path: function (path) {
        _.pull(this._create_paths, path);
    },

    _toggle_create_tag: function (tag) {
        this._toggle_create_path(tag.path);
    },

    _toggle_create_path: function (path) {
        this._toggle(this._create_paths, path);
    },

    /**
     *  This is a stub to allow future work on validation
     * @method validationFailed
     * @param tag
     */
    validationFailed: function (tag) {
        console.log(tag);
        console.error('validation error');
    },

    _bystring: function (path) {
        return _.get(this, path);
    },
    /**
     * Retrieve the tag(s) which are linked to a certain property of the store
     * @param path
     * @returns {array} Tags which have the given path
     */
    getTagByPath: function (path) {
        return this.tag_registry[path];
    },

    /**
     * returns the status of the last request made by this store in order to
     * PhantomJS test for a "200" returned from this function on activity create
     * @memberof ActivityStore
     * @method latest_request_status
     */
    latest_request_status: function () {
        var store = this;
        var last_request;
        if (store.requesthistory === undefined) {
            return 'Store has no request history';
        }
        if (store.requesthistory.length === 0) {
            return 'Store has no requests ';
        }

        last_request = store.requesthistory[store.requesthistory.length - 1];
        if (last_request.status === undefined) {
            return 'last_request has no status';
        }

        return last_request.status;
    },

    get_choice: function (category, code, empty) {
        var label;
        var choice = _(this.choices[category]).find(function (c) { return _.isArray(c) ? c[0] === code : c.code === code; });
        if (!choice) { return empty || ''; }
        label = _.isArray(choice) ? choice[1] : choice.name;
        return label !== '' ? label : code;
    },

    save: function (tag, opts) {
        var store = this;
        var xhr;
        var ajax_opts = {
            method: _.get(opts, 'method') || _.invoke(tag, 'fn.ajax.method') || _.invoke(store, 'fn.ajax.method') || 'PUT',
            url: _.get(opts, 'url') || _.invoke(tag, 'fn.ajax.url') || _.invoke(store, 'urls').update,
            headers: { 'X-CSRFTOKEN': window.csrf_token }
        };

        // Stringify our data
        var data = _.get(opts, 'data') || _.invoke(tag, 'fn.ajax.clean_data') || _.invoke(store, 'clean_data', tag) || store[store.el];

        // Normally we would make a JSON request like this
        if (!_.get(data, '_file')) {
            ajax_opts.data = JSON.stringify(data);
            ajax_opts.dataType = 'json';
            ajax_opts.contentType = 'application/json';
        } else {
            // However if we're doing a FileUpload we need a more intelligent approach
            ajax_opts.cache = false;
            ajax_opts.contentType = false;
            ajax_opts.processData = false;
            ajax_opts.data = new FormData();
            ajax_opts.data.append('_file', _.get(data, '_file')); // Yes, this is "append" not 'push"!
            ajax_opts.data.append('_data', JSON.stringify(data));
        }

        window.banner_message.show(_.get(store, 'messages.saving', gettext('Saving')), 'info');
        // TODO: store.clean_data() functions

        // Pull properties where they are child tags of the supplied tag instance, if given. Otherwise the whole store
        // will be transmitted in the request.

        // File uploads are handled differently
        xhr = $.ajax(ajax_opts)
            .done(function () {
                var response_data = xhr.responseJSON;
                // TODO: Some of this allows workflow which should not be encouraged, like changing Store data from a Tag
                if (_.has(tag, 'fn.ajax.done')) {
                    _.invoke(tag, 'fn.ajax.done', response_data);
                } else if (_.has(store, 'requestopts.create_done') && xhr.status === 201) {
                    store.trigger(_.get(store, 'requestopts.create_done'), data, response_data);
                } else if (_.has(store, 'requestopts.update_done') && xhr.status !== 204) {
                    store.trigger(_.get(store, 'requestopts.update_done'), data, response_data);
                } else if (_.has(store, 'requestopts.delete_done') && xhr.status === 204) {
                    store.trigger(_.get(store, 'requestopts.delete_done'), data, response_data);
                } else if (_.isFunction(store.process_response)) {
                    store.load(store.process_response(response_data));
                } else { store.load(response_data); }
                window.banner_message.show(gettext('Saved'), 'success');
            });

        xhr.fail(function () {
            // store.restore();
            console.error(xhr.responseJSON); // eslint-disable-line no-console
            var is_simple_error;
            // Validation Error handling
            if (xhr.status === 400){
                /* A 'simple' error is one where we have one field and one message in the array */
                is_simple_error = _.size(_.keys(xhr.responseJSON)) === 1 && _.isArray(_.values(xhr.responseJSON)[0]) && _.isString(_.values(xhr.responseJSON)[0][0])
                if (is_simple_error){
                    window.banner_message.show(_.get(store, 'messages.xhr.fail', 'Error while saving: '+_.keys(xhr.responseJSON)[0] + ' - ' + _.values(xhr.responseJSON)[0][0]), 'danger');
                }
                else {
                    /* This is ugly but better than no message */
                    window.banner_message.show('Error(s) while saving: ' + JSON.stringify(xhr.responseJSON), 'danger');
                }
            }
            else {
                window.banner_message.show(_.get(store, 'messages.xhr.fail', xhr.status + ' ' + gettext('Error while saving, please try again')), 'danger');
            }
        });
        store.request = xhr;
        return xhr;
    },

    read: function (tag) { this.save(tag, { url: this.urls.read(), method: 'GET' }); },
    create: function (tag, item) { return this.save(tag, { url: this.urls.create(), method: 'POST', data: item }); },
    delete: function (tag, item) { return this.save(tag, { url: this.urls.delete(item.id), method: 'DELETE', data: { id: item.id } }); }, // TODO: Implement 'remove-by-id' function
    update: function (tag, item) { return this.save(tag, { url: this.urls.update(item.id), method: 'PUT', data: item }); },
    createOrUpdate: function (tag, item) { return _.isNumber(item.id) ? this.update(tag, item) : this.create(tag, item); },

    /* Push a clone of the store's "template" onto the stack */
    item_push: function push_template() {
        var store = this;
        var temp = _.clone(store.template);
        var index = store[store.el].push(temp) - 1;
        return { index: index, item: temp };
    },

    /* Pull the item from the stack at "index" */
    item_pull: function pull(index) {
        var store = this;
        _.pullAt(store[store.el], index);
    },

    /* Wrapper function to return item at index */
    item_get: function get(index) {
        var store = this;
        return { index: index, item: store[store.el][index] };
    },

    /* New-style getters/setters intended to work with a single object */
    removeById: function removeById(id) { var store = this; _.remove(store[store.el], { id: id }); },
    getData: function getData() { return _(this).get(this.el); },
    getDataById: function getDataById(id) { return _.find(this.getData(), { id: _.toNumber(id) }); },
    cloneById: function cloneById(id) { return _.cloneDeep(this.getDataById(id)); },
    setDataById: function setDataById(response_data) { _.assign(this.getDataById(response_data.id), response_data); },
    pushData: function pushData(response_data) { this.getData().push(response_data); return this.getDataById(response_data.id); },
    setOrPushData: function setOrPushData(response_data) { return !_.isUndefined(this.getDataById(response_data.id)) ? this.setDataById(response_data) : this.pushData(response_data); }

};

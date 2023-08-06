/**
 * SerializerMixin provides functions for easier form serialization and
 * object / JSON handling.
 *
 * @mixin
 * @constructor
 * @listens ActivityStore.trigger:element_restored
 * @listens ActivityStore.trigger:element_changed
 */
/* exported SerializerMixin */

var SerializerMixin;

function setTagStore(tag) {
    /*
    Set the tag's "store" property by iterating up through parent tags
    until encountering a 'getStore' function, or a 'store' property, or an 'opts.store' property
    */
    var ancestor = tag;
    while (!tag.store && ancestor) {
        tag.store = _.invoke(ancestor, 'getStore') || _.get(ancestor, 'store') || _.get(ancestor, 'opts.store');
        if (!tag.store) { ancestor = ancestor.parent; }
    }
}

SerializerMixin = {
    init: function () {
        var tag = this;
        var registry;
        setTagStore(tag);

        tag.store.requesthistory = tag.store.requesthistory || [];
        tag.root_element = tag.opts.root_element || tag.store.el;
        tag.languages = tag.store.languages || {};
        tag.language = tag.language || 'en';
        tag.validation_failures = [];

        // If this tag's "validate" function fails, or any nested tag's validation fails,
        // validation_failures will contain failing tag(s)
        /* Track pending responses */
        tag.requests_waiting = 0;
        tag.path_set = [];

        tag.on('mount', function () {
            tag.path = tag.absolute_path();
            tag.data = tag.bystring(tag.path, { strict: false, validate: true }) || '';
            tag.store.tag_registry = tag.store.tag_registry || {};
            registry = tag.store.tag_registry;
            registry[tag.path] = registry[tag.path] || [];
            if (_(registry[tag.path]).indexOf(tag) === -1) {
                registry[tag.path].push(tag);
            }
        });

        tag.on('update', function () {
            tag.store.tag_registry = tag.store.tag_registry || {}; // Removing this causes an error in FF
            if ((tag.absolute_path() !== tag.path) && tag.path !== undefined) {
                tag.store.tag_registry[tag.path].splice(tag.store.tag_registry[tag.path].indexOf(tag.path), 1);
            }

            if (tag.absolute_path() !== undefined) {
                tag.path = tag.absolute_path();
                tag.store.tag_registry[tag.path] = tag.store.tag_registry[tag.path] || [];
                if (tag.store.tag_registry[tag.path].indexOf(tag) === -1) {
                    tag.store.tag_registry[tag.path].push(tag);
                }

                tag.data = tag.bystring(tag.path, { strict: false }) || '';
            }
        });

        tag.on('unmount', function () {
            if (_.isUndefined(tag.store.tag_registry[tag.path])){return;}
            var index = tag.store.tag_registry[tag.path].indexOf(tag.path);
            tag.store.tag_registry[tag.path].splice(index, 1);
        });

        // Always update tags when our object is restored
        RiotControl.on(tag.root_element + '_restored', function () { if (tag.isMounted) { tag.update(); } });

        RiotControl.on(tag.root_element + '_changed', function () { tag.update(); });
    },

    /**
     * Returns the dotted-path notation to get to the data element which this tag affects
     * @param path {string} Path - Optionally, give the path of a different element which sould be treated as a sibling
     * @returns {*}
     */
    absolute_path: function (path) {
        var tag = this;
        var parent_path;
        path = path || tag.opts.path;

        if (path === '') {
            return tag.parent.absolute_path();
        } else if (!path) {
            path = '';
        } else if (path.indexOf('/') === 0) {
            /* Specify a path with a leading slash to always use an absolute */
            path = path.replace('/', '');
            return path;
        } else if (path.indexOf('/') !== 0 && tag.parent !== undefined && $.isFunction(tag.parent.absolute_path)) {
            parent_path = tag.parent.absolute_path();
            path = parent_path + path;
            return path;
        }

        if (path !== undefined && !_.includes(tag.path_set, path)) {
            tag.path_set.push(path);
            tag.data = tag.bystring(path, { strict: false }) || '';
        }

        return path;
    },

    serialize_object: function () {
        var tag = this;
        var serialized_object = {};

        var extracted_data = tag.extract_data();
        $.each(extracted_data, function (input, val) {
            serialized_object[val.path] = val.value;
        });

        serialized_object = tag.unflatten(serialized_object)[tag.root_element];
        return serialized_object;
    },

    /**
     * Serialize the data contained in the tags, and PUT or POST the activity.
     */
    save: function (opts) { // eslint-disable-line consistent-return
        var options = _.extend(opts, {});
        var serialized_object = {};
        var _this = this;
        var remove_paths = [];
        // Explicitly set put or post as method within the tag's store
        options.method = _this.store.method;

        function pruneEmpty(obj) {
            return (function prune(current) {
                _.forOwn(current, function (value, key) {
                    if (_.isUndefined(value) || _.isNull(value) || _.isNaN(value) ||
                        (_.isString(value) && _.isEmpty(value)) ||
                            (_.isObject(value) && _.isEmpty(prune(value)))) {
                        delete current[key];
                    }
                });
                // remove any leftover undefined values from the delete
                // operation on an array
                if (_.isArray(current)) _.pull(current, undefined);

                return current;
            }(_.cloneDeep(obj))); // Do not modify the original object, create a clone instead
        }

        window.banner_message.show(gettext('Saving'), 'info');

        $.each(_this.extract_data(), function (input, val) {
            serialized_object[val.path] = val.value;
        });

        _.each(serialized_object, function (value, path) {
            var remove = false;
            _.each(_this.store._delete_paths, function (delete_path) {
                if (!remove && path.indexOf(delete_path) > -1) {
                    remove_paths.push(path);
                }
            });
        });

        serialized_object = _.omit(serialized_object, remove_paths);
        serialized_object = _.omit(serialized_object, _this.store._delete_paths);
        serialized_object = _this.unflatten(serialized_object)[_this.root_element];

        if (this.store.prune) {
            serialized_object = pruneEmpty(serialized_object);
        }

        // Determine the method to use
        if (options.method === undefined && serialized_object.id === undefined) {
            options.method = 'POST';
        }

        if (options.method === undefined && serialized_object.id !== undefined) {
            options.method = 'PUT';
        }

        if (options.method === 'POST') {
            return _this.post(serialized_object, _this.store.requestopts);
        } else if (options.method === 'PUT') {
            return _this.put(serialized_object, _this.store.requestopts)
                .done(function () {
                    window.banner_message.show('Saved', 'success');
                });
        } else if (options.method === 'PATCH') {
            return _this.put(serialized_object, _.extend(_this.store.requestopts, { method: 'PATCH' }))
                .done(function () {
                    window.banner_message.hide('Saved', 'success');
                });
        }
    },

    /**
     * POST `data` to the URL specified by the store, Execute any RiotControl function which is passed as a parameter
     * @param data
     * @param opts
     */
    post: function (data, opts) {
        var tag = this;
        var xhr;
        if (tag.validated === false && opts.verification !== undefined) {
            tag.store.trigger(opts.verification, tag);
            return null;
        }

        xhr = $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            method: 'POST',
            url: tag.store.urls(data).create,
            headers: { 'X-CSRFTOKEN': window.csrf_token }
        });

        tag.store.requesthistory = tag.store.requesthistory || [];
        tag.requests_waiting += 1;
        tag.store.requesthistory.push(xhr);
        xhr.always(function () { tag.requests_waiting -= 1; });

        if (opts.create_done !== undefined) {
            xhr.done(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.create_done, data, returned_data, textStatus, request);
            });
        }

        if (opts.create_fail !== undefined) {
            xhr.fail(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.create_fail, data, returned_data, textStatus, request);
            });
        }

        if (opts.create_always !== undefined) {
            xhr.always(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.create_always, data, returned_data, textStatus, request);
            });
        }

        return xhr;
    },

    /**
     * PUT `data` to the URL specified by the store, Execute any RiotControl function which is passed as a parameter
     * @param data
     * @param opts
     */
    put: function (data, opts) {
        /* Make an update (PUT) request to the URL specified by the store
         * execute any RiotControl function which is passed as a parameter
         */
        var tag = this;
        var xhr;
        if (tag.validated === false && opts.verification !== undefined) {
            tag.store.trigger(opts.verification, tag);
            return null;
        }

        // Make a PUT request to the server
        xhr = $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            method: opts.method || 'PUT',
            url: opts.update || tag.store.urls(data).update,
            headers: { 'X-CSRFTOKEN': window.csrf_token }
        });

        tag.store.requesthistory = tag.store.requesthistory || [];
        tag.requests_waiting += 1;
        tag.store.requesthistory.push(xhr);
        xhr.always(function () { tag.requests_waiting -= 1; });

        if (opts.update_done !== undefined) {
            xhr.done(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.update_done, data, returned_data, textStatus, request);
            });
        }

        if (opts.update_fail !== undefined) {
            xhr.fail(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.update_fail, data, returned_data, textStatus, request);
            });
        }

        if (opts.update_always !== undefined) {
            xhr.always(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.update_always, data, returned_data, textStatus, request);
            });
        }

        return xhr;
    },

    /**
     * DELETE request to the URL specified by the store, Execute any RiotControl function which is passed as a parameter
     * @param id
     * @param opts
     */
    delete: function (id, opts) {
        /* Send a DELETE request to the server */
        /* Available opts:
            url: url to send request to
            delete_done: str RiotControl callback function name to trigger on xhr.done
            delete_fail: str RiotControl callback on fail
            delete_always: str RiotControl callback always
        */
        var tag = this;

        var xhr = $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            method: 'DELETE',
            url: opts.delete || tag.store.urls({ id: id }).delete,
            headers: { 'X-CSRFTOKEN': window.csrf_token }
        });

        tag.store.requesthistory = tag.store.requesthistory || [];
        tag.requests_waiting += 1;
        tag.store.requesthistory.push(xhr);
        xhr.always(function () { tag.requests_waiting -= 1; });

        if (opts.delete_done !== undefined) {
            xhr.done(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.delete_done, id, returned_data, textStatus, request);
            });
        }

        if (opts.delete_fail !== undefined) {
            xhr.fail(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.delete_fail, id, returned_data, textStatus, request);
            });
        }

        if (opts.delete_always !== undefined) {
            xhr.always(function (returned_data, textStatus, request) {
                tag.store.trigger(opts.delete_always, id, returned_data, textStatus, request);
            });
        }

        return xhr;
    },


    /** Returns an object that represents the data contained in `this`.
     * If the tag has children, `extract_data` will be called recursively on the children.
     *
     * Ex: called on the general tab, `extract_data` returns an array of objects,
     * where each object has a `path` and a `value`, like:
     * [
     *   {
     *     "path": "activity.descriptions",
     *     "value": [
     *       {
     *         "type": {
     *           "code": 2
     *         },
     *         "description": "",
     *         "language": "en"
     *       },
     *       ...
     *     ]
     *   },
     *   ...
     * ]
     * @returns {Array}
     * @memberof SerializerMixin
     */
    extract_data: function () {
        var paths = [];
        var tag = this;

        // Return an object for serialization + 'put'ting

        if (tag.tags !== undefined) {
            $.each(tag.tags, function (index, child_tag) {
                // Iterate through nested tags

                if (child_tag !== undefined) {
                    if (child_tag.opts !== undefined) {
                        paths = paths.concat($.isFunction(child_tag.extract_data) ? child_tag.extract_data() : []);
                    } else if (child_tag.length !== undefined && child_tag.length > 0) {
                        // array where multiple instances of a child tag are used
                        $.each(child_tag, function (child_index, item) {
                            paths = paths.concat($.isFunction(item.extract_data) ? item.extract_data() : []);
                        });
                    }
                }
            });
        }

        if (tag.opts.path !== undefined && !tag.opts.nosubmit) {
            paths.push({
                path: tag.absolute_path(tag.opts.path),
                value: tag.bystring(tag.absolute_path(tag.opts.path))
            });
        }

        return paths;
    },

    /**
     * bystring acts as a getter / setter where a value might be difficult to change directly from a form field
     * @param path {string}
     * @param opts {object|undefined}
     * @returns {*|{}}
     */
    bystring: function (_path, opts) {
        var tag = this;
        var store = _.startsWith(_path, 'this.') ? tag.parent : tag.store;
        var path = _.startsWith(_path, 'this.') ? _.replace(_path, 'this.', '') : _path;
        var value = _.get(store, path);
        var updated_value;
        opts = opts || {};
        if (!_.has(opts, 'data')) {
            return value;
        }

        if (_.has(opts, 'data')) {
            if (opts.data === value) {
                return value;
            }
            _.set(store, path, opts.data);
            updated_value = _.get(store, path);
            tag.data = updated_value;
            tag.value_has_changed = true;
            if (value !== updated_value) {
                if (_.isFunction(store._add_update_path)) {
                    store._add_update_path(tag.path);
                }
                store.trigger('path_updated', tag);
                if (_.isFunction(store.update_tag)) {
                    store.update_tag(tag);
                }
            }

            if (store === tag.parent) {
                tag.parent.update();
                tag.validate();
            }

            return updated_value;
        }
        return null;
    },

    /**
     * Return a hierarchy (i.e. a standard Object)
     * @param data
     * @returns {*}
     */
    unflatten: function (data) {
        var regex = /\.?([^.\[\]]+)|\[(\d+)\]/g; // eslint-disable-line
        var resultholder = {};
        var p;
        if (Object(data) !== data || Array.isArray(data)) {
            return data;
        }
        for (p in data) { // eslint-disable-line
            var cur = resultholder; // eslint-disable-line
            var prop = ''; // eslint-disable-line
            var m; // eslint-disable-line
            while (m = regex.exec(p)) {  // eslint-disable-line
                cur = cur[prop] || (cur[prop] = (m[2] ? [] : {}));
                prop = m[2] || m[1];
            }

            cur[prop] = data[p];
        }

        return resultholder[''] || resultholder;
    },

    /**
     * Return an array of "flattened" JSON data
     * @param data
     * @returns {*}
     */
    flatten: function (data) {
        var result = {};

        function recurse(cur, prop) {
            var isEmpty;
            if (Object(cur) !== cur) {
                result[prop] = cur;
            } else if (Array.isArray(cur)) {
                for (var i = 0, l = cur.length; i < l; i++) { recurse(cur[i], prop + '[' + i + ']'); } // eslint-disable-line
                if (l == 0) { result[prop] = []; } // eslint-disable-line
            } else {
                isEmpty = true;
                for (var p in cur) { // eslint-disable-line
                    isEmpty = false;
                    recurse(cur[p], prop ? prop + '.' + p : p);
                }

                if (isEmpty && prop) {
                    result[prop] = {};
                }
            }
        }

        recurse(data, '');
        return result;
    }
};


    /* {% load i18n %} */
    /* {% comment %}
    This file is maintained as a compatibility layer between "Mohinga" editor and "PHD" results
    Hopefully this file will outlive its usefulness when Mohinga gets joyfully acquainted with
    Sergio and Josh's work on the 'Results Dashboard' and new editor interface
    {% endcomment %}
    */
    /* eslint no-underscore-dangle: 0 */
    var tag = this;
    tag.validated = true;
    tag.classes = {
        select: '',
        outer: '',
        input: '',
        date_label: 'control-label',
        date: '',
        tabpanel: '',
        dropdown: ''
    };

    tag.mixin('TabMixin');
    tag.mixin('SerializerMixin');
    tag.mixin('FormFieldMixin');

    tag.on('mount', function () {
        RiotControl.on('discard-modal-discard-triggered', function () {
            tag.current_edit = -1;
        });
    });

    tag.validate = function () {
        tag.validated = true;
        return tag.validated;
    };

    tag.delete_result = function (e) {
        var result = e.item.result;
        var store = tag.store;
        var url = store.urls(result).delete;
        function inner_delete_function() {
            var xhr = store.save(tag, { url: url, method: 'DELETE', data: { id: result.id } });
        }
        RiotControl.trigger('confirm-delete', { confirm: inner_delete_function, content:'This result will be deleted permanently.' });
    };

    tag.cancel = function () {
        var editing_existing = !_.isUndefined(_.get(tag, 'data[' + tag.current_edit + '].id'));
        if (editing_existing) {
            tag.store[tag.store.el][tag.current_edit] = _.cloneDeep(tag.store._initial[tag.current_edit]);
            
            tag.current_edit = -1;
        } else {
            _.remove(tag.data, { id: undefined });
            tag.current_edit = -1;
        }
    };

    tag.trigger_edit = function (e) {
        tag.current_edit = e.item.index;
    };

    tag.add_result = function () {
        var store = tag.store;
        store[store.el].push(_.cloneDeep(store.template));
        tag.update({
            current_edit: tag.data.length - 1
        })
    };

    tag.has_changed = function () {
        var tag = this;
        return !_.isEqual(tag.store._initial, tag.data)
    };

    tag.discard = function(){
        tag.store[tag.store.el] = _.cloneDeep(tag.store._initial);
    }

    tag.save_results = function () {
        window.banner_message.show(gettext('Saving'), 'info');
        var data = tag.data[tag.current_edit];
        /* Format returned by "simple" is a little different to serialized data from the view */
        data.type = data.result_type;
        var xhr = data.id ? tag.put(data, {}) : tag.post(data, {});
        
        if (xhr !== undefined) {
            xhr.done(function (returned_data) {
                /* Format returned by "simple" is a little different to serialized data from the view */
                returned_data.type = _.find(tag.store.choices.result_type, {code: returned_data.type})
                tag.data[tag.current_edit] = tag.store.reformat(returned_data)
                window.banner_message.show(gettext('Saved'), 'success');
            });
            xhr.fail(function () {
                tag.update({current_edit: -1});
                window.banner_message.show(gettext('Error saving the Results, please try again'), 'danger');
            });
            xhr.always(function(){
                tag.store._initial = _.cloneDeep(tag.data);
                tag.store[tag.store.el] = _.cloneDeep(tag.store._initial);
                tag.update({current_edit: -1});
            })
        }

        return xhr;
    };
    tag.save = tag.save_results;

    tag.current_edit = -1;
    
    tag.store.on('results_deleted', function(data){
        /* A little bit hacky to make this "old" store work with "new" functions */
        var store = this;
        _.remove(store[store.el], {id:data.id})
        tag.store._initial = _.clone(store[store.el]);
        tag.update()
    })

    tag.list_child_tags = function () {
        var tag = this;
        var child_returns;
        var returns = _(tag.tags).values().flatten().value();
        _.remove(returns, _.isUndefined);
        _.each(returns, function (child) {
            if (_.isFunction(child.list_child_tags)) {
                child_returns = child.list_child_tags();
                returns = _.concat(returns, child_returns);
            }
            return returns;
        });
        return _.flatten(_.concat(returns));
    }
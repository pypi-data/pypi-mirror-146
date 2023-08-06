/* {% load i18n %} */
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

   function on_admin_status_change(){
        tag.update();
    }

    tag.on('mount', function(){stores.resultsStore.on('admin_status_change', on_admin_status_change)});
    tag.on('unmount', function(){stores.resultsStore.off('admin_status_change', on_admin_status_change)});

    tag.validate = function () {
        tag.validated = true;
        return tag.validated;
    };

    tag.delete_result = function (e) {
        tag.delete_id = e.item.result.id;
        function inner_delete_function() {
            tag.store.make_request({tag: tag, method: 'DELETE', object_type:'result', data:e.item.result}).done(function(){
                _.remove(tag.data, { id: tag.delete_id });
            });

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
        tag.update({current_edit: e.item.index});
    };


    tag.has_changed = function () {
        /* TODO: Build this out to correctly indicate whether there are changes to be saved or not */
        return false;
    };

    tag.save = function () {
        window.banner_message.show(gettext('Saving'), 'info');

        /* Requests are tricky beasties. Here we break our requests into multiple sets of requests for different
         * content types */

        /* Our first request is for the Result itself. If we have no "id" yet, it's a Create; if we do, it's an Update */

        var data = tag.store.results[tag.current_edit];
        if (data.id){initial = tag.store._initial.get()}
        if (!data.id) {
            tag.store.make_request({
                tag: tag,
                object_type: 'result',
                data: tag.store.results[tag.current_edit]
            }).done(function () {
                window.banner_message.show(gettext('Saved'), 'success');
            }).fail(function () {
                window.banner_message.show(gettext('Error saving the Results, please try again'), 'danger');
            })
        }

    };

    tag.on('update', function(){
       tag.editing = tag.current_edit > 0;
       tag.results = _.filter(tag.store.results, {content_type:'result'})
    });

       tag.on('mount', function(){
            tag.store.on('removed', function(){tag.update()});
            tag.store.on('removed', function(){tag.update()});
            tag.store.on('updated', function(){tag.update()});
        });


    tag.current_edit = -1;

    tag.admin_status_change = function(){tag.store.admin_status_change()}

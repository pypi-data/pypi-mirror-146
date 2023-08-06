var tag = this;

tag.mixin('SerializerMixin');
tag.mixin('ValidationMixin');
tag.mixin('TabMixin');
tag.store = tag.opts.store;
tag.store.group_names = ['sectors'];

tag.save = function () {
    /** Serialize the tags and send the serialized object to the activity update API.
    */
    var xhr;
    var serialized_object = tag.serialize_object();
    var has_changed = tag.has_changed();
    if (!has_changed){
        window.banner_message.show(_.get(tag.store, 'messages.no_changes', 'No changes to save'), 'success');
        return;
    }
    serialized_object.id = tag.store.activity_id;

    window.banner_message.show(gettext('Saving the Sectors'), 'warning');
    tag.update();
    xhr = tag.put(serialized_object, { update_done: 'sectors_update_done' });
    xhr.done(function (response) {
        window.banner_message.show(gettext('Successfully saved the Sectors'), 'success');
        // deleting a sector could invalidate percentages, so validate after saving
        tag.store._initial.sectors = _.cloneDeep(response.sectors);
        tag.store.sectors = _.cloneDeep(response.sectors);
        tag.validate();
        tag.update();
    });
    xhr.fail(function () {
        tag.update();
        window.banner_message.show(gettext('Error saving the Sectors, please try again'), 'warning');
    });
    return xhr;
};

tag.serialize_object = function () {
    returns = _(tag.store.sectors).filter(function(s){return s.sector.code}).value();
    return {'sectors': returns};
};

tag.add_row = function (event) {
    tag.store.add_row(event.target.dataset.group);
    tag.store.trigger('path_updated', { store: tag.store, path: tag.path });
    tag.update();
};

tag.store.on('path_updated', function(){ 
    tag.update();
    tag.has_changed();
});

tag.has_changed = function () {
    var s = _(tag.store.sectors).map(function(s){return _.toNumber(s.sector.code)}).compact().value()
    var i = tag.store._initial.sectors.map(function(s){return s.sector.code})
    tag.value_has_changed = ! _(s).sortBy().isEqual(_.sortBy(i))
    return tag.value_has_changed
};

tag.discard = function(){
    this.store.sectors = _.cloneDeep(this.store._initial.sectors);
}

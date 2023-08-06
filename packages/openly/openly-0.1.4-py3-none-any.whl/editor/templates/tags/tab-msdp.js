/* {% load i18n %} */
/* {% load ifsetting %}
/* globals gettext Promise */
/* {% url 'editor-api-activitytag-detail' pk=activity.pk as source_url %}" */
/* {% url 'editor-api-activitytag-list' as base_url %}; */
var tag = this;
var base_url = '{{base_url}}';
var url = base_url + stores.activityStore.activity.id + '/';

// {% ifsetting EDITOR_SHOW_HELPTEXT_ABOVE %}
tag.EDITOR_SHOW_HELPTEXT_ABOVE = true;
// {% else %}
tag.EDITOR_SHOW_HELPTEXT_ABOVE = false;
// {% endifsetting %}

tag.mixin('SerializerMixin');
tag.mixin('TabMixin');
tag.mixin('ValidationMixin');
tag.store = tag.opts.store;
tag.msdps = tag.store.msdps; /* Msdps which are already selected */
tag.msdp_ids = [];
tag.keyword = '';
tag.select_hidden = true;
tag.modal_options = { tab_name: 'Msdps' };

function setTagMsdpIds() {
    var new_msdp_ids = _.map(tag.store.msdps, function (l) { return l.tag; });
    if (!_.isEqual(_.orderBy(new_msdp_ids), _.orderBy(tag.msdp_ids))) {
        try {
            tag.update({ msdp_ids: new_msdp_ids });
        } catch (e) {
            setTimeout(function () { setTagMsdpIds(); }, 100);
        }
    }
}

function refreshFromResponse(response) {
    var ordered_msdps = _.orderBy(response.activitytag_set, 'tag');
    tag.store.msdps = _.cloneDeep(ordered_msdps);
    tag.store._initial = tag.store._initial || {};
    tag.store._initial.msdps = _.cloneDeep(ordered_msdps);

    tag.update({
        msdps: tag.store.msdps,
        loading: false,
        value_has_changed: false,
        msdp_ids: _.map(tag.store.msdps, function (l) { return l.tag; })
    });
    /* Trigger another update as names sometimes don't show */
    tag.has_changed();
    setTimeout(function () { tag.update(); }, 100);
}

function getData() {
    /* returns a Promise which gives JSON data on `.done()`, either from the store (if already there) or from a request (if we're waiting) */

    function from_store() {
        /* skip the request if data is already in the store */
        return new Promise(function (resolve) { // eslint-disable-line no-undef
            resolve(tag.store.msdps);
        });
    }

    function from_request() {
        tag.update({ loading: true });
        /* initial load of data from projectbank-specific endpoint */
        return $.getJSON(url).then(function (response) { refreshFromResponse(response); });
    }

    return _.has(tag.store, 'msdps') ? from_store() : from_request();
}


function load_msdps_from_store() {
    getData().then(function () {
        var s = tag.store;
        /* Django recommended (2.1+) way to handle JSON parsing */
        function p(div) {
            return JSON.parse(document.getElementById(div).textContent);
        }
        s.choices = s.choices || {};
        if (!s.choices.msdps) {
            s.choices.msdps = s.choices.msdps || p('msdp_tags');
            s.choices.goals = s.choices.goals || p('msdp_goals');
            _.map(s.choices.msdps, function (m, i) {
                m.goal = s.choices.goals[(m.name.split('.')[0])];
                m.code = i;
            });
            s.choices.msdps = _.orderBy(s.choices.msdps, 'tag');
        }
        setTagMsdpIds();
    });
}

function hide_select() {
    tag.update({ select_hidden: true, open_search: null });
}

function show_select(e) {
    tag.update({ select_hidden: false, open_search: e.item.enum });
}

function defaultObject() {
    return { tag: null };
}


tag.on('mount', function () {
    load_msdps_from_store();
});

tag.store.on('msdps_updated', function () {
    load_msdps_from_store();
    tag.clearSearch();
});

tag.save = function () {
    /** Serialize the tags and send the serialized object to the activity update API.
    */
    var xhr;
    var serializeObject = function () {
        var msdps = _.clone(tag.store.msdps);
        // remove the elements that have a null code
        _.remove(msdps, function (msdp) { return !msdp.tag; });
        return { activitytag_set: msdps, pk: stores.activityStore.activity.id };
    };
    var serialized_object = serializeObject();

    window.banner_message.show(gettext('Saving the Msdps'), 'warning');
    tag.update();
    xhr = tag.put(serialized_object, { update_done: 'msdps_update_done' });
    xhr.done(function (response) {
        refreshFromResponse(response);
        window.banner_message.show(gettext('Successfully saved the MSDP Alignment'), 'success');
    }).fail(function () {
        window.banner_message.show(gettext('Error while saving'), 'danger');
    });
};

tag.has_changed = function () {
    /* Handle case where one 'dummy' is added to the tag */
    function noNullCodes(msdp) {
        return !_.isNull(msdp.tag);
    }
    tag.value_has_changed = !_.isEqual(_.filter(tag.store.msdps, noNullCodes), tag.store._initial.msdps);
    return tag.value_has_changed;
};

tag.child_tags_validated = function () { return true; };

tag.discard = function () {
    tag.store.msdps = _.cloneDeep(tag.store._initial.msdps);
};

function drop_object(e) {
    _.remove(tag.store.msdps, function (m) { return m.tag === e.item.msdp.tag; });
    tag.update({ value_has_changed: true });
    setTagMsdpIds();
}

function add_object() {
    tag.has_changed();
    tag.msdps.push(defaultObject());
}

function ensure_one_msdp() {
    if (tag.msdps && tag.msdps.length === 0) { add_object(); }
}

tag.on('update', ensure_one_msdp);
tag.on('mount', ensure_one_msdp);

tag.validate = function () { return true; };
tag.validated_with_children = function () { return true; };

tag.add_object = add_object;
tag.drop_object = drop_object;
tag.hide_select = hide_select;
tag.show_select = show_select;

tag.store.on('path_updated', setTagMsdpIds); // {# Disabled choices need to be refreshed on tag update #}

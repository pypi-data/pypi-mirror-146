/* {% load i18n %} */
var tag = this;

tag.update_title = function () {
    var title = stores.activityStore.get_title();
    tag.activity_title = (title === '') ? '{% trans "Untitled" %}' : title;
    tag.update();
};

tag.update_activity_status = function () {
    // {% trans 'draft' as draft_status %}
    // {% trans 'submitted for review' as review_status %}
    // {% trans 'published' as published_status %}
    var status = stores.activityStore.activity.openly_status;
    if (status === 'blank' || status === 'draft') {
        tag.activity_status = '{{ draft_status|escapejs }}';
    } else if (status === 'review') {
        tag.activity_status = '{{ review_status|escapejs }}';
    } else if (status === 'published') {
        tag.activity_status = '{{ published_status|escapejs }}';
    } else {
        tag.activity_status = status; // ex: superusers can see archives activities
    }
    tag.update();
};

tag.on('mount', function () {
    /* Set default to the first tag */
    route('*', function (route) {
        tag.update({ route: route });
    });
    if (location.hash === '') { // eslint-disable-line no-restricted-globals
        route('general');
    }
    tag.update_title();
    tag.update_activity_status();
    tag.show_status_badge = (stores.reviewStore !== undefined);
    if (tag.show_status_badge) {
        stores.reviewStore.on('activity_status_changed', tag.update_activity_status);
    }
});

tag.letsgetouttahere = function (e) {
    // Going somewhere? We probably want to check that there are no unsaved changes
    var modal_opts = {};
    var current_tab = window.current_tab;
    e.preventDefault(); // Override the usual behaviour of <a> links
    if (!current_tab) {
        route(e.item.name);
    } else if (current_tab.enableRouting()) {
        /* console.log('ok!! You are clear to navigate') */
        route(e.item.name);
    } else {
        modal_opts = {
            show: true,
            current_tag: window.current_tab,
            route: e.item.name
        };
        $('discard-modal')[0]._tag.update({ opts: modal_opts });
    }
};

stores.activityStore.on('activity_updated', tag.update_title);

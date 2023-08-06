/* {% load i18n %} */

var tag = this;
tag.mixin('TabMixin');
tag.store = tag.opts.store;
tag.show_more_logs = false;

// tag has never changed, to prevent showing the modal
tag.has_changed = function () { return false; };

tag.on('mount', function () {
    tag.refs.comment.value = '';
    tag.store.trigger('refresh_logs');
});

tag.on('update', function (options) {
    tag.activity_logs = tag.show_more_logs ? tag.store.activity_logs : tag.store.activity_logs.slice(0, 20);
    if (_.isObject(options) && options.refresh_logs === false) {
        return;
    }
    tag.store.trigger('refresh_logs');
});

tag.store.on('activity_logs_updated', function () {
    tag.update({ refresh_logs: false });
});

tag.post_comment = function (event) {
    var comment_data = { type: 'comment', comment: _.trim(tag.refs.comment.value) };

    event.preventUpdate = true;
    if (!comment_data.comment) { return; } // don't post empty comments
    tag.disable_post = true;  // avoid posting the same comment many times
    tag.update({ refresh_logs: false });

    tag.store.post_comment(comment_data
    ).done(function () {
        tag.refs.comment.value = '';
    }).always(function () {
        tag.disable_post = false;
        tag.update({ refresh_logs: false });
    });
};

tag.toggle_show_more = function () {
    tag.show_more_logs = !tag.show_more_logs;
    tag.update({ refresh_logs: false });
};

var tag = this;

tag.show = function (message, alert_class) {
    tag.show_message = 1;
    tag.alert_class = alert_class;
    tag.message = message;
    tag.message_class = _.kebabCase(message);
    tag.update();
    if (tag.alert_class === 'success') {
        window.setTimeout(function () {
            tag.show_message = 0;
            tag.update();
        }, 5000);
    }
};

tag.hide = function (alert_class) {
    if (tag.alert_class === alert_class) {
        tag.show_message = 0;
        tag.update();
    }
};

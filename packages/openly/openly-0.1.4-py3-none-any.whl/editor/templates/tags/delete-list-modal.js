var tag = this;
tag.show_message = false;
tag.delete_url = "#";

tag.show = function (delete_url) {
    $('.modal', tag.root).modal('show');
    tag.delete_url = delete_url;
    tag.update();
};

tag.hide = function (alert_class) {
    $('.modal', tag.root).modal('hide');
    tag.delete_url = "#";
    tag.update();
};

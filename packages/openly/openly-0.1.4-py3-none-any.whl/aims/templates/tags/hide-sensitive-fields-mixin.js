function HideSensitiveFieldsMixin(tag) {
    this.init = function() {
        tag.hide_sensitive = ("{{ user.is_anonymous }}" == "True" ? true : false);
    }
}

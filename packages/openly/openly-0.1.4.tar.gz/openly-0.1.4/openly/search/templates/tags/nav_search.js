/* {% load static %} */

var tag = this;
tag.nav_search_term = '';
tag.partners = [];
tag.activities = [];

var delay = (function(){
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();

nav_search_keyup(e) {
    delay(function() {
        if (e.target.value.length >= 3) {
            tag.nav_search_term = e.target.value;
            var xhr = $.get('{% url "api_search" %}', {q: tag.nav_search_term, format: 'json'})
                .done(function(data) {
                    tag.data = data;
                    tag.activities = data.activities.slice(0, 3);
                    tag.partners = data.partners.slice(0, 3);

                })
                .fail(function() {
                    tag.data = [];
                    tag.partners = [];
                    tag.activities = [];
                })
                .always(function() {
                    tag.update();
                    $(".navSearchResults").show();
                });
        }
    }, 500);
}

submit_search(e) {
    $(tag.refs.search_form).submit();
}

$('body').on('click', function(e) {
    if (!$(e.target).closest('.navSearchResults').length){
        $(".navSearchResults").hide();
    }
});

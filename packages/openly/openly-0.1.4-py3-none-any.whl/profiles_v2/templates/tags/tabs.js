var tag = this;

tag.on('mount', function () {
    // We only display tabs for sections of the page that exist so once the DOM has
    // crystalized filter out nonexistent sections
    $(document).ready(function () {
        tag.tabs = opts.tabs.filter(function (t) { return $(t.link).length > 0; });
        tag.update();

       // Create a clone of the menu, right next to original.
        $('.menu-styling').addClass('original').clone().insertAfter('.menu-styling').addClass('cloned').css('position', 'fixed').css('top', '0').css('margin-top', '0').css('z-index', '500').removeClass('original').hide();

        setInterval(stickIt, 50);
    });

    $(window).on('scroll', function () {
        var cur_pos = $(this).scrollTop();
        var sections = $('section');
        var nav = $('.menu-styling');
        var nav_height = nav.outerHeight();

        sections.each(function () {
            var top = $(this).offset().top - nav_height;
            var bottom = top + $(this).outerHeight();

            if (cur_pos >= top && cur_pos <= bottom) {
                nav.find('a').removeClass('active-tab');

                nav.find('a[href="#' + $(this).attr('id') + '"]').addClass('active-tab');
            }
        });
    });
});


function stickIt() {
    var orgElementPos = $('.original').offset();
    var orgElementTop = orgElementPos.top;

    if ($(window).scrollTop() >= (orgElementTop)) {
        // scrolled past the original position; now only show the cloned, sticky element.
        // Cloned element should always have same left position and width as original element.
        var orgElement = $('.original');
        var coordsOrgElement = orgElement.offset();
        var leftOrgElement = coordsOrgElement.left;
        var widthOrgElement = orgElement.css('width');
        $('.cloned').css('z-index', '2000').css('left', leftOrgElement + 'px').css('top', 0).css('width', widthOrgElement).show();
        $('.original').css('visibility', 'hidden');
    } else {
    // not scrolled past the menu; only show the original menu.
        $('.cloned').hide();
        $('.original').css('visibility', 'visible');
    }
}

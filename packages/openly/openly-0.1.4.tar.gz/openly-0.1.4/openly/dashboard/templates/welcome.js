/* globals introJs
* {% load common_text %}
*/

$(document).ready(function () {
    var introTour = introJs();
    introTour.setOptions({
        showStepNumbers: false,
        nextLabel: 'Next',
        prevLabel: 'Back',
        exitOnEsc: false,
        exitOnOverlayClick: false,
        showBullets: false,
        tooltipPosition: 'auto',
        scrollToElement: true,
        steps: [
            {
                intro: '' +
                '<div class="shepherd-logo"></div>' +
                '<div class="shephered-header">' +
                   '{{"shepherd_welcome_header" | common_text}}' +
                '</div>' +
                   '{{"shepherd_welcome_aims" | common_text}}' +
                   ' {{"shepherd_welcome_partners" | common_text}}' +
                '<hr/>' +
                '<div class="disclaimer_header text-center hidden-xs">' +
                    '{{"shepherd_welcome_disclaimer" | common_text}}' +
                '</div> ' +
                '<div class="disclaimer_text hidden-xs">' +
                    '{{"shepherd_welcome_disclaimer_partners" | common_text}}' +
                    ' {{"shepherd_welcome_disclaimer_contactfirst" | common_text}} ' +
                '</div><br/>'
            },
            {
                intro: '' +
                '<div class="shephered-subheader">' +
                    '{{"shepherd_search_header" | common_text}}' +
                '</div> ' +
                    '{{"shepherd_search_finding" | common_text}}.' +
                '<br/>' +
                '<div class="shephered-subheader">' +
                    '{{"shepherd_search_profilepages" | common_text}}' +
                '</div>' +
                    '{{"shepherd_search_profilepages_page" | common_text}}. ' +
                    '{{"shepherd_search_profilepages_access" | common_text}}.',
                element: '#nav-search'
            },
            {
                intro: '' +
                '<div class="shephered-subheader">' +
                    '{{"shepherd_visualise_header" | common_text}}.' +
                '</div>' +
                    '{{"shepherd_visualise_dashboards" | common_text}} -- {{"shepherd_visualise_by" | common_text}}.' +
                    ' {{"shepherd_visualise_link" | common_text}}.',
                element: '#dashboard-dropdown'
            },
            {
                intro: '' +
                '<div class="shephered-subheader">' +
                    '{{"shepherd_filtering_header" | common_text}}' +
                '</div>' +
                    '{{"shepherd_filtering_date" | common_text}}. ' +
                    '{{"shepherd_filtering_select" | common_text}}.',
                element: '.input-daterange'
            },
            {
                intro: '<div class="shephered-subheader">' +
                    '{{"shepherd_export_header" | common_text}}' +
                '</div>' +
                    '{{"shepherd_export_download" | common_text}}. ' +
                    '{{"shepherd_export_selecting" | common_text}}',
                element: '.export-csv'
            },
            {
                intro: '<div class="shephered-subheader">' +
                    '{{"shepherd_activity_header" | common_text}}' +
                '</div>' +
                    '{{"shepherd_activity_calculation" | common_text}} ' +
                    '{{"shepherd_activity_page" | common_text}}',
                element: '.activity_table'
            },
            {
                intro: '<div class="shepherd-logo"></div>' +
                '<div class="shephered-header">' +
                    '{{"shepherd_complete" | common_text}}' +
                '</div> ' +
                    '{{"shepherd_complete_further" | common_text}} ' +
                    '{{"shepherd_complete_help_icons" | common_text}} ' +
                '<i class="ion-information-circled dash-info"></i>  ' +
                   '{{"shepherd_complete_help_icons_further" | common_text}}' +
                '<br/><br/>' +
                    '{{"shepherd_complete_working_hard" | common_text}}. ' +
                    '{{"shepherd_complete_info" | common_text}}'
            }
        ]
    });

    if ($('.dash-header').length && !window.mobile && !$('body').hasClass('pdf-style')) {
        if (!window.localStorage.intro_tour) {
            window.localStorage.intro_tour = true;
            introTour.start();
        }

        $('.tutorial-trigger a').on('click', function () { introTour.start(); });
    } else {
        $('.tutorial-trigger').hide();
    }
});

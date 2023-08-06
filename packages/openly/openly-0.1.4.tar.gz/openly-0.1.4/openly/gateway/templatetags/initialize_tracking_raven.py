from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Library
from django.utils.safestring import mark_safe
from django.utils.html import format_html


register = Library()


@register.simple_tag(takes_context=True)
def initialize_tracking_with_user_properties(context):
    """
    Return the code to track via Google Analytics
    Also adds "user properties" for audience definitions
    """
    ga = getattr(settings, 'GA_TRACKING_ID', None)
    if hasattr(context, 'request') and hasattr(context.request, 'user'):
        user = context.request.user
    else:
        user = None
    html = '<!-- GA tracking code'
    if ga and not settings.DEBUG:
        html += ' -->'

    html += F'''
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga}');
    '''
    if user:
        html += F'''
        gtag('set', 'user_properties', {{
            user_is_staff:'{user.is_staff}',
            user_is_superuser:'{user.is_superuser}',
            user_id:'{user.id}',
        }});
        '''
    html += '</script>'
    if settings.DEBUG or not ga:
        html += '(Commented out as Debug is True and/or settings.GA_TRACKING_ID is None) -->'

    return mark_safe(html)


@register.simple_tag(takes_context=False)
def initialize_tracking():
    """
    Returns the JS code to initialize visits tracking.

    Depending on what's defined in settings.py it will return JS code to inizialize and do
    initial tracking for Piwik (legacy) and/or Google Analytics. Could be a good place to
    manage addition of other tracking tools if necessary.

    Google Analutycs
    ----------------
    As of end of 2018, https://developers.google.com/analytics/devguides/collection/gtagjs/

    Piwik
    -----
    See http://developer.piwik.org/guides/tracking-javascript-guide
    Once Piwik is initialized you can start tracking variables by pushing to the _paq array.
    """
    html = ''
    if hasattr(settings, 'GA_TRACKING_ID'):
        GA_TRACKING_CODE = '''
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());

            gtag('config', '{GA_TRACKING_ID}');
        </script>'''
        html += format_html(mark_safe(GA_TRACKING_CODE),
                            GA_TRACKING_ID=settings.GA_TRACKING_ID)
    if hasattr(settings, 'PIWIK_DOMAIN_PATH'):
        PIWIK_TRACKING_CODE = '''
        <script type="text/javascript">
          var _paq = _paq || [];
          _paq.push(['trackPageView']);
          _paq.push(['enableLinkTracking']);
          (function() {{
            var u="//{piwik_domain}/";
            _paq.push(['setTrackerUrl', u+'piwik.php']);
            _paq.push(['setSiteId', {piwik_site_id}]);
            var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
            g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
          }})();
        </script>
        <noscript><p><img src="//{piwik_domain}/piwik.php?idsite={piwik_site_id}" style="border:0;" alt="" /></p></noscript>
        '''
        html += format_html(mark_safe(PIWIK_TRACKING_CODE),
                            piwik_domain=settings.PIWIK_DOMAIN_PATH,
                            piwik_site_id=settings.PIWIK_SITE_ID)

    return mark_safe(html)


@register.simple_tag(takes_context=False)
def initialize_sentry():
    """
    Sentry SDK
    """
    if getattr(settings, 'SENTRY_SDK_DSN', False):
        return mark_safe(
            '''
            <script src="{}"></script>
            <script type="text/javascript">
                var SENTRY_SDK_DSN = '{}';
                Sentry.init({{dsn: SENTRY_SDK_DSN}});
            </script>
            '''.format(
                staticfiles_storage.url('js/browser.sentry-cdn.com/5.19.1/bundle.min.js'),
                getattr(settings, 'SENTRY_SDK_DSN')
            )
        )
    else:
        return ""

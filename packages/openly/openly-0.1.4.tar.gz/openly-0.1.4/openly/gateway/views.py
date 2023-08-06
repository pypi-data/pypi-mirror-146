from django.views.generic import RedirectView, TemplateView
from django.urls import reverse


class Index(TemplateView):
    template_name = "gateway/index.html"


class HomeRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if not user.is_anonymous:
            if user.organisation is None:
                return reverse('aid_by_location')
            else:
                return reverse('activity_manager', kwargs={'org_id': user.organisation.code})
        else:
            return reverse('index')

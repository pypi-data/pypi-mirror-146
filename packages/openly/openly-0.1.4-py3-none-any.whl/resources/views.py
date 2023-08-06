import json

from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.views.generic.base import TemplateView

from aims.models import Activity, DocumentCategory, Organisation

from .resource_view import Resources


class ResourcesView(TemplateView):
    template_name = "resources/resources.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context["resource_categories"] = mark_safe(
            json.dumps(list(DocumentCategory.objects.all().values("pk", "name")))
        )
        context["resource_projects"] = mark_safe(json.dumps([]))
        context["resource_add"] = False
        context["user_org_id"] = ""

        if self.request.user.is_authenticated:
            organisations = Organisation.objects.filter(users__user=self.request.user)
            if organisations:
                context["resource_add"] = True
                context["user_org_id"] = organisations.first().pk
                activities = (
                    Activity.objects.filter(reporting_organisation__in=organisations)
                    .distinct("id")
                    .all()
                )
                context["resource_projects"] = mark_safe(
                    json.dumps([{"pk": a.pk, "title": a.title} for a in activities])
                )

        return context


class ResourceJsonView(View):
    def get(self, *args, **kwargs):
        resources = Resources(host=self.request.get_host())
        resources_dict = resources.resources_as_dict()
        return JsonResponse(data=resources_dict, json_dumps_params={"indent": 2})

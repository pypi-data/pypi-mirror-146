from . import viewsets, results_viewsets
from rest_framework import routers


def router():
    r = routers.SimpleRouter()

    for m in viewsets.__all__:
        prefix = m.replace('ViewSet', '').lower()
        prefix = "editor-api-" + prefix
        viewset = getattr(viewsets, m)
        base_name = prefix
        r.register(prefix, viewset, base_name)
    return r


def results_router():
    """
    This is a simple "automatic URL generator" for all of the ViewSets listed
    in results_viewsets
    """
    router_results = routers.SimpleRouter()

    for m in results_viewsets.__all__:
        prefix = m.replace('ViewSet', '').lower()
        viewset = getattr(results_viewsets, m)
        router_results.register(prefix, viewset, "result-api-" + prefix)
    return router_results

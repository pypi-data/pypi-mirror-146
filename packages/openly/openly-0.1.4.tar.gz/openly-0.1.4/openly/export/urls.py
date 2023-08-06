from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import export.views as views


def all_subclasses(cls):
    '''
    Handy function to let us get nested subclasses
    '''
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


app_name = 'exports'
urlpatterns = [
    url(r'^$', views.ExportView.as_view(), name='index'),
    url(r'^supersetsecretsquirrel/$', views.SupersetSecretSquirrel.as_view(), name='supersetsecretsquirrel'),
    url(r'^portal/$', login_required(views.ExportPortal.as_view()), name='portal')
]

for klass in all_subclasses(views.ExportSheet):
    '''
    Automate the appending of 'ExportSheet' derived query builders
    to the Export namespace
    '''
    klass_name = klass.__qualname__.lower()
    urlpatterns.append(url(r'^{}/$'.format(klass_name), klass.as_view(), name='%s' % (klass_name)))

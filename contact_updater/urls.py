from django.conf.urls import patterns, url
from contact_updater.views import prepopulate_agency

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[-\w]+)/?$', prepopulate_agency),
)

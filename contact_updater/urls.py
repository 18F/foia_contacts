from django.conf.urls import patterns, url
from contact_updater.views import prepopulate_agency, index, download_data

urlpatterns = patterns(
    '',
    url(r'^$', index),
    url(r'^(?P<slug>[-\w]+)/?$', prepopulate_agency),
    url(r'^/download/?$', download_data)
)

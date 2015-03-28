from django.conf.urls import patterns, url

from indigo_https.views import *


urlpatterns = patterns('',
    url(r'^.*?', IndigoView.as_view()),
)

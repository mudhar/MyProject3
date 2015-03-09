from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^Helpdesk/', include('Helpdesk.urls')),
)+staticfiles_urlpatterns()
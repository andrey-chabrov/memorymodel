from django.conf.urls import patterns, include, url
from django.contrib import admin

import settings

import memorymodel.urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(memorymodel.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^{0}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,
             'show_indexes': True}),
    )

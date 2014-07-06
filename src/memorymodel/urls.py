from django.conf.urls import patterns, include, url


urlpatterns = patterns('memorymodel.views',
    url(r'^$', 'home', name='home'),
)

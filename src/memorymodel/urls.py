from django.conf.urls import patterns, include, url


urlpatterns = patterns('memorymodel.views',
    url(r'^$', 'home', name='home'),
    url(r'^model/(?P<modelname>[a-z0-9_]+)/$', 'home', name='model'),
    url(r'^ajax/get_formset_data/(?P<modelname>[a-z0-9_]+)/$', 
        'get_formset_data', name='get_formset_data'),
)

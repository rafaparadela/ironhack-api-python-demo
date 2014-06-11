from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^ironhackers/add$', 'api.endpoints.ironhackers.add'),
    url(r'^ironhackers/delete$', 'api.endpoints.ironhackers.delete'),
    url(r'^ironhackers/list$', 'api.endpoints.ironhackers.list'),
    url(r'^ironhackers/orphans$', 'api.endpoints.ironhackers.orphans'),
    url(r'^ironhackers/link_to_team$', 'api.endpoints.ironhackers.link_to_team'),
    
    url(r'^teams/add$', 'api.endpoints.teams.add'),
    url(r'^teams/delete$', 'api.endpoints.teams.delete'),
    url(r'^teams/list$', 'api.endpoints.teams.list'),


    url(r'^admin/', include(admin.site.urls)),
    #NOT FOUND
    url(r'^', 'api.views.default'),
)

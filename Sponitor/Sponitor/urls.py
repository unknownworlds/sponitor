from django.conf.urls.defaults import patterns, url
from django.conf import settings

import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # 'REST' API
    url(r'^cpu$', 'stats.api.cpu'),
    url(r'^kill$', 'stats.api.kill'),
    url(r'^performance$', 'stats.api.performance'),
    url(r'^endgame$', 'stats.api.endgame'),
    url(r'^location$', 'stats.api.location'),
)

if "SPONITOR_STAGE" in os.environ and os.environ["SPONITOR_STAGE"] == "frontend":
    urlpatterns += patterns('',
        # website
        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
        url(r'^$', 'stats.views.webapp'),
        
        # Other
        url(r'^flush$', 'stats.views.flush'),

        # data
        url(r'^type$', 'stats.views.typeList'),
        url(r'^location1$', 'stats.views.startLocation1List'),
        url(r'^location2$', 'stats.views.startLocation2List'),
        url(r'^types$', 'stats.views.typeList'),
        url(r'^weapon$', 'stats.views.weaponList'),
        url(r'^maps$', 'stats.views.mapList'),
        url(r'^versions$', 'stats.views.versionList'),
        
        # Statistics
        url(r'^resolution$', 'stats.views.resolution'),
        url(r'^win/pie$', 'stats.views.winPie'),
        url(r'^win/bar$', 'stats.views.winBar'),
        url(r'^win/distance$', 'stats.views.winDistanceBar'),
        url(r'^kill/pie$', 'stats.views.killPie'),
        url(r'^kill/weapon/pie$', 'stats.views.killWeaponPie'),
        url(r'^performance/graph$', 'stats.views.playerPerformance'),
        url(r'^gpu$', 'stats.views.gpu'),
        url(r'^cpucore$', 'stats.views.cpucore'),
        url(r'^cpuspeed$', 'stats.views.cpuspeed'),
        url(r'^lifetime$', 'stats.views.lifetime'),
        url(r'^startlocationcount$', 'stats.views.startlocationCount'),
    )

if not settings.DEBUG:
    urlpatterns += patterns('', (
       r'^' + settings.STATIC_URL[1:] + '(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}
    ))
    pass
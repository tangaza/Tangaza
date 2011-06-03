#
#    Tangaza
#
#    Copyright (C) 2010 Nokia Corporation.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Authors: Billy Odero, Jonathan Ledlie
#

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Currently logging to /tmp/tangaza.log

urlpatterns = patterns('tangaza.Tangaza.views',
    #(r'', include('tangaza.Tangaza.urls')),
    #(r'^from=\+?(\d{1,20})/body=(.{1,160})/$', 'index'),
    (r'^$', 'welcome'),
    (r'^tangaza/$', 'index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^ping/$', 'ping'),
)


urlpatterns += patterns('tangaza.Tangaza.dashboard',
    (r'^web/dashboard/$', 'get_users'),
    (r'^web/dashboard/(\w{0,20})/$', 'get_users'),
)

urlpatterns += patterns('tangaza.Tangaza.api',
    (r'^api/$', include('tangaza.Tangaza.api_urls')),
)

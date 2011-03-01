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
#    Authors: Billy Odero, Jonathan Ledlie, Ian Lawrence
#

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('tangaza.Tangaza.views',
    # Example:
    # (r'^tangaza/', include('tangaza.foo.urls')),

    # main entry point
    # we parse the message in django, not in kannel
    (r'^from=\+?(\d{1,20})/msg=(.{1,160})/smsc=(.{1,20})/$', 'index'),
    
    # testing/pinging
    (r'^ping/$', 'ping'),
    (r'^echo/from=\+?(\d{1,20})/smsc=(.{1,20})/text=(.{0,140})/$', 'echo'),
    (r'^id/from=\+?(\d{1,20})/smsc=(.{1,20})/id=(.{0,140})/$', 'sms_id'),

    # default, blank sms goes straight here
    (r'^update/from=\+?(\d{1,20})/$', 'update'),
    
    #(r'^join/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'join_group'),
    (r'^join/from=\+?(\d{1,20})/group=([\d|\w]{1,60})/slot=(\d?)/smsc=(.{1,20})/$', 'join_group'),
    (r'^leave/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'leave_group'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/(.*)', admin.site.root),
    #(r'^', 'sms.views.root'),

)

urlpatterns += patterns('tangaza.Tangaza.commands',
    # called directly from kannel
    (r'^quiet_group/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'quiet_group'),
    (r'^unquiet_group/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'unquiet_group'),
    (r'^all_groups/from=\+?(\d{1,20})/$', 'quiet_or_unquiet_all_groups'),
    (r'^tangaza_off/from=\+?(\d{1,20})/$', 'quiet_all'),
    (r'^tangaza_on/from=\+?(\d{1,20})/$', 'unquiet_all'),
    (r'^set_name/from=\+?(\d{1,20})/name=(\w{1,60})/$', 'set_username'),
)


urlpatterns += patterns('tangaza.Tangaza.appadmin',
    # called directly from kannel
    (r'^create_group/from=\+?(\d{1,20})/group=(\w{1,20})/slot=([\+|\w|\s]{0,90})/$', 'request_create_group'),
    (r'^delete_group/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'delete_group'),
    (r'^invite_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=([\+?\d|\s|\w|,]{1,140})/smsc=(.{1,20})/$', 'invite_user_to_group'),    
    (r'^add_admin/from=\+?(\d{1,20})/group=(\w{1,60})/admin=([\+?\d|\s]{1,90})/$', 'add_admin_to_group'),
    (r'^delete_admin/from=\+?(\d{1,20})/group=(\w{1,60})/admin=([\+?\d|\s]{1,90})/$', 'delete_admin_from_group'),

    (r'^delete_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=([\+?\d|\s]{1,90})/$', 'delete_user_from_group'),
    (r'^ban_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=(\w{1,20})/$', 'ban_user_from_group'),          
    (r'^unban_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=(\w{1,20})/$', 'unban_user_from_group'),


)

# XXX restrict access to this to local IPs
#urlpatterns += patterns('tangaza.Tangaza.maintenance',
#    # cronjobs call these to keep things in order
#    (r'^maint/periodic/$', 'periodic_maintenance'),
#)

#urlpatterns += patterns('tangaza.Tangaza.dashboard',
#    (r'^web/dashboard/$', 'get_users'),
#    (r'^web/dashboard/(\w{0,20})/$', 'get_users'),
#)
#urlpatterns += patterns('tangaza.Tangaza.web.views',
#    (r'^web/room/$', 'index'),
#)

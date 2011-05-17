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
#    Authors: Billy Odero
#

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name':'admin/login.html'}),
    (r'^logout/$', 'tangaza.Tangaza.api.logout'),
)
urlpatterns += patterns('tangaza.Tangaza.api',

    # main entry point for POST requests
    (r'^api/$', 'get_update'),
    
    # main entry point for GET requests
    (r'^members/group=(\d{1,10})/$', 'get_members'),
    (r'^admins/group=(\d{1,10})/$', 'get_admins'),
    (r'^groups/$', 'get_groups'),
    (r'^update/$', 'get_update'),
    (r'^messages/$', 'get_messages'),

    # POST requests from here on
    (r'^join/from=\+?(\d{1,20})/group=([\d|\w]{1,60})/slot=(\d?)/smsc=(.{1,20})/$', 'request_join'),
    (r'^leave/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'request_leave'),

    (r'^quiet/$', 'request_quiet'),
    (r'^unquiet/$', 'request_unquiet'),
#    (r'^all_groups/from=\+?(\d{1,20})/$', 'quiet_or_unquiet_all_groups'),
#    (r'^tangaza_off/from=\+?(\d{1,20})/$', 'quiet_all'),
#    (r'^tangaza_on/from=\+?(\d{1,20})/$', 'unquiet_all'),
    (r'^set_name/$', 'set_username'),

    (r'^create/from=\+?(\d{1,20})/group=(\w{1,20})/slot=([\+|\w|\s]{0,90})/$', 'request_create_group'),
    (r'^delete_group/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'request_delete_group'),
    (r'^invite/from=\+?(\d{1,20})/group=(\w{1,60})/user=([\+?\d|\s|\w|,]{1,140})/smsc=(.{1,20})/$', 'request_invite_user'), 

    (r'^add_admin/from=\+?(\d{1,20})/group=(\w{1,60})/admin=([\+?\d|\s]{1,90})/$', 'request_add_admin'),
    (r'^delete_admin/from=\+?(\d{1,20})/group=(\w{1,60})/admin=([\+?\d|\s]{1,90})/$', 'request_delete_admin'),

    (r'^delete_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=([\+?\d|\s]{1,90})/$', 'request_delete_user'),
    (r'^ban_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=(\w{1,20})/$', 'request_ban_user'),
    (r'^unban_user/from=\+?(\d{1,20})/group=(\w{1,60})/user=(\w{1,20})/$', 'request_unban_user'),


)

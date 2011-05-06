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


urlpatterns = patterns('tangaza.Tangaza.api',

    # main entry point for POST requests
    (r'^api/$', ''),
    
    # main entry point for GET requests
    (r'^api/members/group=(\d{1,10}/$)', 'get_members'),
    (r'^api/admins/group=(\d{1,10}/$)', 'get_admins'),
    (r'^api/groups/member=(\d{1,10})/$', 'get_groups'),
    (r'^api/update/member=(\d{1,10})/$', 'get_update'),
    (r'^api/messages/group=(\d{1,10})/$', 'get_messages'),
    
    # testing/pinging
    (r'^api/ping/$', 'ping'),
    (r'^join/from=\+?(\d{1,20})/group=([\d|\w]{1,60})/slot=(\d?)/smsc=(.{1,20})/$', 'join_group'),
    (r'^leave/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'leave_group'),
)

urlpatterns += patterns('tangaza.Tangaza.commands',
    # called directly from kannel
    (r'^api/quiet_group/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'quiet_group'),
    (r'^api/unquiet_group/from=\+?(\d{1,20})/group=(\w{1,60})/$', 'unquiet_group'),
    (r'^api/all_groups/from=\+?(\d{1,20})/$', 'quiet_or_unquiet_all_groups'),
    (r'^api/tangaza_off/from=\+?(\d{1,20})/$', 'quiet_all'),
    (r'^api/tangaza_on/from=\+?(\d{1,20})/$', 'unquiet_all'),
    (r'^api/set_name/from=\+?(\d{1,20})/name=(\w{1,60})/$', 'set_username'),
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

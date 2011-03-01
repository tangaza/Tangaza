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

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response

from models import *
from datetime import datetime as dt
from datetime import timedelta

def get_users (request, sort_col="datetime"):
    #users
    user_count = UserPhones.objects.count()
    most_active_user = PubMessages.objects.extra(
        select={'count':'count(phone_number)', 'phone':'phone_number'},
        tables=['user_phones'], where=['user_id=src_user_id'], order_by = ['-count'])[:1]
    most_active_user = most_active_user.values('count', 'phone')
    most_active_user.query.group_by = ['phone']
    
    #tangazos
    tangazo_count = PubMessages.objects.count()
    
    #last 5 days
    pub = PubMessages.objects.filter()#timestamp__gt=dt.date(dt.today() - timedelta(days=5)))
    pub = pub.extra(select={'count':'count(date(timestamp))', 'pub_date':'date(timestamp)'}, order_by = ['-pub_date'])[:5]
    pub = pub.values('count', 'pub_date')
    pub.query.group_by = ['date(timestamp)']

    #groups
    group_count = Groups.objects.extra(where=['group_name not regexp("^[0-9]+$")', 'is_active is not null']).count()
    grp = PubMessages.objects.extra(
        select={'count':'count(group_name)', 'group_name':'group_name'},
        tables=['groups'], where=['group_id=channel'], order_by = ['-count'])[:1]
    grp = grp.values('count', 'group_name')
    grp.query.group_by = ['group_name']

    largest_group = UserGroups.objects.extra(
        select={'count':'count(user_groups.group_id)', 'group_name':'group_name'},
        tables=['groups'], where=['user_groups.group_id=groups.group_id'], order_by = ['-count'])[:1]
    largest_group = largest_group.values('count', 'group_name')
    largest_group.query.group_by = ['group_name']
    
    #list of tangazos
    tangazos = get_tangazos(sort_col)
    
    return render_to_response ('dashboard.html',
                               {'user_count': user_count, 'group_count':group_count,
                                'tangazo_count':tangazo_count, 'calls': pub, 'most_active_group':grp[0],
                                'most_active_user':most_active_user[0], 'largest_group':largest_group[0],
                                'tangazos':tangazos})

def get_groups (request):
    groups = Groups.objects.all()

def get_calls (request):
    calls = PubMessages.objects.all()
    
def get_tangazos (sort_col):
    if sort_col == 'date':
        sort_col = 'datetime'
    elif sort_col == 'sender':
        sort_col = 'phone_number'
    elif sort_col == 'group':
        sort_col = 'group_name'
    else:
        sort_col = 'datetime'
    
    tangazos = PubMessages.objects.extra(
        select={'filename':'filename', 'phone_number':'phone_number',
                'group_name':'group_name', 'datetime':'timestamp', 'name_file':'name_file'},
        tables=['user_phones', 'groups', 'users'],
        where =['user_phones.user_id=src_user_id', 'users.user_id=src_user_id', 'channel=group_id'], order_by = [sort_col])

    return tangazos
        

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
#

from tangaza.sms.models import *
from tangaza.sms.views import *
from tangaza.sms.forms import *
from django.contrib import admin


#inline definitions
class GroupAdminInline(admin.TabularInline):
    model = GroupAdmin
    extra = 1
    max_num = 20
    
class UserGroupInline(admin.TabularInline):
    model = UserGroups
    extra = 1
    max_num = 20

class UserPhonesInline(admin.TabularInline):
    model = UserPhones
    form = UserPhonesForm
    max_num = 3

#Groups customization
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_type', 'is_active')
    list_filter = ('group_type', 'is_active')
    inlines = [GroupAdminInline, UserGroupInline]
    filter_horizontal = ['admins']
    
    fieldsets = (
        (None, 
         {'fields': ['group_name', 'group_type', 'is_active'], 'classes':['wide']}
         ),
        )
    
admin.site.register(Groups, GroupsAdmin)

#Users customization
class UserAdmin(admin.ModelAdmin):
    inlines = [UserPhonesInline]
    form = UserForm
    
admin.site.register(Users, UserAdmin)

####

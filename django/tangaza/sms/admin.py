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
import logging

logger = logging.getLogger('tangaza_logger')

def filtered_user_queryset(request):
    org = request.user.organization_set.get()
    groups = Groups.objects.filter(org = org)
    
    user_groups = UserGroups.objects.filter(group__in = groups)
    users = [ug.user.user_id for ug in user_groups]
    
    qs = Users.objects.filter(user_id__in = users)
    
    return qs
    
#inline definitions
class GroupAdminInline(admin.TabularInline):
    model = GroupAdmin
    extra = 1
    max_num = 20
    formset = GroupAdminInlineFormset
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == 'user' and not request.user.is_superuser:
            kwargs['queryset'] = filtered_user_queryset(request)
            #return db_field.formfield(**kwargs)
        return super(GroupAdminInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class UserGroupInline(admin.TabularInline):
    model = UserGroups
    form = UserGroupsForm
    formset = UserGroupsInlineFormset
    extra = 1
    max_num = 20
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == 'user' and not request.user.is_superuser:
            kwargs['queryset'] = filtered_user_queryset(request)
            #return db_field.formfield(**kwargs)
        return super(UserGroupInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class UserPhonesInline(admin.TabularInline):
    model = UserPhones
    form = UserPhonesForm
    formset = UserPhonesInlineFormset
    max_num = 3
    extra = 1

#Groups customization
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_type', 'is_active')
    list_filter = ('group_type', 'is_active')
    inlines = [GroupAdminInline, UserGroupInline]
    search_fields = ['group_name']
    form = GroupForm
    
    def queryset(self, request):
        qs = super(GroupsAdmin, self).queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(org = request.user.organization_set.get())
        return qs.exclude(group_type = 'mine')
    
    def save_model(self, request, obj, form, change):
        if not change:
            org = request.user.organization_set.get()
            obj.org = org
        obj.save()
    
    fields = ['group_name', 'group_type', 'is_active']
    
admin.site.register(Groups, GroupsAdmin)

#Users customization
class UserAdmin(admin.ModelAdmin):
    inlines = [UserPhonesInline]
    form = UserForm
    #search_fields = ['userphones__phone_number']
    #ordering = ['userphones__phone_number']
    search_fields = ['name_text']
    ordering = ['name_text']
    fields = ['name_text', 'user_pin']
    
    def queryset(self, request):
        #Only returns users that belong to groups from this users organization
        #There has to be a better way of doing this
        qs = super(UserAdmin, self).queryset(request)
        if not request.user.is_superuser:
            org = request.user.organization_set.get()
            groups = Groups.objects.filter(org = org)
            user_groups = UserGroups.objects.filter(group__in = groups)
            users = [ug.user.user_id for ug in user_groups]
            qs = qs.filter(user_id__in = users)
        
        return qs
        
admin.site.register(Users, UserAdmin)

admin.site.register(Organization)

#Add profile as part of auth_user fields
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

#AuthUserAdmin.list_display += ('user_profile',)
#AuthUserAdmin.fieldsets[0][1]['fields'] += ('user_profile',)

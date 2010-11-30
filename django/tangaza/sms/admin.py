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
    formset = GroupAdminInlineFormset
    
class UserGroupInline(admin.TabularInline):
    model = UserGroups
    form = UserGroupsForm
    formset = UserGroupsInlineFormset
    extra = 1
    max_num = 20

class UserPhonesInline(admin.TabularInline):
    model = UserPhones
    form = UserPhonesForm
    max_num = 3
    extra = 0
    
#Groups customization
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_type', 'is_active')
    list_filter = ('group_type', 'is_active')
    inlines = [GroupAdminInline, UserGroupInline]
    search_fields = ['group_name']
    
    def queryset(self, request):
        qs = super(GroupsAdmin, self).queryset(request)
        return qs.exclude(group_type = 'mine')
    
    #Issue: Cant use a m2m field. it wont save. so using inlines instead
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        from django.contrib.admin import widgets
        
        if db_field.name == 'admins':
            ug = UserGroups.objects.filter(group_name = self.group_name)
            
            kwargs['widget'] = widgets.FilteredSelectMultiple(
                db_field.verbose_name, (db_field.name in self.filter_vertical))
            return super(GroupsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    fields = ['group_name', 'group_type', 'is_active']#, 'admins', 'users']
    
admin.site.register(Groups, GroupsAdmin)

#Users customization
class UserAdmin(admin.ModelAdmin):
    inlines = [UserPhonesInline]
    form = UserForm
    search_fields = ['userphones__phone_number']
    
admin.site.register(Users, UserAdmin)

####
class GroupAdminManager(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        import sys
        sys.stdout = sys.stderr
        print "GroupAdmin: save_model",  obj
        pass
    def save_formset(self, request, form, formset, change):
        import sys
        sys.stdout = sys.stderr
        print "GroupAdmin: save_formset",obj
        pass

admin.site.register(GroupAdmin, GroupAdminManager)

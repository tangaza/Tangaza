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

from tangaza.Tangaza.models import *
from tangaza.Tangaza.views import *
from tangaza.Tangaza.forms import *
from tangaza.Tangaza import utility
from django.template.defaultfilters import slugify
from django.contrib import admin
import logging

from tangaza.Tangaza import signals as custom_signal

logger = logging.getLogger(__name__)

def filtered_user_queryset(request):
    #Filter users so that the admin can only see users in their organization
    org = request.user.organization_set.get()
    groups = Vikundi.objects.filter(org = org)
    
    user_groups = UserGroups.objects.filter(group__in = groups)
    users = [ug.user_id for ug in user_groups]
    
    qs = Watumiaji.objects.filter(id__in = users)
    
    return qs

#inline definitions
class GroupAdminInline(admin.TabularInline):
    model = GroupAdmin
    extra = 1
    #max_num = 20
    formset = GroupAdminInlineFormset
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #filter users per organization
        if db_field.name == 'user' and not request.user.is_superuser:
            kwargs['queryset'] = filtered_user_queryset(request)
            return db_field.formfield(**kwargs)
        return super(GroupAdminInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class UserGroupInline(admin.TabularInline):
    model = UserGroups
    form = UserGroupsForm
    formset = UserGroupsInlineFormset
    extra = 1
    #max_num = 20
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #Filter users per organization
        if db_field.name == 'user' and not request.user.is_superuser:
            kwargs['queryset'] = filtered_user_queryset(request)
            return db_field.formfield(**kwargs)
        return super(UserGroupInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class UserPhonesInline(admin.TabularInline):
    model = UserPhones
    form = UserPhonesForm
    formset = UserPhonesInlineFormset
    max_num = 1
    extra = 1

#Groups customization
class VikundiAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'group_type', 'is_active', 'user_count', 'admin_count', 'msg_count']
    list_filter = ['group_type', 'is_active']
    inlines = [GroupAdminInline, UserGroupInline]
    search_fields = ['group_name']
    form = VikundiForm
    fields = ['group_name', 'group_type', 'is_active']
    actions  = ['custom_delete_selected', 'activate_selected', 'deactivate_selected']
    
    #NOTE: Reason for overriding changelist_view, add_view, change_view
    #####################
    #Since the superusers are not associated with any particular organization
    #they should be able to select an organization from a dropdown.
    #Other users are already associated with specific organizations
    def changelist_view(self, request, extra_context=None):
        #self.list_display.append('user_count')
        if request.user.is_superuser and not self.list_display.__contains__('org'):
            #self.list_display.append('is_deleted')
            self.list_display.append('org')
        return super(VikundiAdmin, self).changelist_view(request, extra_context)
    
    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser and not self.fields.__contains__('org'):
            self.fields.append('org')
        return super(VikundiAdmin, self).add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser and not self.fields.__contains__('org'):
            self.fields.append('org')
        return super(VikundiAdmin, self).change_view(request, object_id, extra_context)
    
    def queryset(self, request):
        from django.db.models import Count
        #Limit the groups that are displayed
        #Superuser sees all; other system admins only see groups belonging to their organization
        qs = super(VikundiAdmin, self).queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(org = request.user.organization_set.get())
            #qs = qs.annotate(user_count=Count('usergroups'))
        return qs.exclude(group_type = 'mine')
    
    def save_model(self, request, obj, form, change):
        #Members organization = system admins (system admin == request.user)
        #If its the superuser, this is already retrieved from org dropdown field
        if not change:
            if request.user.is_superuser:
                logger.debug('Org on form: %s' % obj.org)
            else:
                org = request.user.organization_set.get()
                obj.org = org
        obj.save()
        return obj
    
    def activate_selected(self, request, queryset):
        for obj in queryset:
            obj.activate()
            
        if queryset.count() == 1:
            message_bit = "1 vikundi was"
        else:
            message_bit = "%s vikundi were" % queryset.count()
        self.message_user(request, "%s successfully activated." % message_bit)
        
    activate_selected.short_description = "Activate selected vikundi"
    
    def deactivate_selected(self, request, queryset):
        for obj in queryset:
            obj.deactivate()
            
        if queryset.count() == 1:
            message_bit = "1 vikundi was"
        else:
            message_bit = "%s vikundi were" % queryset.count()
        self.message_user(request, "%s successfully deactivated." % message_bit)
        
    deactivate_selected.short_description = "Deactivate selected vikundi"

admin.site.register(Vikundi, VikundiAdmin)

#Users customization
class WatumiajiAdmin(admin.ModelAdmin):
    inlines = [UserPhonesInline]
    form = WatumiajiForm
    search_fields = ['name_text']
    ordering = ['name_text']
    fields = ['name_text', 'user_pin']#, 'organization']
    exclude = ['organization']
    
    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser and not self.fields.__contains__('organization'):
            self.fields.append('organization')
        return super(WatumiajiAdmin, self).add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser and not self.fields.__contains__('organization'):
            self.fields.append('organization')
        return super(WatumiajiAdmin, self).change_view(request, object_id, extra_context)
    
#    def delete_view(self, request, object_id, extra_context=None):
#        return custom_delete_view(self, request, object_id, extra_context)
    
    def custom_delete_selected(self, request, queryset):
        #Meant to cancel the default delete operation in admin page
        #so that the system uses the model's delete method instead of queryset.delete 
        for obj in queryset:
            obj.delete()
            
        if queryset.count() == 1:
            message_bit = "1 member was"
        else:
            message_bit = "%s members were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
        
#    custom_delete_selected.short_description = "Delete selected members"
    
    def save_model(self, request, obj, form, change):
        
        new_watumiaji = form.save(commit=False)
        new_watumiaji.save()
        #Super users dont belong to any group so have to display a dropdown field for organization
        #that they can use to allocate the user
        if request.user.is_superuser:
            org_id = request.POST['organization']
            slot = utility.auto_alloc_slot(obj)
            org = Organization.objects.get(pk = int(org_id))
            grp_name = slugify(org.org_name).replace('-','')
            group = Vikundi.objects.get(group_name = grp_name, org = org)
            #TODO: Remove user from other organizations, if any so that they are not members
            #of more than one organization
            if not new_watumiaji.is_member(group):
                new_watumiaji.join_group(group, slot, None, False)
        
        #if adding a new user then they'll be added to default
        #group for that organization
        if not change:
            if not request.user.is_superuser:
                
                slot = utility.auto_alloc_slot(obj)
                org = Organization.objects.get(org_admin = request.user)
                grp_name = slugify(org.org_name).replace('-','')
                group = Vikundi.objects.get(group_name = grp_name, org = org)
                obj.join_group(group, slot, None, False)
    
    def queryset(self, request):
        #Only returns users that belong to groups from this users organization
        #There has to be a better way of doing this
        qs = super(WatumiajiAdmin, self).queryset(request)
        if not request.user.is_superuser:
            org = request.user.organization_set.get()
            groups = Vikundi.objects.filter(org = org)
            user_groups = UserGroups.objects.filter(group__in = groups)
            users = [ug.user.id for ug in user_groups]
            qs = qs.filter(id__in = users)
        
        return qs

admin.site.register(Watumiaji, WatumiajiAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    form = OrgForm
    actions = ['deactivate_selected', 'activate_selected']
    list_filter = ['is_active']
    list_display = ['org_name', 'is_active']
    
#    def delete_view(self, request, object_id, extra_context=None):
#        return custom_delete_view(self, request, object_id, extra_context)
    
    def deactivate_selected(self, request, queryset):
        for obj in queryset:
            obj.deactivate()
            
        if queryset.count() == 1:
            message_bit = "1 organization was"
        else:
            message_bit = "%s organizations were" % queryset.count()
        self.message_user(request, "%s successfully deactivated." % message_bit)
    
    deactivate_selected.short_description = "Deactivate selected organizations"
    
    def activate_selected(self, request, queryset):
        for obj in queryset:
            obj.activate()
        
        if queryset.count() == 1:
            message_bit = "1 organization was"
        else:
            message_bit = "%s organizations were" % queryset.count()
        self.message_user(request, "%s successfully activated." % message_bit)
    
    activate_selected.short_description = "Activate selected organizations"
    
#    def save_model(self, request, obj, form, change):
#        org = obj.save()
#        group_name = slugify(obj.org_name).replace('-','')
#        
#        custom_signal.create_vikundi_object.send(sender=obj, auth_user=obj.org_admin,
#                                                 group_name=group_name, org=obj)

admin.site.register(Organization, OrganizationAdmin)

#Add profile as part of auth_user fields

admin.site.unregister(User)

from django.contrib.auth.admin import UserAdmin
class UserProfileInline(admin.StackedInline):
    model = Watumiaji
    max_num = 1
    inlines = [UserPhonesInline]
    fields = ['name_text', 'user_pin']
    #exclude = ['place_id', 'name_file', 'dirty', 'modify_stamp']

class OrgInline(admin.StackedInline):
    model = Organization
    form = OrgForm
    formset = OrgInlineFormset
    max_num = 1

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline, OrgInline]

admin.site.register(User, CustomUserAdmin)

class GroupLeaderAdmin(admin.ModelAdmin):
    model = GroupAdmin
    list_display = ['user', 'group']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'group' and not request.user.is_superuser:
            kwargs['queryset'] = Vikundi.objects.filter(org = request.user.organization_set.get())
            return db_field.formfield(**kwargs)
        return super(GroupLeaderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        #Only returns users that belong to groups from this users organization
        #There has to be a better way of doing this
        qs = super(GroupLeaderAdmin, self).queryset(request)
        if not request.user.is_superuser:
            org = request.user.organization_set.get()
            groups = GroupAdmin.objects.filter(group__org = org)
            users = [ug.user.id for ug in groups]
            qs = qs.filter(id__in = users)

        return qs

admin.site.register(GroupAdmin, GroupLeaderAdmin)

class PubMessagesAdmin(admin.ModelAdmin):
    model = PubMessages
    list_display = ['timestamp', 'src_user', 'channel', 'play_message']
    
    def get_actions(self, request):
        actions = super(PubMessagesAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions    
    
    def queryset(self, request):
        # Only returns users that belong to groups from this users organization
        # There has to be a better way of doing this
        
        qs = super(PubMessagesAdmin, self).queryset(request)
        if not request.user.is_superuser:
            org = request.user.organization_set.get()
            #messages = PubMessages.objects.filter(group__org = org)
            #users = [ug.user.id for ug in groups]
            qs = qs.filter(channel__org = org)
        
        return qs
    
    valid_lookups = ('channel')
    
    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup.startswith(self.valid_lookups):
            return True
        return super(PubMessagesAdmin, self).lookup_allowed(lookup, *args, **kwargs)

admin.site.register(PubMessages, PubMessagesAdmin)

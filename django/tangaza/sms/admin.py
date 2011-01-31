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
from tangaza.sms import utility
from django.template.defaultfilters import slugify
from django.contrib import admin
import logging

logger = logging.getLogger('tangaza_logger')

admin.site.disable_action('delete_selected')
###############################################################################
# Copied from options.py to override the default delete_view method
# There has to be a better way to implement my own models delete method
###############################################################################
    
def custom_delete_view(self, request, object_id, extra_context=None):
    from django.contrib.admin.util import unquote, get_deleted_objects
    from django.utils.safestring import mark_safe
    from django.utils.html import escape
    from django.utils.encoding import force_unicode
    from django.utils.text import capfirst
    from django import forms, template
    from django.shortcuts import get_object_or_404, render_to_response
    from django.http import Http404, HttpResponse, HttpResponseRedirect
    
    "The 'delete' admin view for this model."
    opts = self.model._meta
    app_label = opts.app_label
    
    try:
        obj = self.queryset(request).get(pk=unquote(object_id))
    except self.model.DoesNotExist:
        # Don't raise Http404 just yet, because we haven't checked
        # permissions yet. We don't want an unauthenticated user to be able
        # to determine whether a given object exists.
        obj = None
        
    if not self.has_delete_permission(request, obj):
        raise PermissionDenied
    if obj is None:
        raise Http404(u'%(name)s object with primary key %(key)r does not exist.' % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
    
    # Populate deleted_objects, a data structure of all related objects that
    # will also be deleted.
    deleted_objects = [mark_safe(u'%s: <a href="../../%s/">%s</a>' % (escape(force_unicode(capfirst(opts.verbose_name))), object_id, escape(obj))), []]
    deleted_objects = remove_hist_objects(deleted_objects)
    perms_needed = set()
    get_deleted_objects(deleted_objects, perms_needed, request.user, obj, opts, 1, self.admin_site)
    deleted_objects = remove_hist_objects(deleted_objects)
    #import sys
    #sys.stdout = sys.stderr
    #print deleted_objects
    if request.POST: # The user has already confirmed the deletion.
        if perms_needed:
            raise PermissionDenied
        obj_display = force_unicode(obj)
        self.log_deletion(request, obj, obj_display)
            #obj.delete()
            # This is the override
        if type(self) == Groups:
            Groups.delete(request.user.member_profile, obj)
        else:
            obj.delete()
        
        self.message_user(request, u'The %(name)s "%(obj)s" was deleted successfully.' % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
        
        if not self.has_change_permission(request, None):
            return HttpResponseRedirect("../../../../")
        return HttpResponseRedirect("../../")
    
    context = {
        "title": u"Are you sure?",
        "object_name": force_unicode(opts.verbose_name),
        "object": obj,
        "deleted_objects": deleted_objects,
        "perms_lacking": perms_needed,
        "opts": opts,
        "root_path": self.admin_site.root_path,
        "app_label": app_label,
	}
    context.update(extra_context or {})
    context_instance = template.RequestContext(request, current_app=self.admin_site.name)
    return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
            ], context, context_instance=context_instance)
    
###############################################################################

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
            return db_field.formfield(**kwargs)
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
            return db_field.formfield(**kwargs)
        return super(UserGroupInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class UserPhonesInline(admin.TabularInline):
    model = UserPhones
    form = UserPhonesForm
    formset = UserPhonesInlineFormset
    max_num = 3
    extra = 1

#recursively removes history objects from list of deleted_objects the user sees
#on the delete confirmation, since they dont need to know about their existence
def remove_hist_objects(deleted_objects):
    new_list = []
    for item_a in deleted_objects:
        if type(item_a) == type([]):
            if len(item_a) > 0:
                new_list.append(remove_hist_objects(item_a))
            else:
                new_list.append(item_a)
        else: #is unicode
            if not item_a.__contains__('history'):
                new_list.append(item_a)
        
    #remove the empty sets from new_list
    return [x for x in new_list if x != [[]]]

#Groups customization
class GroupsAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'group_type', 'is_active']
    list_filter = ['group_type', 'is_active']
    inlines = [GroupAdminInline, UserGroupInline]
    search_fields = ['group_name']
    form = GroupForm
    fields = ['group_name', 'group_type', 'is_active']
    actions  = ['custom_delete_selected', 'activate_selected', 'deactivate_selected']
    
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser and not self.list_display.__contains__('is_deleted'):
            self.list_display.append('is_deleted')
            self.list_display.append('org')
        return super(GroupsAdmin, self).changelist_view(request, extra_context)
    
    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser and not self.fields.__contains__('org'):
            self.fields.append('org')
        return super(GroupsAdmin, self).add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser and not self.fields.__contains__('org'):
            self.fields.append('org')
        return super(GroupsAdmin, self).change_view(request, object_id, extra_context)
    
    def delete_view(self, request, object_id, extra_context=None):
        return custom_delete_view(self, request, object_id, extra_context)
    
    def queryset(self, request):
        qs = super(GroupsAdmin, self).queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(org__in = request.user.organization_set.all())
            qs.exclude(group_type = 'mine', is_deleted = 'yes')
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:
            if request.user.is_superuser:
                #user picks this from the org field
                logger.error('Org on form: %s' % obj.org)
            else:
                org = request.user.organization_set.get()
                obj.org = org
        obj.save()
    
#    def get_actions(self, request):
#        actions = super(GroupsAdmin, self).get_actions(request)
#        del actions['delete_selected']
#        return actions
    
    def custom_delete_selected(self, request, queryset):
        if request.user.member_profile_id == None:
            self.message_user(request, "You need to create a member profile for yourself before you can proceed")
            return 
        for obj in queryset:
            Groups.delete(request.user.member_profile, obj)
        
        if queryset.count() == 1:
            message_bit = "1 group  was"
        else:
            message_bit = "%s groups were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
        
    custom_delete_selected.short_description = "Delete selected groups"
    
    def activate_selected(self, request, queryset):
        for obj in queryset:
            obj.activate()
        
        if queryset.count() == 1:
            message_bit = "1 group was"
        else:
            message_bit = "%s groups were" % queryset.count()
        self.message_user(request, "%s successfully activated." % message_bit)
        
    activate_selected.short_description = "Activate selected groups"
    
    def deactivate_selected(self, request, queryset):
        for obj in queryset:
            obj.deactivate()
        
        if queryset.count() == 1:
            message_bit = "1 group was"
        else:
            message_bit = "%s groups were" % queryset.count()
        self.message_user(request, "%s successfully deactivated." % message_bit)
        
    deactivate_selected.short_description = "Deactivate selected groups"

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
    actions = ['custom_delete_selected']
    
    def delete_view(self, request, object_id, extra_context=None):
        return custom_delete_view(self, request, object_id, extra_context)
    
    def custom_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        
        if queryset.count() == 1:
            message_bit = "1 member was"
        else:
            message_bit = "%s members were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
        
    custom_delete_selected.short_description = "Delete selected members"
    
    def save_model(self, request, obj, form, change):
        obj.save()
        #if adding new user then they'll be added to default
        #group for that organization
        if not change:
            if request.user.is_superuser:
                pass #catch this on the form
            else:
                slot = utility.auto_alloc_slot(obj)
                org = Organization.objects.get(org_admin = request.user)
                grp_name = slugify(org.org_name).replace('-','')
                group = Groups.objects.get(group_name = grp_name, org = org)
                obj.join_group(group, slot, None, False)
    
    def queryset(self, request):
        #Only return users that belong to groups from this users organization
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

class OrganizationAdmin(admin.ModelAdmin):
    form = OrgForm
    actions = ['deactivate_selected', 'activate_selected']
    list_filter = ['is_active']
    list_display = ['org_name', 'is_active']
    
    def delete_view(self, request, object_id, extra_context=None):
        return custom_delete_view(self, request, object_id, extra_context)
    
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
    
    def save_model(self, request, obj, form, change):
        #Note: This will only ever execute for superuser(s)
        org = obj.save()
        if not change:
            #create group with similar name
            logger.error('Org details %s: ' % obj.org_id)
            grp_name = slugify(obj.org_name).replace('-','')
            user = request.user
            slot = utility.auto_alloc_slot(user.member_profile, user.is_super_user)
            g = Groups.create(user.member_profile, grp_name, slot, org = obj)
            logger.error('Created Group %s for org %s' % (obj, g))
            
            #Add root as admin to every group
            g.add_admin(user.member_profile, user.member_profile)

admin.site.register(Organization, OrganizationAdmin)

#Add profile as part of auth_user fields
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

AuthUserAdmin.list_display += ('member_profile',)
AuthUserAdmin.fieldsets[0][1]['fields'] += ('member_profile',)

#
#    Tangaza
#
#    Copyright (C) 2010 Nokia Corporation.
#
#    This program is free software: you can redistribute it and/or modify
#    It under the terms of the GNU Affero General Public License as
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

from django import forms
from django.db import models
from tangaza.Tangaza.models import *
from tangaza.Tangaza import utility

from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

class UserPhonesInlineFormset(forms.models.BaseInlineFormSet):
    
    def clean(self):
        
        form_count = 0
        primary_nums = 0
        already_primary = False
        
        for form in self.forms:
            try:
                if form.cleaned_data:
                    #must have at least one phone number
                    if not form.cleaned_data['DELETE']:
                        form_count += 1
                    '''
                    #make sure at least/at most one is_primary
                    if form.cleaned_data['is_primary'] == 'yes':
                        primary_nums += 1
                    '''
            except AttributeError:
                #raised coz of the extra field(s) so just ignore
                pass
        
        msg = u''
        if form_count < 1: msg = u'Users must have a phone number'
        if primary_nums > 1: msg = u'A user can only have one primary number'
        #if primary_nums < 1: msg = u'There must be  at least one primary number'
        
        if len(msg) > 0:
            logger.error(msg)
            raise forms.ValidationError(msg)

class UserPhonesForm(forms.ModelForm):
    class Meta:
        model = UserPhones
        exclude = ['country', 'is_primary']
    
    def save(self, force_insert=False, force_update=False, commit=True):
        user_form = super(UserPhonesForm, self).save(commit=False)
        
        country_name = Countries.phone2country (user_form.phone_number)
        country = Countries.objects.get(country_name=country_name)
        user_form.country = country
        user_form.is_primary = 'yes'
        last = Watumiaji.objects.latest('id')
        user_form.user_id = last.id
        user_form.save()
        return user_form

class UserGroupsInlineFormset(forms.models.BaseInlineFormSet):
    
    def clean(self):
        deleting_admin = False
        form_count = 0
        
        #checked if marked for delete
        #if user is admin, if so prevent delete
        for form in self.forms:
            try:
                if form.cleaned_data:
                    user = form.cleaned_data['user']
                    marked_delete = form.cleaned_data['DELETE']
                    if marked_delete and user.is_admin(form.cleaned_data['group']):
                        deleting_admin = True
                
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    form_count += 1
            except AttributeError:
                pass
        
        if deleting_admin:
            msg = u'You cannot delete a user who is also the group administrator. ' \
                'Delete from group admin first'
            logger.error(msg)
            raise forms.ValidationError(msg)
        
        #There must be at least one group member
        if form_count < 1:
            msg = u'You must have at least one member in a group'
            logger.error (msg)
            raise forms.ValidationError(msg)

#User Groups customization
class UserGroupsForm(forms.ModelForm):
    
    class Meta:
        model = UserGroups
        exclude = ['slot']
    
    def clean_slot(self):
        slot = self.cleaned_data['slot']
        if int(slot) != 9:
            raise forms.ValidationError('The slot value should not exceed 9')
        
        return self.cleaned_data['slot']
    
    def save(self, force_insert=False, force_update=False, commit=True):
        ug_form = super(UserGroupsForm,self).save(commit=False)
        
        #for new users auto alloc slot. self.initial == {} for new records
        if self.initial == {}:
            ug_form.slot = utility.auto_alloc_slot(ug_form.user)
        
        #if quiet state changed use methods in model
        ug_db = UserGroups.objects.filter(pk = ug_form.pk)
        
        if len(ug_db) > 0: #if it's an edit then ug_db is not empty
            if ug_db[0].is_quiet != ug_form.is_quiet:
                if ug_form.is_quiet == 'yes':
                    ug_form.group.set_quiet(ug_form.user)
                else:
                    ug_form.group.unquiet(ug_form.user)
        
        #For some reason this value is not set
        ug_form.group_id = ug_form.group.pk
        ug_form.save()
        
        return ug_form

#Group admin customization
class GroupAdminInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        form_count = 0
        
        for form in self.forms:
            
            try:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    form_count += 1
            except AttributeError:
                #raised coz of the extra field(s) so just ignore
                pass
        if form_count < 1:
            msg = u'You must have at least one administrator in a group'
            logger.error (msg)
            raise forms.ValidationError(msg)

###################################################
# Added so that the forms below can access the request object

import threading
_thread_locals = threading.local()

class ThreadLocals(object):
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    """
    def process_request(self, request):
        _thread_locals.request = request

class OrgForm(forms.ModelForm):
    class Meta:
        model = Organization
        
    def clean(self):
        cleaned_data = super(OrgForm, self).clean()
        admin = cleaned_data['org_admin']
        logger.debug("Grae: %s" % admin)
        try:
            org = Organization.objects.get(org_admin=admin)
            raise forms.ValidationError(u'%s is already the administrator for %s. A person can only be the adminstrator of one organization.' % (admin, org))
        except Organization.DoesNotExist:
            pass
        
        return cleaned_data

class OrgInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        form_count = 0
        
        for form in self.forms:
            try:
                if form.cleaned_data:
                    #must have at least one phone number
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        form_count += 1
                        
            except AttributeError:
                #raised coz of the extra field(s) so just ignore
                pass
            
        msg = u''
        if form_count < 1: msg = u'You must specify an organization for the user'
        
        if len(msg) > 0:
            logger.error(msg)
            raise forms.ValidationError(msg)

#User customization
class WatumiajiForm(forms.ModelForm):
    #This organization field is needed to link user to organization
    #NOTE: This will only be visible to superuser who is not linked to any organization
    organization = forms.ModelChoiceField(queryset = Organization.objects.all(),
                                          required=False)#lambda: True if _thread_locals.request.user.is_superuser else False)
    
    class Meta:
        model = Watumiaji
        
    def __init__(self, *args, **kwargs):
        #Set the initial value of org in the dropdown list displayed, to be the users org
        user = kwargs.get('instance', {})
        logger.debug('something user %s' % user)
        
        if user:
            ug = UserGroups.objects.filter(user = user)
            
            if len(ug) > 0:
                group = ug[0].group
                initial = kwargs.get('initial', {})
                initial['organization'] = group.org.pk
                kwargs['initial'] = initial
                
        if not _thread_locals.request.user.is_superuser:
            initial = kwargs.get('initial', {})
            initial['organization'] = _thread_locals.request.user.organization_set.get().pk
            kwargs['initial'] = initial
            logger.debug('spot %s' % kwargs)
        return super(WatumiajiForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(WatumiajiForm, self).clean()
        user = _thread_locals.request.user
        #cleaned_data = self.cleaned_data
        
        if not user.is_superuser:
            cleaned_data['organization'] = user.organization_set.get()
            logger.debug('Smooth %s' % cleaned_data)        
        else:
            if not cleaned_data['organization']:
                raise forms.ValidationError(u'Select the organization')
        
        org = cleaned_data['organization']
        
        #get all groups in org
        groups = Vikundi.objects.filter(org = org)
        #logger.debug("test %s" % self.instance.id)
        users = Watumiaji.objects.filter(id = self.instance.id)
        
        # only check if new user
        if len(users) < 1:
            # get all users in org with same_name
            ug = UserGroups.objects.filter(group__in = groups, user__name_text = cleaned_data['name_text'])
            
            # if there's any user with same name, raise error
            if len(ug) > 0:
                raise forms.ValidationError(u'A user with that name already exists in the organization.')
            
        return cleaned_data
    
    def save(self, force_insert=False, force_update=False, commit=True):
        user_form = super(WatumiajiForm, self).save(commit=False)
        if not _thread_locals.request.user.is_superuser:
            user_form.org = _thread_locals.request.user.organization_set.get()
        
        user_form.save()
        return user_form

class VikundiForm(forms.ModelForm):
    class Meta:
        model = Vikundi
    
    def clean_is_active(self):
        
        if self.cleaned_data['is_active'] == 'yes' and not self.instance.group_name_file:
            msg = u'The group cannot be activated until a ' \
                'voice recording of the group name is provided.'
            logger.error(msg)
            raise forms.ValidationError(msg)
        return self.cleaned_data['is_active']

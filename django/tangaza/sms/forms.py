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
#

from django import forms
from django.db import models
from tangaza.sms.models import *
from tangaza.sms import utility

import logging
logger = logging.getLogger('tangaza_logger')

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
                    
                    #make sure at least/at most one is_primary
                    if form.cleaned_data['is_primary'] == 'yes':
                        primary_nums += 1
            except AttributeError:
                #raised coz of the extra field(s) so just ignore
                pass
        
        msg = u''
        if form_count < 1: msg = u'Users must have a phone number'
        if primary_nums > 1: msg = u'A user can only have one primary number'
        if primary_nums < 1: msg = u'There must be  at least one primary number'
        
        if len(msg) > 0:
            logger.error(msg)
            raise forms.ValidationError(msg)

class UserPhonesForm(forms.ModelForm):
    class Meta:
        model = UserPhones
        exclude = ['country']

    def save(self, force_insert=False, force_update=False, commit=True):
        user_form = super(UserPhonesForm, self).save(commit=False)
        logger.error('user_form: %s' % user_form)
        country_name = Countries.phone2country (user_form.phone_number)
        country = Countries.objects.get(country_name=country_name)
        user_form.country = country
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
            msg = u'You cannot delete a user who is also the group administrator. Delete from group admin first'
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
        ug_db = UserGroups.objects.filter(user_group_id = ug_form.user_group_id)        
        
        if len(ug_db) > 0: #if it's an edit then ug_db is no empty
            if ug_db[0].is_quiet != ug_form.is_quiet:
                if ug_form.is_quiet == 'yes':
                    ug_form.group.set_quiet(ug_form.user)
                else:
                    ug_form.group.unquiet(ug_form.user)
        
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
        
#User customization
class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        #fields = ['name_text', 'user_pin']
    
class GroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        
#    def clean_is_active(self):
#        is_active = self.cleaned_data['is_active']
#        logger.debug("Active status: %s" % is_active)
#        #is_active = u'no'
#        return is_active

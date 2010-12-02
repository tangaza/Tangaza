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
        
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    form_count += 1
            except AttributeError:
                #raised coz of the extra field(s) so just ignore
                pass
        if form_count < 1:
            msg = u'Users must have a phone number'
            logger.error (msg)
            raise forms.ValidationError(msg)

from  django.db.models.signals import *
#connect to post-save signal to log save
def callback(sender, **kwargs):
    logging.info("signal: %s" % dir(kwargs))

post_save.connect(callback)

class UserPhonesForm(forms.ModelForm):
    class Meta:
        model = UserPhones
        exclude = ['country']

class UserGroupsInlineFormset(forms.models.BaseInlineFormSet):
    
    def clean(self):
        errors_exist = False

        #checked if marked for delete
        #if user is admin, if so prevent delete
        for form in self.forms:
            try:
                if form.cleaned_data:
                    user = form.cleaned_data['user']
                    marked_delete = form.cleaned_data['DELETE']
                    if marked_delete and user.is_admin(form.cleaned_data['group']):
                        errors_exist = True
                        
            except AttributeError:
                pass
            
        if errors_exist:
            msg = u'You cannot delete a user that is the the group administrator. Delete from group admin first'
            logger.error(msg)
            raise forms.ValidationError(msg)
    
#User Groups customization
class UserGroupsForm(forms.ModelForm):
    class Meta:
        model = UserGroups
        exclude = ['slot', 'is_quiet']
    
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
    


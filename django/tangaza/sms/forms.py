from django import forms
from django.db import models
from tangaza.sms.models import *

class UserPhonesForm(forms.ModelForm):
    class Meta:
        model = UserPhones
        exclude = ['country']

#User Groups customization
class UserGroupsForm(forms.ModelForm):
    class Meta:
        model = UserGroups

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name_text', 'user_pin']
        

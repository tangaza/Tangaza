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
#    Authors: Billy Odero
#

from tangaza.Tangaza.models import *
from tangaza.Tangaza import utility
from django.dispatch import Signal
from django.db.models.signals import *

import logging

logger = logging.getLogger(__name__)

def get_or_create_user_profile(user):
    profile = None
    
    try:
        profile = user.get_profile()
    except Watumiaji.DoesNotExist:
        profile = Watumiaji.objects.create(name_text=user.username, user=user) 
    return profile

create_vikundi_object = Signal(providing_args=["auth_user", "group_name", "org"])

def create_vikundi_object_handler(sender,  **kwargs):
    logger.debug ('Creating vikundi %s' % kwargs)
    auth_user = kwargs['auth_user']
    group_name =  kwargs['group_name']
    org = kwargs['org']
    
    slot = utility.auto_alloc_slot(get_or_create_user_profile(auth_user), auth_user.is_superuser)
    
    user = auth_user.get_profile()
    Vikundi.create(user, group_name, slot, org = org)

create_vikundi_object.connect(create_vikundi_object_handler)

def user_left_group(sender, **kwargs):
    logger.debug("Deleting user group %s" % kwargs)
    
#    action = Actions.objects.get(action_desc = 'left group')
#    user_group = kwargs['instance']
#    hist = UserGroupHistory(user = user_group.user, group = user_group.group, action = action)
#    hist.save()

post_delete.connect(user_left_group, sender=UserGroups)

def user_joined_group(sender, **kwargs):
    if not kwargs['created']:
        return
    
    action = Actions.objects.get(action_desc = 'joined group')
    user_group = kwargs['instance']
    hist = UserGroupHistory(user = user_group.user, group = user_group.group, action = action)
    hist.save()

post_save.connect(user_joined_group, sender=UserGroups)

def group_created(sender, **kwargs):
    if not kwargs['created']:
        return
    instance = kwargs['instance']
    
    #if its a new group there'll be only one of it in group_admin table
    g = GroupAdmin.objects.filter(group = instance)
    if len(g) > 1:
        return
    
    action = Actions.objects.get (action_desc = 'created group')
    admin_group_hist = AdminGroupHistory (group = instance.group, action = action,
                                          user_src = instance.user, user_dst = instance.user)
    admin_group_hist.save()

#using GroupAdmin to send signal so as to be able to access user details
post_save.connect(group_created, sender=GroupAdmin)

from django.template.defaultfilters import slugify
def organization_created(sender, **kwargs):
    if not kwargs['created']:
        return
    instance = kwargs['instance']
    
    group_name = slugify(instance.org_name).replace('-','')
    
    create_vikundi_object.send(sender=instance, auth_user=instance.org_admin,
                                             group_name=group_name, org=instance)

post_save.connect(organization_created, sender=Organization)

def user_invited(sender, **kwargs):
    if not kwargs['created']:
        return
    inv = kwargs['instance']
    
    action = Actions.objects.get(action_desc = 'invited user')
    hist = UserGroupHistory(user = inv.invitation_from, group = inv.group, action = action)
    hist.save()

post_save.connect(user_invited, sender=Invitations)

def admin_added(sender, **kwargs):
    if not kwargs['created']:
        return
    group_admin = kwargs['instance']
    pass

post_save.connect(admin_added, sender=AdminGroupHistory)

def user_created(sender, **kwargs):
    #NOTE: 
    #Disabled creation if 'mine' group for now so signal doesnt work at the moment
    #To enable the signal connector just uncomment the signal line below
    if not kwargs['created']:
        return
    
    instance = kwargs['instance']
    user = instance.user
    
    #if its a new user there'll be only one of it in user_phones table
    #if just adding an additional number there'll be more than 1
    u = UserPhones.objects.filter(user=user)
    if len(u) > 1:
        return
    
    group = Groups (group_name = instance.phone_number, group_type = 'mine')
    group.save()
    
    user_group = UserGroups (user = user, group = group, slot = 1, is_quiet = 'no')
    user_group.save()
    
    grp_admin = GroupAdmin(user = user, group = group)
    grp_admin.save()
    
    action = Actions.objects.get (action_desc = 'created user')
    admin_group_hist = AdminGroupHistory (group = group, action = action,
                                          user_src = user, user_dst = user)

#post_save.connect(user_created, sender=UserPhones)                                                      

def group_delete_starting(sender, **kwargs):
    logger.debug("Group delete starting")

pre_delete.connect(group_delete_starting, Vikundi)

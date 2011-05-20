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

from __future__ import with_statement
import threading

import re
import logging
import string
import urllib2, urllib

from django.http import HttpResponse
from models import Watumiaji, Vikundi
from utility import *


lock = threading.RLock()

logger = logging.getLogger(__name__)

##Admin actions
#@resolve_user
def request_create_group (request, user, language, group_name, slot):
    from django.template.defaultfilters import slugify
    
    logger.debug ("user %s group_name %s slot %s" % (user, group_name, slot))

    slot = urllib.unquote_plus(slot)

    group_type = 'private'
    
    #only allow group leaders to create groups
    #group leader is the group admin of the main/default organization's group
    default_org = UserGroups.objects.filter(user = user).order_by('pk')[0].group.org
    groups = Vikundi.objects.filter(group_name = slugify(default_org))
    if len(groups) > 0:
        if not user.is_admin(groups[0]):
            return [False, language.action_not_allowed()]
    
    if not user.has_empty_slot ():
        return [False, language.user_has_no_empty_slots ()]
                
    type_and_slot_regex = re.compile("^\w+\s+\d$")
    slot_only_regex = re.compile("^\d$")
    
    if type_and_slot_regex.match(slot):
        (group_type, slot) = slot.split()
        if group_type != 'private':
            group_type = 'public'
    elif len(slot) > 1 and not slot_only_regex.match(slot): #only provided type without slot
        group_type = slot
        if group_type != 'private': group_type = 'public' #check to ensure its actually a group type
        slot = ''
    else:
        #group_type = 'po'
        slot = ''
    
    msg_list = []
    
    if slot is None or len(slot) < 1:
        logger.debug ("slot is none")
        slot = auto_alloc_slot(user)
        logger.info ("slot allocated %s" % slot)
    else:
        logger.debug ("slot is %s" % slot)
    
    #regex = re.compile ('^[A-Za-z]')
    #this regex match doesnt work with unicode character set
    #if not regex.match (group_name) or len(group_name) < 4 or len(group_name) > 60:
    if not group_name[0].isalpha() or len(group_name) < 4 or len(group_name) > 60:
        msg_list.append (language.group_name_not_valid (group_name))
    
    if slot >= 0 and not user.slot_is_empty (slot):
        msg_list.append (language.slot_not_free (slot))
    
    
    # XXX calling this causes an error (and we've fixed the types as unchangeable for now)
    #if not Groups.is_valid_type (group_type):
        #ok = False
        #msg_list.append (language.invalid_group_type (group_type))
    
    # that should take care of the race condition
    with lock:
        
        if not Vikundi.is_name_available (group_name):
            msg_list.append (language.group_name_not_available (group_name))
            # TODO add suggestions
        
        if len(msg_list) > 0:
            msg_text = " ".join(msg_list)
            logger.debug("TWIG: %s" % msg_text)
            return [False, msg_text]
        
        #Any time you create a user the first group they join is the 
        #organization's group
        default_org = UserGroups.objects.filter(user = user).order_by('pk')[0].group.org
        logger.debug('default: %s %s %s %s %s' % (user, group_name, slot, group_type, default_org))
        # create group and assign it to the given slot, if one has been provided
        group = Vikundi.create (user, group_name, slot, group_type, org = default_org)
    
    return [True, language.group_created (group_name, slot, group_type)]

#@resolve_user
def delete_group (request, admin, language, group_name_or_slot):
    logger.debug("group: %s" % (group_name_or_slot))
    
    group = Vikundi.resolve (admin, group_name_or_slot)    

    if group is None:
        return [False, language.unknown_group (group_name_or_slot)]

    if not admin.is_admin (group):
        return [False, language.admin_privileges_required (group)]

    #Vikundi.delete (admin, group)
    group.delete()

    return [True, language.group_deleted (group)]

#@resolve_user
def add_admin_to_group (request, curr_admin, language, group_name_or_slot, new_admin_phone):
    
    admin_list = new_admin_phone.replace("+"," ").split()
    logger.debug("group: %s admins: %s" % (group_name_or_slot, admin_list))
    
    msg_list = []
    
    group = Vikundi.resolve (curr_admin, group_name_or_slot)

    if group is None:
        return [False, language.unknown_group (group_name_or_slot)]
    
    if not curr_admin.is_admin (group):
        msg_list.append(language.admin_privileges_required (group))
    
    if len(msg_list) > 0:
        return [False, string.join(msg_list, " ")]
    
    msg_list= []
    invalid_users = []
    non_members = []
    valid_users = []
    
    for admin_phone in admin_list:
        new_admin = Watumiaji.resolve (admin_phone)
        
        if new_admin == None:
            invalid_users.append(admin_phone)
        else:
            if not new_admin.is_member (group):
                non_members.append(admin_phone)
            else:
                if not new_admin.is_admin (group):
                    group.add_admin (curr_admin, new_admin)
                    valid_users.append(admin_phone)
    
    if len(valid_users) > 0:
        valid_users = string.join(valid_users, ",")
        msg_list.append(language.added_admin (valid_users, group))
    
    if len(non_members) > 0:
        non_members = string.join(non_members, ",")
        msg_list.append(language.admin_must_be_member (non_members))
    
    if len(invalid_users) > 0:
        invalid_users = string.join(invalid_users, ",")
        msg_list.append(language.unknown_user (invalid_users))
        
    return [False, string.join(msg_list, " ")]

#@resolve_user
def delete_admin_from_group (request, curr_admin, language, group_name_or_slot, del_admin_phone):
    admin_list = del_admin_phone.replace("+", " ").split()
    logger.debug("group: %s users: %s" % (group_name_or_slot, admin_list))
    
    msg_list = []
            
    group = Vikundi.resolve (curr_admin, group_name_or_slot)
    
    if group is None:
        return [False ,language.unknown_group (group_name_or_slot)]
    
    if not curr_admin.is_admin (group):
        msg_list.append(language.admin_privileges_required (group))
    
    # is he removing himself?
    for admin_phone in admin_list:
        del_admin = Watumiaji.resolve (admin_phone)
        
        if curr_admin.user_id == del_admin.user_id:
            admin_count = group.get_admin_count ()
            if admin_count == 1:
                msg_list.append(language.cannot_delete_only_admin (curr_admin, group))

    # have to stay admin of your own group
    if curr_admin.is_mine (group):
        msg_list.append(language.cannot_delete_self_from_my_group (curr_admin, group))
    
    if len(msg_list) > 0:
        return [False ,string.join(msg_list, " ")]
    
    msg_list = []
    valid_users = []
    invalid_users = []
    
    for admin_phone in admin_list:
        del_admin = Watumiaji.resolve(del_admin_phone)
        
        if del_admin == None:
            invalid_users.append(admin_phone)
        else:
            if del_admin.is_admin (group):
                group.delete_admin (curr_admin, del_admin)
            valid_users.append(admin_phone)
    
    if len (valid_users) > 0:
        valid_users = string.join(valid_users, ",")
        msg_list.append (language.deleted_admin (valid_users, group))
        
    if len (invalid_users) > 0:
        invalid_users = string.join(invalid_users, ",")
        msg_list.append(language.unknown_user (invalid_users))
    
    return [True, string.join(msg_list, " ") ]

#@resolve_user
def invite_user_to_group (request, user, language, group_name_or_slot, invite_user_phone, smsc = 'mosms'):
    from django.conf import settings
    
    #logger.debug('user: %s, language: %s, group: %s, phone: %s, smsc %s' % (user, language, group_name_or_slot, invite_user_phone, smsc))
    
    invited_user_list = invite_user_phone.replace("+", " ").replace(",", " ").split()
    name = ''
    
    if not invited_user_list[0].isdigit():
        name = invited_user_list[0]
        #if user hasnt registered a name add that as their name
        if not user.name_text:
            user.set_name(name)
        invited_user_list.remove(name)
    
    logger.debug ('group: %s users: %s' % (group_name_or_slot, invited_user_list))
    
    msg_list = []
    
    group = Vikundi.resolve (user, group_name_or_slot)
    
    if group is None:
        return [False, language.unknown_group (group_name_or_slot)]
    
    if not user.is_admin (group):
        if not group.is_public ():
            msg_list.append(language.cannot_invite_user ())
    
    if len(msg_list) > 0:
            return [False, string.join(msg_list, " ")]
    
    msg_list = []
    valid_users = []
    invalid_users = []
    
    for user_phone in invited_user_list:
        #make sure its a number
        phone_regex = re.compile("^\d+$")
        if not phone_regex.match(user_phone):
            continue
        
        invited_user = Watumiaji.resolve_or_create(request, user, language, user_phone)
        
        if invited_user == None:
            invalid_users.append(user_phone)
        else:
            if not invited_user.is_member(group):
                user.invite_user (invited_user, group)
                if invited_user.is_mine (group): group.group_name  = 'mine'
            valid_users.append(user_phone)
            
            origin = settings.SMS_VOICE[smsc]
            
            global_send_sms ("+" + invited_user.phone_number, name + " <"
                    + re.sub('^2547', '07', user.phone_number) + "> invited you to the "
                    + group.group_name + " group. Reply: join "
                    + group.group_name + ", to get their messages. "
                    + "Create ur own groups and tangaza by flashing %s. Enjoy!" % settings.SMS_VOICE['VOICE_%s' % origin], origin)
    
    if len(valid_users) > 0:
        valid_users = string.join(valid_users, ",")
        msg_list.append(language.invited_user (valid_users, group))
    
    if len(invalid_users) > 0:
        invalid_users = string.join(invalid_users, ",")
        msg_list.append(language.unknown_user (invalid_users))
    
    return [True, string.join(msg_list, " ")]
    
# convenience method for e.g. web site
# not to be called via sms
@resolve_user
def add_user_to_group (request, user, language, user_added_phone, group_name):
    user_added = Watumiaji.resolve_or_create(request, user, language, user_added_phone)
    group = Vikundi.resolve (user, group_name)
    
    if group is None:
        return [False, language.unknown_group (group_name)]
    
    if not user_added.has_empty_slot ():
        return [False, language.user_has_no_empty_slots ()]
    
    group.add_user (user, user_added)
    
    return [True, language.added_user_to_group (user, group)]
    
#@resolve_user
def delete_user_from_group (request, admin, language, group_name_or_slot, del_user_phone):
    del_user_list = del_user_phone.replace("+", " ").split()
    logger.debug ("group: %s users: %s" % (group_name_or_slot, del_user_list))
    
    msg_list = []
    
    group = Vikundi.resolve (admin, group_name_or_slot)
    
    if group is None:
        return [False, language.unknown_group (group_name_or_slot)]
    
    if len(del_user_list) < 1:
        return [False, language.no_user_specified()]
    
    del_user = Watumiaji.objects.filter(name_text = del_user_list[0])
    if not del_user:
        return [False, language.unknown_user(del_user_list[0])]
    
    if del_user[0].pk == admin.pk:
        msg_list.append(language.cannot_leave_own_group())
    
    if not admin.is_admin (group):
        msg_list.append(language.admin_privileges_required (group))
    
    if len(msg_list) > 0:
        return [False, string.join(msg_list, " ")]
    
    msg_list = []
    valid_users = []
    invalid_users = []
    non_members = []
    
    for user_phone in del_user_list:
        if user_phone.isdigit():
            del_user = Watumiaji.resolve(user_phone)
        else:
            #in case the admin used the members nickname
            del_user = Watumiaji.objects.filter(name_text = user_phone)
            if len(del_user) > 0:
                del_user = del_user[0]
        
        if not del_user:
            invalid_users.append(user_phone)
        else:
            if del_user.is_member (group):
                #delete as admin as well
                if del_user.is_admin (group):
                    group.delete_admin (admin, del_user_phone)
                
                group.delete_user (admin, del_user)
                valid_users.append(user_phone)
    
    if len(valid_users) > 0:
        valid_users = string.join(valid_users, ",")
        msg_list.append(language.deleted_user_from_group (valid_users, group))
    
    if len(invalid_users) > 0:
        invalid_users = string.join(invalid_users, ",")
        msg_list.append(language.unknown_user (invalid_users))
    
    return [True, string.join(msg_list, " ")]

#@resolve_user
def ban_user_from_group (request, user, language, ban_user_phone, group_name_or_slot):
    '''
    ban_user = Watumiaji.resolve(ban_user_phone)
    
    if ban_user == None:
        return [False, language.unknown_user (ban_user_phone)]
    
    group = Vikundi.resolve (admin, group_name_or_slot)
    
    if group == None:
        return [False, language.unknown_group (group_name_or_slot)]
    '''
    return [True, language.user_banned(ban_user_phone, group_name_or_slot)]

#@resolve_user
def unban_user_from_group (request, user, language, ban_user_phone, group_name_or_slot):
    	return [True, language.user_unbanned(ban_user)]

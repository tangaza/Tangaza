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

import string
import logging

from models import *
from django.db import transaction
from django.http import HttpResponse
from django.conf import settings

logger = logging.getLogger('tangaza_logger')

def resolve_user (func):
    
    def validate (*args):
        
        #logger.debug ('validate A')
        
        p = UserPhones.objects.filter(phone_number = args[1])
        
        if len(p) < 1:
            user = Users.create_user(args[1], args[1])
        else:
            user = p[0].user
        
        #logger.debug ('validate A2')
        
        user.phone_number = args[1]
    	
        # XXX pull out the users language from the DB
        language = LanguageFactory.create_language('eng')
        new_args = [args[0], user, language]
        arg_data = args[2:] #the other data e.g. slot, group name etc
        new_args.extend(arg_data)
        args = tuple(new_args)
        
        #logger.debug ('validate B')
        
        return HttpResponse(func(*args))
        
    return validate

def get_user_by_phone (phone):
    return Users.resolve(phone)

def auto_alloc_slot(user):
    logger.info("Auto allocation slot number")
    
    from sets import Set
    
    slots = Set(range(1, 10))
    used_slots = Set(user.get_used_slots())
    free_slots = slots.difference(used_slots)
    slots = list(free_slots)
    slots.sort()
    slot = slots[0]

    logger.info("Slot found: %d" % slot)
    
    return slot

# use standard ISO 639 codes
# swa -> swahili
# eng -> english
# http://en.wikipedia.org/wiki/ISO_639


##############################################################################
class Language(object):
     def slot_not_free(self, slot):
         return self._slot_status % (slot)

     def name_set (self, name):
         return self._name_set % (name)

     def group_too_big_for_sms (self, origin):
         return self._group_too_big_for_sms % (settings.SMS_VOICE["VOICE_%s" % origin])
     
     def invalid_group_type(self, group_type):
         return self._invalid_group_type % (group_type)
     
     def user_has_no_empty_slots(self):
         return self._user_has_no_empty_slots
     
     def group_name_not_available(self, group_name):
         return self._group_name_not_available % (group_name)

     def group_name_not_valid(self, group_name):
         return self._group_name_not_valid % (group_name)
     
     def unknown_group(self, group_name):
         return self._unknown_group % (group_name, group_name, group_name)
     
     def admin_privileges_required(self, group):
         return self._admin_privileges_required % (group.group_name)

     # XXX when only !foo given (no slot), first was called...
     def group_created(self, group_name, slot, group_type):
         if slot > 0:
             return self._group_created_w_slot % (group_type, group_name, slot)
         else:
             return self._group_created_no_slot % (group_name)
     
     def group_deleted(self, group):
         return self._group_deleted % (group.group_name)

     def already_member(self, group):
         return self._already_member % (group.group_name)
     
     def unknown_user(self, user):
         return self._unknown_user % (user)
     
     def already_admin(self, user, group):
         return self._already_admin % (user.phone_number, group.group_name)
     
     def added_admin(self, user, group):
         return self._added_admin % (user, group.group_name)
     
     def user_not_admin(self, user, group):
         return self._user_not_admin % (user.phone_number, group.group_name)
     
     def cannot_delete_only_admin(self, user, group):
         return self._cannot_delete_only_admin % (user.phone_number, group.group_name)

     def cannot_leave_when_only_admin(self, group):
         return self._cannot_leave_when_only_admin % group.group_name
     
     def cannot_delete_self_from_my_group(self):
         return self._cannot_delete_self_from_my_group
     
     def deleted_admin(self, user, group):
         return self._deleted_admin % (user, group.group_name)
     
     def cannot_invite_user(self):
         return self._cannot_invite_user
     
     def invited_user(self, user, group):
         return self._invited_user % (user, group.group_name)
     
     def added_user_to_group(self, user, group):
         return self._added_user_to_group % (user.phone_number, group.group_name)
     
     def user_not_in_group(self, user, group):
         return self._user_not_in_group % (user.phone_number, group.group_name)

     def nonmember_cannot_send(self, group):
         return self._nonmember_cannot_send % group.group_name

     def member_cannot_send(self, group):
         return self._member_cannot_send % group.group_name
     
     def deleted_user_from_group(self, user, group):
         return self._deleted_user_from_group % (user, group.group_name)
     
     def user_left_group(self, group):
         return self._user_left_group % (group)
     
     def current_groups(self, group_list):
         return self._current_groups % (group_list)
     
     def tangaza_info(self):
         return self._tangaza_info
     
     def user_banned(self, user, group):
         return self._user_banned % (user, group)
     
     def user_unbanned(self, user, group):
         return self._user_banned % (user, group)
     
     def cannot_leave_own_group (self):
         return self._cannot_leave_own_group

     def joined_group(self, group, slot):
         return self._joined_group % (group.group_name, slot)

     def cannot_join_without_invite(self, group):
         return self._cannot_join_without_invite % (group.group_name)
     
     def admin_must_be_member (self, admins):
         return self._admin_must_be_member % (admins)

     def group_quieted (self, group):
         return self._group_quieted % (group.group_name)
     
     def group_unquieted (self, group):
         return self._group_unquieted % (group.group_name)

     def unquieted_all_groups (self):
         return self._unquieted_all_groups

     def quieted_all_groups (self):
         return self._quieted_all_groups

     def user_update(self, msg):
         return self._user_update % (msg)
     
class EnglishLanguage(Language):
    def __init__(self):
        self._group_too_big_for_sms = "This group's size has exceeded the maximum allowed of 12, for sending sms Tangazos. Call %s to Tangaza using voice instead."
        self._name_set = "OK. Your name has been set. Your friends will now know you as %s."
        self._slot_status = "Slot %s is not available."
        self._invalid_group_type = "That group type %s does not exist."
        self._user_has_no_empty_slots  = "No more empty slots available."
        self._group_name_not_available = "The group name %s is already in use, please select another name."
        self._group_name_not_valid = "That new group name isn't valid: %s. Names must begin with a letter and be at least four letters or numbers."
        self._unknown_group = "The group %s does not exist. Try create %s to create it."
        self._admin_privileges_required = "You have to be the administrator of the %s group to carry out that operation."
        self._group_created_w_slot = "OK. Created the %s group %s, assigned key %s. Reply: invite groupname yourname friend1 friend2 to invite people. Use friend phone number"
        self._group_created_no_slot = "OK. Created group %s."
        self._group_deleted = "%s group deleted."
        self._already_member = "You are already a member of the %s group."
        self._unknown_user = "User(s) %s dont exist."
        self._already_admin = "%s is already an administrator of the %s group."
        self._added_admin = "%s added as an administrator of %s."
        self._deleted_admin = "%s deleted as administrator of the %s group."
        self._user_not_admin = "%s is not an administrator of the %s group."
        self._cannot_delete_only_admin = "Sorry.  %s is the only administrator of the %s group and cannot be deleted."
        self._cannot_leave_when_only_admin = "Sorry. You're the only admin, so you can't leave.  Make someone else an admin first: admin %s phone"
        self._cannot_delete_self_from_my_group = "You cannot delete yourself as the administrator on this group."
        self._cannot_invite_user = "You cannot invite users to this group. Only the group's administrator can do that."
        self._invited_user = "An invitation was sent to %s to join the group '%s'."
        self._added_user_to_group = "%s was added to the %s group."
        self._user_not_in_group = "%s is not a member of the %s group."
        self._nonmember_cannot_send = "Sorry. You need to be a member of a group to send to it.  Try join %s to join."
        self._member_cannot_send = "Sorry. You can only receive messages from this group, not send them: %s."
        self._deleted_user_from_group = "You deleted %s from the %s group."
        self._user_left_group = "You left the %s group."
        self._current_groups = "You current groups are %s."
        self._tangaza_info = "Information on Tangaza is currently not available please check later."
        self._user_banned = "%s banned from %s."
        self._user_unbanned = "Ban has been lifted. %s is a member of %s again."
        self._cannot_leave_own_group = "You cannot leave a group you created. You can only delete it."
        self._joined_group = "You joined the %s group, assigned key number %s."
        self._admin_must_be_member = "%s: not member(s). Administrator must be a member."
        self._cannot_join_without_invite = "%s is a private group. You cannot join without being invited."
        self._group_quieted = "You will no longer receive tangaza updates from the %s group."
        self._group_unquieted = "You will receive tangaza updates from the %s group from now on."
        self._quieted_all_groups = "You will no longer receive any tangaza updates."
        self._unquieted_all_groups = "You will receive tangaza updates from all groups that you are a member of."
        self._user_update = "Groups: %s"
        
class SwahiliLanguage(Language):
    def __init__(self):
       self._slot_status = "Nafasi %s kinatumika"
       self._group_too_big_for_sms = "Kikundi hiki ni kikubwa na kimepitisha idadi. Piga %s kutangaza ukitimia sauti yako."
       self._name_set = "Sawa. Marafiki wako sasa watakufahamu kama %s."
       self._invalid_group_type = "Kikundi aina %s hakiko" 
       self._user_has_no_empty_slots = "Hakuna nafasi tupu tena"
       self._group_name_not_available = "Jina la kikundi %s lishatumika, tafadhali chagua lingine"  
       self._group_name_not_valid = "Jina hilo la kikundi sio sahihi: %s"
       self._unknown_group = "Kikundi %s hakiko. Jaribu unda %s kukiunda kikundi hicho"
       self._admin_privileges_required = "Yafaa uwe mtengezaji wa kikundi %s ili kuendeleza kazi hiyo"
       self._group_created_w_slot = "Sawa. Umeunda kikundi %s kiitwacho %s kwenye nafasi ya %s"
       self._group_created_no_slot = "Sawa. Kukunid %s kimetengenezwa"
       self._group_deleted = "Kikundi %s kimefutwa"
       self._already_member = "Wewe tayari ni memba wa kikundi %s"
       self._unknown_user = "Hawa hawajapatikana %s"
       self._already_admin = "%s tayari ni mtengenezaji wa kikundi %s"
       self._added_admin = "%s ameongozwa kama mtengenezaji wa kikundi %s"
       self._deleted_admin = "%s ameondolewa kama mtengenezaji wa kikundi %s"
       self._user_not_admin = "%s sio mtengenezaji wa kikundi %s"
       self._cannot_delete_only_admin = "Samahani. %s ndiye mtengenezaji pekee aliyebaki katika kikundi %s"
       self._cannot_leave_when_only_admin = "Samahani. %s wewe ndiwe mtengenezaji pekee, hauwezi ondoka. Unda mtengenezaji mwingine kwanza: !simu ya mtengenezaji %s"
       self._cannot_delete_self_from_my_group = "Hauwezi kujiondoa kama mtengenezaji wa hiki kikundi"
       self._cannot_invite_user = "Hauwezi alika watumizi kwa hiki kikundi. Ni mtengenzaji wa kikundi hiki pekee anayeweza kufanya hivyo"
       self._invited_user = "Mwaliko umetumwa kwa %s kujiunga na kikundi %s"
       self._added_user_to_group = "%s ameongezwa kwa kikundi %s"
       self._user_not_in_group = "%s sio memba wa kikundi %s"
       self._nonmember_cannot_send = "Samahani. Ya bidi uwe memba wa hicho kikundi ili ukitangazie"
       self._member_cannot_send = "Samahani. Unaweza tu kupokea tangazo kutoka kwa hiki kikundi. Hauwezi tangaza; %s "
       self._deleted_user_from_group = "Umeondoa %s kutoka kwa kikundi %s"
       self._user_left_group = "Ulitoka kikundi %s"
       self._current_groups = "Vikundi ulivyo navyo sasa ni %s"
       self._tangaza_info = "Maelezo juu ya tangaza hayapo kwa sasa. Tafadhali jaribu tena baadaye"
       self._user_banned = "%s amezuiliwa kutoka kikundi %s"
       self._user_unbanned = "%s amekubaliwa kama memba wa kikundi %s"
       self._cannot_leave_own_group = "Hauwezi ondoka kutoka kikundi ulichounda, unaweza tu kukifuta"
       self._joined_group = "Umejiunga na kikundi %s, nafasi %s"
       self._cannot_join_without_invite = "Kikundi %s ni ya kibinafsi. Hauwezi kiunga kualikwa"
       self._admin_must_be_member = "%s  sio memba. mtengenezaji wa kikundi lazima awe memba."
       self._group_quieted = "Hautapokea tena matangazo kutoka kikundi %s"
       self._group_unquieted = "Utapokea matangazo kutoka kikundi %s kuanzia sasa"
       self._quieted_all_groups = "Hautapokea tena matangazo"
       self._unquieted_all_groups = "Utopokea matangazo kutoka kwa vikundi vyote ulivyo jiunga navyo"
       self._user_update = "Vikundi: %s"

class ShengLanguage(Language):
    def __init__(self):
        self._group_too_big_for_sms = ""
        self._slot_status = ""
        self._name_set = ""
        self._invalid_group_type = ""
        self._user_has_no_empty_slots = ""
        self._group_name_not_available = ""
        self._group_name_not_valid = ""
        self._unknown_group = ""
        self._admin_privileges_required = ""
        self._group_created_w_slot = ""
        self._group_created_no_slot = ""
        self._group_deleted = ""
        self._already_member = ""
        self._unknown_user = ""
        self._already_admin = ""
        self._added_admin = ""
        self._deleted_admin = ""
        self._user_not_admin = ""
        self._cannot_delete_only_admin = ""
        self._cannot_leave_when_only_admin = ""
        self._cannot_delete_self_from_my_group = ""
        self._cannot_invite_user = ""
        self._invited_user = ""
        self._added_user_to_group = ""
        self._user_not_in_group = ""
        self._nonmember_cannot_send = ""
        self._member_cannot_send = ""
        self._deleted_user_from_group = ""
        self._user_left_group = ""
        self._current_groups = ""
        self._tangaza_info = ""
        self._user_banned = ""
        self._user_unbanned = ""
        self._cannot_leave_own_group = ""
        self._joined_group = ""
        self._cannot_join_without_invite = ""
        self._admin_must_be_member = ""
        self._group_quieted = ""
        self._group_unquieted = ""
        self._quieted_all_groups = ""
        self._unquieted_all_groups = ""
        self._user_update = ""

class BlankLanguage(Language):
    def __init__(self):
        self._group_too_big_for_sms = ""
        self._name_set = ""
        self._slot_status = ""
        self._invalid_group_type = ""
        self._user_has_no_empty_slots = ""
        self._group_name_not_available = ""
        self._group_name_not_valid = ""
        self._unknown_group = ""
        self._admin_privileges_required = ""
        self._group_created_w_slot = ""
        self._group_created_no_slot = ""
        self._group_deleted = ""
        self._already_member = ""
        self._unknown_user = ""
        self._already_admin = ""
        self._added_admin = ""
        self._deleted_admin = ""
        self._user_not_admin = ""
        self._cannot_delete_only_admin = ""
        self._cannot_leave_when_only_admin = ""
        self._cannot_delete_self_from_my_group = ""
        self._cannot_invite_user = ""
        self._invited_user = ""
        self._added_user_to_group = ""
        self._user_not_in_group = ""
        self._nonmember_cannot_send = ""
        self._member_cannot_send = ""
        self._deleted_user_from_group = ""
        self._user_left_group = ""
        self._current_groups = ""
        self._tangaza_info = ""
        self._user_banned = ""
        self._user_unbanned = ""
        self._cannot_leave_own_group = ""
        self._joined_group = ""
        self._cannot_join_without_invite = ""
        self._admin_must_be_member = ""
        self._group_quieted = ""
        self._group_unquieted = ""
        self._quieted_all_groups = ""
        self._unquieted_all_groups = ""
        self._user_update = ""


class LanguageFactory(object):
    @classmethod
    def create_language(cls, language):
        if language == 'eng':
            return EnglishLanguage();
        elif language == 'swa':
            return SwahiliLanguage()
        elif language == 'shg':
            return ShengLanguage()
        elif language == 'xxx':
            return BlankLanguage()


text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
_null_trans = string.maketrans("", "")
def istext (u, text_characters=text_characters, threshold=0.30):

    #logger.debug ('u %s' % u)

    # if s contains any null, it's not text:
    if "\0" in u:
        return False
    # an "empty" string is "text":
    if not u:
        return True
    # Get the substring of s made up of non-text characters
    s = str (u)
    t = s.translate(_null_trans, text_characters)
    # s is 'text' if less than 30% of its characters are non-text ones:
    return len(t)/len(s) <= threshold

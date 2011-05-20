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

import re
import logging
import string
import urllib
import urllib2

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext

from utility import *
from appadmin import *
import grammar

logger = logging.getLogger(__name__)

# XXX for testing, should be put in DB
max_group_size = 200
MAX_GROUP_SMS_SIZE = 12

##############################################################################
# The front of the site

def welcome(request):
    '''Returns the default start page of the site'''
    return render_to_response('Tangaza/base_start.html',  context_instance=RequestContext(request))

##############################################################################
# Basic entry points for testing

def echo(request, phone, smsc, text):
    logger.debug ('from %s smsc %s text %s' % (phone, smsc, text))
    resp = ('Echo: from %s smsc %s text %s' % (phone, smsc, text))
    return HttpResponse(resp)

def sms_id(request, phone, smsc, id):
    logger.debug ('from %s smsc %s id %s' % (phone, smsc, id))
    resp = ('Echo: from %s smsc %s id %s' % (phone, smsc, id))
    return HttpResponse(resp)

def ping(request):
    logger.debug ('ping')
    return HttpResponse('pong')

##############################################################################
# Entry points that resolve the user, and wrap the response

@resolve_user
def update(request, user, language):
    return request_update (user,language)

#@resolve_user
def join_group (request, user, language, group_name, slot = '', username = '', smsc = 'mosms'):
    logger.debug("Starting join group user:%s group:%s" % (user, group_name))
    group = Vikundi.resolve (user, group_name)
    
    if group is None:
        logger.info ("smsc: %s user: %s unknown_group %s" % (smsc, user, group_name))
        return [False, language.unknown_group(group_name)]
    
    from django.conf import settings
    
    return request_join (user, language, group, slot, settings.SMS_VOICE[smsc])

#@resolve_user
def leave_group (request, user, language, group_or_slot):
    group = Vikundi.resolve (user, group_or_slot)
    if group is None:
        logger.info ("user %s unknown_group %s" % (user, group_or_slot))
        return [False, language.unknown_group(group_or_slot)]
    
    return request_leave (user, language, group)

##############################################################################
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@resolve_user
def index(request, user, language):
    
    logger.debug ('entry point')
    
    # XXX set language on-the-fly
    # or pull from db based on users selection on phone
    # language = LanguageFactory.create_language('eng')
    
    if request.method == "GET":
        logger.debug ('get request')
        return request_update (user,language)
    
    raw_text = request.raw_post_data.decode('UTF8')
    
    logger.info ('user: %s text: %s' % (user, raw_text))
    
    # empty request
    if not raw_text:
        return request_update (user,language)
    
    msg_list = []
    tokens = raw_text.split()
    parsed_text = grammar.parse(tokens, language)
    command = parsed_text['command']
    extras = parsed_text['extras']
    member = parsed_text['member']
    group_name = parsed_text['group']
    
    if command == language.CREATE:
        logger.debug('request create group %s' % group_name)
        # request, user, language, group_name, slot
        return request_create_group(request, user, language, group_name, '')[1]
    elif command == language.JOIN:
        logger.debug('request join group %s' % group_name)
        # request, user, language, group_name, slot
        return join_group(request, user, language, group_name)[1]
    elif command == language.INVITE:
        # (request, user, language, group_name_or_slot, invite_user_phone, smsc = 'mosms')
        logger.debug('request invite user %s to group %s' % (user, group_name))
        invited_users = ' '.join([member, extras])
        return invite_user_to_group(request, user, language, group_name, invited_users)[1]
    elif command == language.LEAVE:
        logger.debug('request leave group %s' % group_name)
        # leave_group (request, user, language, group_or_slot)
        return leave_group (request, user, language, group_name)[1]
    elif command == language.DELETE:
        logger.debug('request delete group %s' % group_name)
        # delete_group (request, admin, language, group_name_or_slot)
        return delete_group (request, user, language, group_name)[1]
    elif command == language.REMOVE:
        logger.debug('request remove user %s' % user)
        # delete_user_from_group (request, admin, language, group_name_or_slot, del_user_phone)
        return delete_user_from_group (request, user, language, group_name, member)[1]
    elif command == language.SETNAME:
        logger.debug('request set name user %s, username %s' % (user, username))
        return set_username(request, user, language, username)[1]
    else:
        return request_update (user,language)[1]


##############################################################################

def request_join (user, language, group, slot, origin):
    
    # SMS-only if no slot given
    
    logger.debug ("join group %s slot %s user %s" % (group, slot, user))
    
    # XXX group_name??
    # if group is None:
    #	return language.unknown_group(group_name)
    
    # check if there's another in the organization with that name
    org = group.org
    groups = Vikundi.objects.filter(org = org)
    
    ug_b = UserGroups.objects.filter(group__in = groups, user__name_text = user.name_text)
    
    if user.is_member(group):
        return [False, language.already_member(group)]
    
    if len(ug_b) > 0:
        return [False, u'A user with that name already exists in the organization.']
    
    if not user.has_empty_slot(): #and slot >= 0:
        return [False, language.user_has_no_empty_slots ()]
    
    if len(slot) < 1: #meaning user never provided a slot number
        slot = auto_alloc_slot(user)
	
	if slot == 0 or (slot > 0 and not user.slot_is_empty(slot)):
            return [False, language.slot_not_free(slot)]
	
	if not group.is_public() and not user.was_invited(group):
            return [False, language.cannot_join_without_invite (group)]
	
	if group.get_user_count() >= max_group_size:
            return [False, u'Sorry, groups sizes are limited, so you cannot be added to %s' % group.group_name]
        
	user.join_group(group, slot, origin)
	
	return [True, language.joined_group(group, slot)]

##############################################################################

def request_send(user, language, msg_text, group, origin):
    
    if not user.is_member(group):
        logger.info ("nonmember user %s tried to send to group %s" % (user, group))
        return [False, language.nonmember_cannot_send(group)]
    
    if not user.can_send(group):
        logger.info ("member user %s tried to send to group %s" % (user, group))
        return [False, language.member_cannot_send(group)]
    
    logger.info ("member user %s sent OK to group %s text %s" % (user, group, msg_text))
    
    # check for errors
    receipt_count = group.send_msg (user, msg_text, origin)
    
    # XXX turn into language
    if receipt_count == 0:
        return [False, ('Sorry, no one to send to.  Invite friends with invite %s' % group.group_name)]
    else:
        # if receipt_count == 1:
        # return ('T: %s <1>' % msg_text)
        # else:
        return [True, ('T<%d>: %s' % (receipt_count, msg_text))]

##############################################################################

def request_update (user, language):

    import string
    # XXX Still have to modify this to be lang indep
    
    update = []
    # 1: current groups
    groups = UserGroups.objects.filter(user = user).extra(order_by = ['slot'])
    
    g = [str(x.slot) + "@" + x.group.group_name for x in groups]
    g = string.join(g).replace(user.phone_number, 'mine') + ".\n"
    update.append(g)
    
    # 2: invitations
    invitations = Invitations.objects.filter(completed='no', invitation_to = user)
    i = ""
    if len(invitations) > 0:
        i = ["from: " + x.invitation_from.userphones_set.get().phone_number + "->"
             + x.group.group_name + "; " for x in invitations]
    i = "Invitations(" + str(len(invitations)) + ") " + string.join(i) + ".\n"
    update.append(i)
    
    # 3: new messages
    msgs = SubMessages.objects.filter(dst_user = user, heard = 'no')
    
    update.append("Messages(" + str(len(msgs)) + ")")
    
    logger.debug ("user %s" % user)	
    
    return [True, language.user_update(' '.join(update))]

##############################################################################
def request_leave (user, language, group):
	
    if group is None:
        logger.info ("user %s unknown_group %s" % (user, group))
        return [False, language.unknown_group(name_or_slot)]

    if not user.is_member(group):
        logger.info ("user %s not in group %s" % (user, group))
        return [False, language.user_not_in_group(user, group)]
    
    if user.is_admin(group):
        logger.debug ("admin=yes")
        
        if user.is_mine (group):
            # cannot delete our default group
            logger.debug ("mine=yes")
            logger.info ("user %s cannot leave own group" % user)
            return [False, language.cannot_leave_own_group()]
        
        logger.debug ("mine=no")
        
        if group.get_admin_count () == 1:
            logger.debug ("admin_count = 1")
            
            if group.get_user_count () > 1:
                logger.info ("user %s cannot leave only admin group %s" % (user, group))
                return [False, language.cannot_leave_when_only_admin(group)]
            else:
                # just one user: us
                # keep this in for now and test deletions
                user.leave_group(group)
                # Groups.delete (user, group)
                group.delete()
                logger.info ("user %s leaving and deleting group %s" % (user, group))
                return [True, ' '.join([language.user_left_group(group) , language.group_deleted (group)])]
        else:
            
            logger.debug ("admin_count > 1")
            logger.info ("admin user %s leaving group %s" % (user, group))
            user.leave_group(group)			
            
    else:
        
        # if we're not an admin, there must be other member
        # of the group, so we are free to leave
        logger.debug ("normal leave")
        logger.info ("normal user %s leaving group %s" % (user, group))
        user.leave_group(group)
	
    return [True, language.user_left_group(group.group_name)]

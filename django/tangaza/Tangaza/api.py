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
from tangaza.Tangaza import commands, views, utility
#from django.core import serializers
import json
import functools
from django.http import HttpResponse
from django.contrib import auth

logger = logging.getLogger(__name__)

def logout(request):
    auth.logout(request)
    return HttpResponse(json.dumps([{'status':0, 'message':'Logged out'}]))

def json_repr(queryset, fields=None):
    '''
    Django serializer doesnt display items in custom querysets
    e.g. if you use Model.objects.extra(select={'field'}...)
    This is a custom serializer that enables this
    '''
    items = [x.__dict__ for x in queryset]
    if not items:
        return json.dumps([{'status':1, 'message':''}])
    fields = items[0].keys() if fields == None else fields
    for item in items:
        for k in item.keys():
            if k.startswith('_') or k not in fields:
                del item[k]
    print 'b lot'
    return json.dumps(items)

def needs_login(func):
    @functools.wraps(func)
    def wrapper(*args):
        request = args[0]
        if request.user.is_authenticated():
            try:
                profile = request.user.get_profile()
            except Watumiaji.DoesNotExist:
                return HttpResponse(json.dumps([{'status':-1, 'message':'Profile not found'}]))
            
            phone = UserPhones.objects.filter(user = profile)[0]
            profile.phone_number = phone.phone_number
            
            language = utility.LanguageFactory.create_language(profile.language.name)
            new_args = [args[0], profile, language]
            new_args.extend(args[1:])
            args = tuple(new_args)
            return HttpResponse(func(*args)) # already json-formatted by json_repr
        else:
            return HttpResponse(json.dumps([{'status':-1, 'message':'User not logged in'}]))
    return wrapper
        
@needs_login
def get_members(request, member, language, group):
    '''
    Returns: 
     All members in the a particular group
     
    Args: 
     member- the member making the request, 
     group - the group whose members are being requested for
    '''
    fields = ['id', 'name_text', 'place_id']
    # first get all groups user x is a member of
    groups = [x.group for x in UserGroups.objects.filter(group__id = group, user = member)]
    # then get all members from these groups
    members = [x.user for x in UserGroups.objects.filter(group__in = groups)]
    return json_repr(members, fields)

@needs_login
def get_groups(request, member, language):
    '''
    Returns: 
     All groups that the user is a member of
     
    Args: 
     member - the member making the request
    '''
    fields = ['id', 'is_active', 'group_name_file', 'group_type', 'group_name']
    # only get groups that user x is a member of
    groups = [x.group for x in UserGroups.objects.filter(user = member)]
    return json_repr(groups, fields)

@needs_login
def get_messages(request, member, language):
    '''
    Returns: 
     The list of messages that member has received
     
    Args:
     member - the member making the request
    '''
    fields = ['id', 'message_path', 'date_sent', 'heard', 'flagged', 'group_id']
    messages = SubMessages.objects.filter(dst_user = member)
    messages = messages.extra(
        select={'message_path':'filename', 'group_id':'pub_messages.channel', 'date_sent':'sub_messages.timestamp'}, 
        tables=['pub_messages'], 
        where=['message_id=pub_messages.id'])
    
    for x in messages:
        x.message_path = ''.join(['http://', request.META['HTTP_HOST'], '/status/', x.message_path, '.gsm'])
        
    # return serializers.serialize('json', messages)
    return json_repr(messages, fields)

@needs_login
def get_admins(request, member, language, group):
    '''
    Returns: 
     The list of admins in the group
    
    Args:
     group - the group whose administrators are being requested for
    '''
    fields = ['name_text', 'id', 'name_file']
    admins = [x.user for x in GroupAdmin.objects.filter(group = group)]
    #return serializers.serialize('json', admins, fields = fields])
    return json_repr(admins, fields)

@needs_login    
def get_update(request, member, language):
    '''
    Returns:
     Your current status i.e. groups you are a member of, info on unheard messages, pending invites
    
    Args: 
     member - the member requesting this info
    '''
    update = views.request_update(member, language)[1]
    return json.dumps([{'message': update}])


##############################################################################
# POST methods from here on
##############################################################################
from tangaza.Tangaza import views

def json_output(func):
    @functools.wraps(func)
    def wrapper(*args):
        status, msg = func(*args)
        err = 0
        if not status:
            err = -1
        return HttpResponse(json.dumps([{'status': err, 'message':msg}]))
    return wrapper

def ensure_post(func):
    @functools.wraps(func)
    def wrapper(*args):
        request = args[0]
        if request.method != 'POST':
            return HttpResponse(json.dumps([{'status':-1, 'message':'This should be a POST request not a GET request.'}]))
        else:
            return func(*args)
    return wrapper

@ensure_post
@needs_login
@json_output
def request_join(request, member, language):
    '''
    Returns: 
     status - 0 if successfully joined, -1 if it failed; message - error or success message
    
    Args:
     member - the member trying to join a group
     group - the group that the member wants to join
    '''
    group = request.POST.get('group', '')
    if not group:
        return [False, 'Some parameters are missing']
    
    try:
        g = Vikundi.objects.get(group)
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return views.join_group(request, member, language, g.group_name)

@ensure_post
@needs_login
@json_output
def request_leave(request, member, language):
    '''
    Returns:
     status - 0 if successfully left group, -1 if it failed; message - error or success message
    
    Args:
     member - the member who is leaving the group
     group - the group that the member is leaving
    '''
    group = request.POST.get('group', '')
    if not group:
        return [False, 'Some parameters are missing']
    
    try:
        g = Vikundi.objects.get(group)
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return views.leave_group(request, member, language, g.group_name)

@ensure_post
@needs_login
@json_output
def request_quiet(request, member, language):
    '''
    Returns: 
     status - 0 if successfully set group to quiet, -1 if failed; message - error or success message
    
    Args:
     member - the who doesnt want to receive updates from the group
     group - the group that the member wants to put on silent mode
    '''
    group = request.POST.get('group', '')
    if not group:
        return [False, 'Some parameters are missing']
    
    try:
        g = Vikundi.objects.get(group)
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    return commands.quiet_group (request, member, language, g.group_name)

@ensure_post
@needs_login
@json_output
def request_unquiet(request, member, language):
    '''
    Returns:
     status - 0 if successfully set group to send updates, -1 if failed; message - error or success message
    
    Args:
     member - the member who wants to receive the updates
     group - the group that the member wants to receive updates from
    '''
    group = request.POST.get('group', '')
    if not group:
        return [False, 'Some parameters are missing']
    
    try:
        g = Vikundi.objects.get(id=group)
        if not member.is_member(g):
            return [False, 'Not Allowed']
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return commands.unquiet_group(request, member, language, g.group_name)

@ensure_post
@needs_login
@json_output
def set_username(request, member, language):
    '''
    Returns:
     status - 0 if a new username was set, -1 if it failed; message - error or success message
    Args:
     member - the member who wants to change their username
     username - a new username for the member
    '''
    username = request.POST.get('username', '')
    
    if not username:
        return [False, 'Some parameters are missing']
    
    return commands.set_username (request, member, language, username)

@ensure_post
@needs_login
@json_output
def request_create_group(request, member, language):
    '''
    Returns: 
     status - 0 if group created, -1 if it failed; message - error or success message
    Args:
     member - the member who wants to create a group
     group_name - the name of the group to be created
    '''
    group_name = request.POST.get('group_name', '')
    if not group_name:
        return [False, 'Some parameters are missing']
    
    return appadmin.request_create_group(request, member, language, group_name, '')

@ensure_post
@needs_login
@json_output
def request_delete_group(request, member, language, group):
    '''
    Returns: 
     status - 0 if group deleted, -1 if it failed; message - error or success message
    Args:
     member - the member deleting a group
     group - the id of group being deleted
    '''
    
    group = request.POST.get('group', '')
    if not group:
        return [False, 'Some parameters are missing']
    
    try:
        g = Vikundi.objects.get(id=group)
        if not member.is_member(g):
            return [False, 'Not Allowed']
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return appadmin.delete_group (request, user, language, group.group_name)

@ensure_post
@needs_login
@json_output
def request_invite_user(request, member, language):
    '''
    Returns: 
     status - 0 if invite was sent, -1 if it failed; message - error or success message
     
    Args:
     member - the member sending the invite
     group - the group the person is being invited to
     invited_user_phone - the phone number of the person being invited
    '''
    group = request.POST.get('group', '')
    invite_user_phone = request.POST.get('invite_user_phone', '')
    
    if not group or not invite_user_phone:
        return [False, 'Some parameters are missing']
    
    try:
        g = Vikundi.objects.get(id=group)
        if not member.is_member(g):
            return [False, 'Not Allowed']
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return appadmin.invite_user_to_group (request, member, language, g.group_name, invite_user_phone)

@ensure_post
@needs_login
@json_output
def request_add_admin(request, member, language):
    '''
    Returns:
     status - 0 if admin was successfully added, -1 if it failed; message - error or success message
    Args:
     member - the member (must be an administrator) who wants to add new administrator to the group
     group - the group to which the new administrator is being added
     new_admin - the new administrator being added to the group
    '''
    group = request.POST.get('group', '')
    new_admin = request.POST.get('new_admin', '')
    
    if not group or not new_admin:
        return [False, 'Some parameters are missing']
    
    try:
        admin = Watumiaji.objects.get(id=new_admin)
        admin.phone_number = UserPhones.objects.get(user = admin).phone_number
    except Watumiaji.DoesNotExist:
        return [False, 'Admin does not exist']
    
    try:
        g = Vikundi.objects.get(id=group)
        if not member.is_member(g):
            return [False, 'Not Allowed']
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return appadmin.add_admin_to_group (request, member, language, g.group_name, admin.phone_number)

@ensure_post
@needs_login
@json_output
def request_delete_admin(request, member, language):
    '''
    Returns:
     status - 0 if the admin was successfully deleted, -1 if it failed; message - error or success message
    
    Args:
     member - the member (must be an administrator) who wants to delete an administrator from the group
     group - the group from which the administrator is being deleted
     del_admin - the administrator that is being deleted from the group
    '''
    group = request.POST.get('group', '')
    del_admin = request.POST.get('del_admin', '')
    
    if not group or not del_admin:
        return [False, 'Some parameters are missing']
    
    try:
        admin = Watumiaji.objects.get(id=del_admin)
        admin.phone_number = UserPhones.objects.get(user = admin).phone_number
    except Watumiaji.DoesNotExist:
        return [False, 'Admin does not exist']
    
    try:
        g = Vikundi.objects.get(id=group)
        if not member.is_member(g):
            return [False, 'Not Allowed']
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return appadmin.delete_admin_from_group (request, member, language, g.group_name, admin.phone_number)

@ensure_post
@needs_login
@json_output
def request_delete_user(request, member, language):
    '''
    Returns: 
     status - 0 if the member was successfully deleted, -1 if it failed; message - error or success message
    
    Args:
     member - the member (must be an administrator) who wants to delete a member from the group
     group - the group from which the member is being deleted
     del_user - the member being deleted from the group
    '''
    group = request.POST.get('group', '')
    del_user = request.POST.get('del_user', '')
    
    if not group or not del_user:
        return [False, 'Some parameters are missing']
    
    try:
        user = Watumiaji.objects.get(id=del_user)
        user.phone_number = UserPhones.objects.get(user = user).phone_number
    except Watumiaji.DoesNotExist:
        return [False, 'Admin does not exist']
    
    try:
        g = Vikundi.objects.get(id=group)
        if not member.is_member(g):
            return [False, 'Not Allowed']
    except Vikundi.DoesNotExist:
        return [False, 'Group does not exist']
    
    return appadmin.delete_user_from_group (request, member, language, g.group_name, user)


############################################################
# NOTE: Features below not yet implemented
############################################################

@json_output
def request_ban_user(request):
    return appadmin.ban_user_from_group (request, user, language, ban_user_phone, group_name_or_slot)

@json_output
def request_unban_user(request):
    return appadmin.unban_user_from_group (request, user, language, ban_user_phone, group_name_or_slot)

@json_output
def request_tangaza_off(request):
    pass

@json_output
def request_tangaza_on(request):
    pass

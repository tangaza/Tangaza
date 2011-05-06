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
from django.core import serializers
import json

# TODO: Find a good way of returning errors
class ERRORS:
    err_not_member = 'you are not a member of this group'

def get_members(request, member, group):
    '''
    Returns: All members in the a particular group
    Parameters: 
     member- the member making the request, 
     group - the group whose members are being requested for
    '''
    fields = ['name_text', 'place_id']
    members = [x.user for x in UserGroups.objects.filter(group = group)]
    return serializers.serialize('json',  members, fields = fields)

def get_groups(request, member):
    '''
    Returns: All groups that the user is a member of
    Parameters: 
     member - the member making the request
    '''
    fields = ['is_active', 'group_name_file', 'group_type', 'group_name']
    group = [x.group for x in UserGroups.objects.filter(user = member)]
    groups = Vikundi.objects.filter(id__in = group)
    return serializers.serialize('json',  groups, fields = fields)

def get_messages(request, member):
    '''
    Returns: The list of messages that you have received
    Parameters:
     member - the member making the request
    '''
    #fields = ['message', 'timestamp', 'heard', 'flagged']
    messages = SubMessages.objects.filter(dst_user = member)
    return serializers.serialize('json', messages)
    
def get_admins(request, group):
    '''
    Returns: The list of admins in the group
    Parameters:
    '''
    fields = ['name_text']
    admins = [x.user for x in GroupAdmins.objects.filter(group = group)]
    return serializers.serialize('json', admins, fields = fields])
    
def get_update(request, member):
    '''
    Returns: Your current status i.e. groups you are a member of, info on unheard messages, pending invites
    Paramters: 
     member - the member requesting this info
    '''
    update = views.request_update(request, member)
    return json.JSONEncoder().encode({'message': update})


##############################################################################
# POST methods from here on
##############################################################################
from tangaza.Tangaza import views


def request_join(request, member, language, group_name):
    '''
    Returns: status - 0 if successfully joined, -1 if it failed; message - error or success message
    Parameters:
     member - the member trying to join a group
     group_name - the name of the group the member wants to join
    '''
    msg = views.join_group(request, member, language, group_name)
    err = 0
    if msg != language.joined_group(group, slot):
        err = -1
        
    return json.JSONEncoder().encode({'status': err, 'message':msg})

def request_leave(request, member, language, group_name):
    '''
    Returns: status - 0 if successfully left group, -1 if it failed; message - error or success message
    Parameters:
     member - the member who is leaving the group
     group_name - the name of the group being left
    '''
    msg = views.leave_group(request, member, language, group_name)
    err = 0
    if msg != language.user_left_group(group.group_name):
        err = -1
    return json.JSONEncoder().encode({'status': err, 'message':msg})

def request_quiet(request):
    pass

def request_unquiet(request):
    pass

def request_tangaza_off(request):
    pass

def request_tangaza_on(request):
    pass

def set_name(request, member):
    '''
    Returns: status - 0 if a new username was set, -1 if it failed; message - error or success message
    Parameters:
     member - the member who wants to change their username
    '''
    pass

def request_create_group(request, member, language, group_name):
    '''
    Returns: status - 0 if group created, -1 if it failed; message - error or success message
    Parameters:
     member - the member who wants to create a group
     group_name - the name of the group to be created
    '''
    msg = request_create_group(request, member, language, group_name, '')
    err = 0
    if msg != language.group_created(group_name, slot, group_type):
        err = -1
    return json.JSONEncoder().encode({'status':err, 'message':msg})

def request_delete_group(request, member, language, group_id):
    '''
    Returns: status - 0 if group deleted, -1 if it failed; message - error or success message
    Parameters:
     member - the member deleting a group
     group_id - the group being deleted
    '''
    group = Vikundi.objects.filter(id = group_id)
    msg = ''
    if not group:
        msg = language.unknown_group (group_name_or_slot)

    if not member.is_admin (group):
        msg = language.admin_privileges_required (group)
    
    if not msg:
        group.delete()
        msg = language.group_deleted(group)
        
    err = 0
    if msg != language.group_deleted(group):
        err = -1
    return json.JSONEncoder().encode({'status':err, 'message':msg})

def request_invite_user(request, member, language, group_name, invited_user_phone):
    '''
    Returns: status - 0 if invite was sent, -1 if it failed; message - error or success message
    Parameters:
     member - the member sending the invite
     group_name - the group the person is being invited to
     invited_user_phone - the phone number of the person being invited
    '''
    msg = invite_user_to_group (request, user, language, group_name, invite_user_phone)
    err = 0
    if msg != language.invited_user(invited_user_phone, group_name):
        err = -1
        
    return json.JSONEncoder().encode({'status':err, 'message':msg})

def request_add_admin(request):
    pass

def request_delete_admin(request):
    pass

def request_delete_user(request):
    pass

def request_ban_user(request):
    pass

def request_unban_user(request):
    pass

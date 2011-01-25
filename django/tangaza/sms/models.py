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
import urllib
import logging


from django.db import models
from django.db import transaction
from django.db.models.signals import *
from django.contrib.auth.models import User as AuthUser

logger = logging.getLogger('tangaza_logger')

# Note that because of settings in settings.py, each request is handled as its own transaction.

# Default slot is 1 (not 0)

ACTIVE_CHOICES = ((u'yes', u'Yes'),)
class Organization(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=100)
    org_admin = models.ForeignKey(AuthUser)
    is_active = models.CharField(max_length=3, choices=ACTIVE_CHOICES, null=True, blank=True)
    
    class Meta:
        db_table = u'organization'
        #app_label = u'Tangaza'
        
    def __unicode__(self):
        return self.org_name
    
    def delete (self):
        self.is_active = None
        self.save()
        
class SmsLog (models.Model):
    sms_id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=20)
    text = models.CharField(max_length=200)

    class Meta:
        db_table = 'sms_log'
        #app_label = u'Tangaza'

class Actions(models.Model):
    action_id = models.AutoField(primary_key=True)
    action_desc = models.CharField(max_length=90,unique=True)
    class Meta:
        db_table = u'actions'
        #app_label = u'Tangaza'
    
    def __unicode__(self):
        return self.action_desc

class OrderedUserManager(models.Manager):
    def get_query_set(self):
        users = super(OrderedUserManager, self).get_query_set()
        users = users.extra(select={'phone_number':'phone_number'}, tables=['user_phones'])
        users = users.extra(where=['user_phones.user_id=users.user_id'])
        users = users.order_by('phone_number')
        return users

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_pin = models.CharField(max_length=4, null=True, blank=True)
    name_text = models.CharField(max_length=20, verbose_name=u'Nickname')
    #objects = OrderedUserManager()
    
    class Meta:
        db_table = u'users'
        #app_label = u'Tangaza'
        verbose_name = u'Member'
    
    def __unicode__(self):
        #return '[user_id=' + str(self.user_id) +']'
        #return self.userphones_set.get().phone_number
        return self.name_text
    
    def set_name (self, name):
        self.name_text = name
        self.save()
    
    def get_used_slots(self):
        user_groups = UserGroups.objects.filter(user = self)
        used_slots = [ug.slot for ug in user_groups]
        return used_slots
        
    def is_mine (self, group):
        # true iff group is this users mine group
        # checked by seeing that he is the only admin
        if not group.group_type == 'mine':
            return False
        return self.is_admin(group)
    
    def slot_is_empty (self, slot):
        user_groups = UserGroups.objects.filter(user=self, slot=slot)
        return (len(user_groups) < 1)
    
    def has_empty_slot (self):
        user_groups = UserGroups.objects.filter(user=self)
        return len (user_groups) < 9
    
    def is_admin(self, group):
        grps = GroupAdmin.objects.filter(user=self, group=group)
        return len(grps) > 0
    
    def was_invited(self, group):
        inv_list = Invitations.objects.filter(group = group, completed = 'no', invitation_to = self)
        return len(inv_list) > 0
        
    @classmethod
    def resolve(cls, phone):
        try:
            if len(phone) > 0:
                if phone.startswith('07'):
                    phone = "254" + phone[1:]
            
            user = UserPhones.objects.get(phone_number = phone).user
            user.phone_number = phone
            user.language = ""
        except UserPhones.DoesNotExist:
            user = None
        return user
    
    @classmethod
    def resolve_or_create (cls, request, invoking_user, language, phone):
        if phone.startswith('07'):
            phone = "254" + phone[1:]
            
        user = cls.resolve (phone)
        if not user == None:
            return user
        
        return cls.create_user (phone, phone)
    

    def leave_group(self, group):
        UserGroups.objects.filter(user = self, group = group).delete()
        GroupAdmin.objects.filter(user = self, group = group).delete()

        #action = Actions.objects.get(action_desc = 'left group')
        #hist = UserGroupHistory(user = self, group = group, action = action)
        #hist.save()
        
    def invite_user(self, invited_user, group):
        invitation, created = Invitations.objects.get_or_create(group = group, 
                                invitation_to = invited_user, completed = 'no',
                                defaults = {'invitation_from': self})
        if not created:
            invitation.invitation_from = self
        
        invitation.save()
        action = Actions.objects.get(action_desc = 'invited user')
        hist = UserGroupHistory(user = self, group = group, action = action)
        hist.save()
        
    def is_member(self, group):
        grps = UserGroups.objects.filter(group = group, user = self)
        return len(grps) > 0

    def can_send(self, group):
        # assume membership already checked
        if group.is_public():
            return True
        if self.is_mine(group):
            return True
        return False

    def join_group(self, group, slot, origin, notify_admin = True):
        grps = UserGroups(user = self, group = group, slot= slot, is_quiet = 'no')
        grps.save()
        
        invs = Invitations.objects.filter(invitation_to = self, completed = 'no', group = group)
        for inv in invs:
            inv.completed = 'yes'
            inv.save()
        
        #notify admin(s) new user has joined
        if notify_admin:
            admins = GroupAdmin.objects.filter(group=group)
            for admin in admins:
                logger.debug("Notifying admin %s of new user in group" % admin.user)
                admin_phone = UserPhones.objects.get(user = admin.user, is_primary = 'yes')
                new_user_phone = UserPhones.objects.get (user = self)
                if self.name_text == None: self.name_text = ""
                text = "A new user %s<%s> has joined %s" % (self.name_text, new_user_phone.phone_number, group.group_name)
                sent = global_send_sms(admin_phone.phone_number, text, origin)
    
    @classmethod
    def create_user (cls, phone, own_group):

        logger.debug ('phone %s' % phone)
        
        user = Users()
        #additional info
        user.phone_number = phone
        user.language = ""
        user.save()

        country_name = Countries.phone2country (phone)
        country = Countries.objects.get(country_name=country_name)
        user_phone = UserPhones (country = country, phone_number = phone,
                                 user = user, is_primary = 'yes')
        user_phone.save()
        
        # NOTE: The commented bit below is now handled by user_created signal
        # to be removed once fully tested
        #group = Groups (group_name = own_group, group_type = 'mine', is_active = 'yes')
        #group.save()
        
        #user_group = UserGroups (user = user, group = group, slot = 1, is_quiet = 'no')
        #user_group.save()
        
        #action = Actions.objects.get (action_desc = 'joined group')
        #user_grp_hist = UserGroupHistory (group = group, action = action,
        #                                  user = user)
        #user_grp_hist.save()
        
        #grp_admin = GroupAdmin(user = user, group = group)
        #grp_admin.save()
        
        #action = Actions.objects.get (action_desc = 'created user')
        #admin_group_hist = AdminGroupHistory (group = group, action = action,
        #                                      user_src = user, user_dst = user)
        #admin_group_hist.save()

        #additional info
        #user.phone_number = phone
        #user.language = ""

        return user
    
YES_NO_CHOICES = ((u'yes', u'Yes'),(u'no', u'No'),)

class Groups(models.Model):
    
    GROUP_TYPES = ((u'mine', u'Mine'), (u'private', u'Private'), (u'public', u'Public'))
    
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=60,db_index=True)
    group_name_file = models.CharField(max_length=60, null = True, blank = True)
    group_type = models.CharField(max_length=21, choices=GROUP_TYPES[1:], default = u'private')
    is_active = models.CharField(max_length=3, choices=ACTIVE_CHOICES, null=True, blank=True)
    org = models.ForeignKey(Organization)
    
    class Meta:
        db_table = u'groups'
        #app_label = u'Tangaza'
        unique_together = ("group_name","is_active")
        ordering = ['group_name']
        verbose_name = u'Group'
        
    def __unicode__(self):
        #for group admin to work we cant return in this format 
        #        return '[id=' + str(self.group_id) + ',name=' + self.group_name + ',type=' + self.group_type + ',active=' + self.is_active+']'
        return self.group_name

    def get_admin_count (self):
        admins = GroupAdmin.objects.filter (group = self)
        return admins.count()

    def get_user_count(self):
        user_set = UserGroups.objects.filter (group = self)
        #logger.debug ("count = %d" % len(user_set))
        return user_set.count()


    def is_public(self):
        return self.group_type == 'public'

    def is_private(self):
        return self.group_type == 'private'
    
    def set_quiet(self, user):
        usr_grp = UserGroups.objects.get(group = self, user = user)
        usr_grp.is_quiet = 'yes'
        usr_grp.save()
        
        #set heard to yes to cancel previous but unheard updates
        subs = SubMessages.objects.filter(dst_user = user, channel = self)
        for s in subs:
            s.heard = 'yes'
            s.save()
        
        action = Actions.objects.get(action_desc = 'quieted group')
        hist = UserGroupHistory(group = self, action = action, user = user)
        hist.save()
        
    def unquiet(self, user):
        usr_grp = UserGroups.objects.get(group = self, user = user)
        usr_grp.is_quiet = 'no'
        usr_grp.save()

        action = Actions.objects.get(action_desc = 'unquieted group')
        hist = UserGroupHistory(group = self, action = action, user = user)
        hist.save()

    @classmethod
    def quiet_all(cls, user):
        usr_grp_list = UserGroups.objects.filter(user = user)
        for usr_grp in usr_grp_list:
            grp = usr_grp.group
            grp.set_quiet(user)
    
    @classmethod
    def unquiet_all(cls, user):
        usr_grp_list = UserGroups.objects.filter(user = user)
        for usr_grp in usr_grp_list:
            grp = usr_grp.group
            grp.unquiet(user)
            
            
    def add_admin(self, admin_doing_add, admin_being_added):
        admin = GroupAdmin (user = admin_being_added, group = self)
        admin.save()
        
        add_action = Actions.objects.get (action_desc='added admin')
        
        history = AdminGroupHistory(group = self, action = add_action, user_src = admin_doing_add,
                                    user_dst = admin_being_added)
        history.save()
        
    def delete_admin (self, admin_doing_delete, admin_being_deleted):
        GroupAdmin.objects.filter (user = self, group = group).delete()
        
        action = Actions.objects.get(action_desc = 'deleted admin')
        hist = AdminGroupHistory(group = self, action = action, user_src = admin_doing_delete,
                                 user_dst = admin_being_deleted)
        hist.save()


    def add_user (self, admin_doing_add, user_being_added):
        group = UserGroups(user = user_being_added, group = self, is_quiet = 'n')
        group.save()
        
        #action = Actions.objects.get(action_desc = 'joined group')
        #user_hist = UserGroupHistory(group = self, action = action, user = user_being_added)
        #user_hist.save()

        action = Actions.objects.get(action_desc = 'added user')
        admin_hist = AdminGroupHistory(group = self, action = action, user_src = admin_doing_add, 
                                       user_dst = user_being_added)
        admin_hist.save()


    def delete_user (self, admin_doing_delete, user_being_deleted):
        UserGroups.objects.filter(user=user_being_deleted, group = self).delete()

        action = Actions.objects.get(action_desc = 'deleted user')
        hist = AdminGroupHistory(group = self, action = action, user_src = admin_doing_delete,
                                 user_dst = user_being_deleted)
        hist.save()
        

    @classmethod
    # if name_or_slot is None, then resolve to users 'mine' group
    def resolve(cls, user, name_or_slot):
        group = None

        if name_or_slot.lower() == 'my' or name_or_slot.lower() == 'mine' or \
            name_or_slot is None or len(name_or_slot) < 1:
            name_or_slot = user.phone_number
        
        regex = re.compile('^\d$')
        if regex.match(name_or_slot):
            grps = UserGroups.objects.filter(user = user, slot = name_or_slot)
            logger.debug ("used: user_group %s" % grps)
            if len(grps) > 0: group  = grps[0].group
        else:
            grps = Groups.objects.filter(group_name = name_or_slot, is_active = 'yes')
            logger.debug ("used: group %s" % grps)
            if len(grps) > 0: group  = grps[0]

        return group

    @classmethod
    def is_name_available (cls, name):
        grps = cls.objects.filter(group_name = name, is_active = 'yes')
        return len(grps) < 1
    
    @classmethod
    def create (cls, user, group_name, slot, group_type='private', org = None):
        group = Groups(group_name = group_name, group_type = group_type, org = org)
        group.save()
        
        grp_admin = GroupAdmin(user = user, group = group)
        grp_admin.save()
        
        usr_grp = UserGroups(group = group, user = user, is_quiet = 'no', slot = slot)
        usr_grp.save()
        
        # NOTE: the commented bit handled by signals. still testing
        #action = Actions.objects.get(action_desc = 'created group')
        #hist = AdminGroupHistory(group = group, action = action, user_src = user, user_dst = user)
        #hist.save()
        
        #usr_hist = UserGroupHistory(group = group, action = action, user = user)
        #usr_hist.save()
        return group

    @classmethod
    def delete (cls, admin=None, group=None):
        grp = cls.objects.get(group_id = group.group_id)
        grp.is_active = None
        UserGroups.objects.filter (group = group).delete()
        GroupAdmin.objects.filter (group = group).delete()
        Invitations.objects.filter (group = group).delete()
        grp.save()

        action = Actions.objects.get(action_desc = 'deleted group')
        hist = AdminGroupHistory(group = group, action = action, user_src = admin, user_dst = admin)
        hist.save()

    def send_msg (self, user, text, origin):
        logger.debug ("group %s user %s text %s" % (self, user,text))

        user_set = UserGroups.objects.filter (group = self, is_quiet = 'no')

        count = 0
        for dst_user in user_set:
            logger.debug ("dst_user %s" % dst_user)

            user_phone = UserPhones.objects.get (user = dst_user.user_id, is_primary = 'yes')
            if dst_user.user_id == user.user_id:
                logger.debug ("not sending to self %s" % user_phone)
                continue
            else:
                logger.debug ("user_phone %s" % user_phone)
                
                sent = global_send_sms(user_phone.phone_number, text, origin)
                if sent: count += 1
                
        return count
    
    @classmethod
    def is_valid_type (cls, type_name):
        return dict(GROUP_TYPES).has_key(type_name)


class AdminGroupHistory(models.Model):
    admin_group_hist_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Groups)
    action = models.ForeignKey(Actions)
    user_src = models.ForeignKey(Users, related_name = 'src')
    user_dst = models.ForeignKey(Users, related_name = 'dst')
    #JL this wasnt here before. what happens if there's no user_dst?
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = u'admin_group_history'
        #app_label = u'Tangaza'

class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_code = models.IntegerField()
    country_name = models.CharField(max_length=40)
    
    class Meta:
        db_table = u'countries'
        #app_label = u'Tangaza'
        ordering = ['country_name']
        
    def __unicode__(self):
        return self.country_name
    
    @classmethod
    def phone2country(cls, phone):
        return 'kenya'


class GroupAdmin(models.Model):
    group_admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users)
    group = models.ForeignKey(Groups)
    
    class Meta:
        db_table = u'group_admin'
        #app_label = u'Tangaza'
        verbose_name = u'Group Admin'
        unique_together = (('user', 'group'))
    
    def __unicode__(self):
        return self.group.group_name
    
class Invitations(models.Model):
    invitation_id = models.AutoField(primary_key=True)
    invitation_to = models.ForeignKey(Users, related_name='to',db_index=True)
    invitation_from = models.ForeignKey(Users, related_name='from')
    group = models.ForeignKey(Groups)
    create_stamp = models.DateTimeField(auto_now_add=True)
    completed = models.CharField(max_length=9, choices = YES_NO_CHOICES, default = 'no')
    class Meta:
        db_table = u'invitations'
        #app_label = u'Tangaza'

#XXX Odero kannel should probably store this, not us
class SmsRawmessage(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=120)
    timestamp = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=1536)
    class Meta:
        db_table = u'sms_rawmessage'
        #app_label = u'Tangaza'

class UserGroupHistory(models.Model):
    user_group_hist_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Groups)
    action = models.ForeignKey(Actions)
    user = models.ForeignKey(Users)
    create_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = u'user_group_history'
        #app_label = u'Tangaza'

class UserGroups(models.Model):
    user_group_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users)
    group = models.ForeignKey(Groups)
    is_quiet = models.CharField(max_length=9, choices=YES_NO_CHOICES, default='no')
    slot = models.PositiveIntegerField()
    class Meta:
        db_table = u'user_groups'
        #app_label = u'Tangaza'
        verbose_name = u'User Group'
        unique_together = (('user','slot'), ('user','group'),)

    def __unicode__(self):
        return "Group: %s, Slot: %d" % (self.group.group_name, self.slot)
    
class UserPhones(models.Model):
    phone_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Countries)
    phone_number = models.CharField(max_length=120,db_index=True,unique=True)
    user = models.ForeignKey(Users,db_index=True)
    is_primary = models.CharField(max_length=9, choices=YES_NO_CHOICES, default = 'yes')
    class Meta:
        db_table = u'user_phones'
        #app_label = u'Tangaza'
        verbose_name = u'User Phone'
        ordering = ['phone_number']
        
    def __unicode__(self):
        return '[phone=' + self.phone_number + ',primary=' + self.is_primary + ']'

class PubMessages(models.Model):
    pub_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    src_user = models.ForeignKey(Users)
    channel = models.ForeignKey(Groups, db_column = "channel")
    filename = models.CharField(max_length=30)
    text = models.CharField(max_length=250)
    class Meta:
        db_table = u'pub_messages'
        #app_label = u'Tangaza'

class SubMessages(models.Model):
    sub_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(PubMessages)
    timestamp = models.DateTimeField(auto_now_add=True)
    dst_user = models.ForeignKey(Users)
    heard = models.CharField(max_length=9, choices=YES_NO_CHOICES)
    flagged = models.CharField(max_length=9, choices=YES_NO_CHOICES)
    channel = models.ForeignKey(Groups, db_column = "channel")
    class Meta:
        db_table = u'sub_messages'
        #app_label = u'Tangaza'
        
def global_send_sms (dest_phone, text, origin = 'KE'):
    from django.conf import settings
    
    username = settings.SMS_VOICE['SMS_USERNAME_%s' % origin]
    password = settings.SMS_VOICE['SMS_PASSWORD_%s' % origin]
    source = settings.SMS_VOICE['SMS_FROM_%s' % origin]
    sms_url = settings.SMS_VOICE['SMS_URL_%s' % origin]
    
    sent = False
    
    if origin == 'KE':
        params = urllib.urlencode ({'username':username, 'password':password, 'source':source,
                                    'destination':dest_phone, 'message': text[:160]})
    else:
        params = urllib.urlencode ({'username':username, 'password':password, 'from':source,
                                    'to':dest_phone, 'text': text[:160]})
        
    try:
        logger.debug("Request made: %s?%s" % (sms_url, params))
        resp = urllib.urlopen ("%s?%s" % (sms_url, params))
        logger.debug (resp.read())
        
        #logger.debug ('not sending for now')
        sent = True
    except URLError:
        logger.info ('failed: %s' % url)
        
    return sent

#############################################################################################
# Extend Auth user to work with Users
AuthUser.add_to_class('member_profile', models.ForeignKey(Users))

#############################################################################################
# Signal handlers for post-actions

def user_left_group(sender, **kwargs):
    logging.debug("Deleting user group %s" % kwargs)
    
    action = Actions.objects.get(action_desc = 'left group')
    user_group = kwargs['instance']
    hist = UserGroupHistory(user = user_group.user, group = user_group.group, action = action)
    hist.save()

post_delete.connect(user_left_group, sender=UserGroups)

def user_joined_group(sender, **kwargs):
    if not kwargs['created']:
        return
    
    action = Actions.objects.get(action_desc = 'joined group')
    user_group = kwargs['instance']
    hist = UserGroupHistory(user = user_group.user, group = user_group.group, action = action)
    hist.save()

post_save.connect(user_joined_group, sender=UserGroups)

def user_created(sender, **kwargs):
    if not kwargs['created']:
        return
    
    instance = kwargs['instance']
    user = instance.user
    
    #if its a new user there'll be only one of it in user_phones table
    #if just adding an additional number there'll be more than 1
    u = UserPhones.objects.filter(user=user)
    if len(u) > 1:
        return
    
    group = Groups (group_name = instance.phone_number, group_type = 'mine', is_active = 'yes')
    group.save()
    
    user_group = UserGroups (user = user, group = group, slot = 1, is_quiet = 'no')
    user_group.save()
    
    grp_admin = GroupAdmin(user = user, group = group)
    grp_admin.save()
    
    action = Actions.objects.get (action_desc = 'created user')
    admin_group_hist = AdminGroupHistory (group = group, action = action,
                                          user_src = user, user_dst = user)

#post_save.connect(user_created, sender=UserPhones)

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

post_save.connect(group_created, sender=GroupAdmin)

from django.template.defaultfilters import slugify
def organization_created(sender, **kwargs):
    if not kwargs['created']:
        return
    instance = kwargs['instance']
    
    #create group with same name
    
#post_save.connect(organization_created, sender=Organization)

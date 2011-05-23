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

from django.db import models
from django.contrib.auth.models import User
import logging
import re

logger = logging.getLogger(__name__)

# Some default values for database fields

GROUPTYPE = (
    ('mine', 'Mine'),
    ('private', 'Private'),
    ('public', 'Public'),
)

WATUMIAJI_STATUS = (
    ('good', 'Good'),
    ('bad', 'Bad'),
    ('blacklisted', 'Blacklisted'),
)

LEVELS = (
    ('basic', 'Basic'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
)

NOTIFY_STATUS = (
    ('off', 'Off'),
    ('on', 'On'),
)

YES_NO = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

YES_NULL = (
    ('yes', 'Yes'),
)
class Actions(models.Model):
    '''
    Actions by users of the system.
    Tangaza keeps a log of all the actions performed by the users. Actions model provides the list of allowable actions
    '''
    action_desc = models.CharField(max_length=270)
    class Meta:
        db_table = u'actions'

class Languages(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        db_table = u'languages'
        ordering = [u'name']
    
    def __unicode__(self):
       return self.name

class SmsLog(models.Model):
    '''Keeps a log of all smses received by the system'''
    sender = models.CharField(max_length=60)
    text = models.CharField(max_length=600, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = u'sms_log'

class Watumiaji(models.Model):
    '''
    This is the profile for membership in Tangaza groups. 
    For any user to be able to communicate using Tangaza they need such a profile.
    '''
    user_pin = models.CharField(max_length=18, blank=True, null=True, default=None)
    status = models.CharField(max_length=33, choices = WATUMIAJI_STATUS, default='good', 
                              help_text=u'Is the member considered good, bad or blacklisted by the admin?')
    place_id = models.IntegerField(default=1, help_text=u'Where are they from?')
    level = models.CharField(max_length=24, choices = LEVELS, default='advanced', help_text=u'Level of expertise in using the system')
    callback_limit = models.IntegerField(default = 60, help_text=u'How much free talk time (seconds) remaining?')
    invitations_remaining = models.IntegerField(default = 100, help_text=u'How many invitations remaining to be sent out?')
    language = models.ForeignKey(Languages, default=1, help_text=u'Preferred language')
    name_file = models.CharField(max_length=96, blank=True, help_text=u'File path to the speech recorded name')
    name_text = models.CharField(max_length=255, db_index=True, verbose_name=u'Username')
    create_stamp = models.DateTimeField(auto_now_add=True)
    modify_stamp = models.DateTimeField(auto_now=True)
    notify_stamp = models.DateTimeField(null=True, help_text=u'When were they last notified that you have new messages?')
    notify_period = models.TimeField(auto_now_add=True, help_text=u'What time of the day would they like to be notified?')
    dirty = models.CharField(max_length=9, choices=YES_NO, default='no')
    notify_status = models.CharField(max_length=9, choices=NOTIFY_STATUS, default='on', 
                                     help_text=u'Would they like to use the defined notification settings?')
    accepted_terms = models.CharField(max_length=9, choices=YES_NO, default='no')
    dirty_time = models.DateTimeField(null=True)
    notify_time = models.DateTimeField(null=True, help_text=u'Last time they were notified')
    calling_time = models.DateTimeField(null=True, help_text=u'When was their last call?')
    user = models.OneToOneField(User, unique=True, null=True, blank=True, verbose_name=u'Administrator account', 
                             help_text=u"What is their web admin account?")
    
    class Meta:
        db_table = u'watumiaji'
        verbose_name_plural = u'Tangaza Member Profiles'
        verbose_name = u'Tangaza Member Profile'
        ordering = [u'name_text']
    
    def __unicode__(self):
       return self.name_text
    
    def get_used_slots(self):
        '''
        Slots represent the number on the keypad assigned to a group
        All users (except the super user) have maximum 9 slots
        '''
        user_groups = UserGroups.objects.filter(user = self)
        used_slots = [ug.slot for ug in user_groups]
        return used_slots
    
#    def delete(self):
#        #yet to decide on how to deal with this
#        pass
    
    def set_name (self, name):
        '''Set the member's nickname'''
        self.name_text = name
        self.save()
        
    def is_mine (self, group):
        '''Checks if the member owns the vikundi/group'''
        # true iff group is this users mine group
        # checked by seeing that he is the only admin
        if not group.group_type == 'mine':
            return False
        return self.is_admin(group)
    
    def slot_is_empty (self, slot):
        '''Returns False if the slot that the user is trying to use is already in use. True otherwise.'''
        user_groups = UserGroups.objects.filter(user=self, slot=slot)
        return (len(user_groups) < 1)
    
    def has_empty_slot (self):
        '''Returns False if the user alread has 9 groups (and thus no empty slots to use). Returns True otherwise.'''
        user_groups = UserGroups.objects.filter(user=self)
        return len (user_groups) < 9
    
    def is_admin(self, group):
        '''Returns True if the user is an administrator of the provided group. Returns False otherwise.'''
        grps = GroupAdmin.objects.filter(user=self, group=group)
        return len(grps) > 0
    
    def was_invited(self, group):
        '''
        A user can only join a group if they were invited. 
        This method returns True if the user was invited to the group they are trying to join.
        '''
        inv_list = Invitations.objects.filter(group = group, completed = 'no', invitation_to = self)
        return len(inv_list) > 0
    
    @classmethod
    def resolve(cls, phone):
        '''Resolves the phone number provided and returns the member associated with it.'''
        try:
            if len(phone) > 0:
                if phone.startswith('07'):
                    phone = "254" + phone[1:]
            
            user = UserPhones.objects.get(phone_number = phone).user
            user.phone_number = phone
            #user.language = ""
        except UserPhones.DoesNotExist:
            user = None
            
        return user
    
    @classmethod
    def resolve_or_create (cls, request, invoking_user, language, phone):
        '''
        Works similar to resolve() but creates the member if they do not exist, 
        then returns the associated member object
        '''
        if phone.startswith('07'):
            phone = "254" + phone[1:]
        
        user = cls.resolve (phone)
        
        if not user == None:
            return user
        
        return cls.create_user (phone, phone)
    
    def leave_group(self, group):
        '''When a user leaves, this deletes any links to vikundi in the UserGroups and GroupAdmin tables in the database'''
        UserGroups.objects.filter(user = self, group = group).delete()
        GroupAdmin.objects.filter(user = self, group = group).delete()
        
    def invite_user(self, invited_user, group):
        '''
        Adds an entry to the Invitation model to show that the user was invited and can thus join the group. 
        Check ``was_invited``.
        '''
        invitation, created = Invitations.objects.get_or_create(group = group,
                                                                invitation_to = invited_user, completed = 'no',
                                                                defaults = {'invitation_from': self})
        if not created:
            invitation.invitation_from = self
            
        invitation.save()
        
    def is_member(self, group):
        '''
        Returns True if the user is a member of the group, and False otherwise
        '''
        grps = UserGroups.objects.filter(group = group, user = self)
        return len(grps) > 0
    
    def can_send(self, group):
        '''
        Returns True if the user can send messages to this group, otherwise returns False
        You can only send messages to a group that you are a member of.
        '''
        # assume membership already checked
        if (group.is_public() or self.is_mine(group)) and group.is_active == 'yes':
            return True
        return False
    
    def join_group(self, group, slot, origin, notify_admin = True):
        '''
        Adds an entry to the ``UserGroup`` model to show that the user has joined the group. 
        It also marks ``completed`` flag in the ``Invitation`` model as 'yes'.
        '''
        grps = UserGroups(user = self, group = group, slot= slot, is_quiet = 'no')
        grps.save()
        
        invs = Invitations.objects.filter(invitation_to = self, completed = 'no', group = group)
        for inv in invs:
            inv.completed = 'yes'
            inv.save()
        
        #notify admin(s) new user has joined
        if notify_admin:
            admins = GroupAdmin.objects.filter(group = group)
            for admin in admins:
                logger.debug("Notifying admin %s of new user in group" % admin.user)
                admin_phone = UserPhones.objects.get(user = admin.user, is_primary = 'yes')
                new_user_phone = UserPhones.objects.get (user = self)
                if self.name_text == None: self.name_text = ""
                text = "A new user %s<%s> has joined %s" % (self.name_text, new_user_phone.phone_number, group.group_name)
                sent = global_send_sms(admin_phone.phone_number, text, origin)
    
    @classmethod
    def create_user (cls, phone, own_group):
        '''Creates a user with group type mine and assigns phone as primary phone number'''
        logger.debug ('Beginning create user: phone %s' % phone)
        user = Watumiaji(name_text='User_'+phone)
        
        #additional info
        user.phone_number = phone
        user.language = Languages.objects.get(name='English')
        user.save()
        
        country_name = Countries.phone2country (phone)
        country = Countries.objects.get(country_name=country_name)
        user_phone = UserPhones (country = country, phone_number = phone,
                                 user = user, is_primary = 'yes')
        user_phone.save()
        
        return user

class Organization(models.Model):
    '''
    An organization is the highest level container for all entities within Tangaza. 
    All Tangaza users (except the superuser) must belong to an organization.
    '''
    org_name = models.CharField(max_length=210, db_index=True, verbose_name=u'Name', help_text="The name of the Organisation")
    org_admin = models.ForeignKey(User, verbose_name=u'Administrator', help_text="Who is the administrator of this organization?")
    #tangaza_account = models.ForeignKey(Watumiaji, help_text="What is their Tangaza account?")
    toll_free_number  = models.CharField(max_length=21,help_text="What is the toll free number this organisation are using?")
    is_active =  models.CharField(max_length=9, choices=YES_NULL, null=True, default='yes')
    
    class Meta:
        db_table = u'organization'
        ordering = [u'org_name']
        
    def __unicode__(self):
       return self.org_name

    def activate(self):
        '''Reactivates previously deactivated organizations so that their users can resume using Tangaza'''
        self.is_active = 'yes'
        self.save()
        
        #Change the users staff status
        auth_user = User.objects.get(pk = self.org_admin.pk)
        auth_user.is_staff = 1
        auth_user.save()
        
        #Activate the groups as well
        groups = Groups.objects.filter(org = self)
        map(lambda g: g.activate(), groups)
        
    def deactivate(self):
        '''
        Deactivates the organization such that users in these organizations should not be able to use Tangaza.
        '''
        self.is_active = None
        self.save()
        
        #Change the users staff status
        auth_user = User.objects.get(pk = self.org_admin.pk)
        auth_user.is_staff = 0
        auth_user.save()
        
        #Deactivate the groups as well 
        groups = Groups.objects.filter(org = self)
        map(lambda g: g.deactivate(), groups)
        
#    def delete (self):
#        self.deactivate()

class VikundiManager(models.Manager):
    def get_query_set(self):
        return super(VikundiManager, self).get_query_set().annotate(
            models.Count('usergroups')).annotate(
            models.Count('groupadmin')).annotate(
                models.Count('pubmessages'))
            
class Vikundi(models.Model):
    '''
    A group within Tangaza. People using Tangaza have to be members to send/receive messages
    
    Types::
     
     Mine - Personal. Only the owner can send messages. You have to be invited to join
     Private - You can only send messages if you are a member. You have to be invited to join
     Public - Anyone can send messages to these. You can join without being invited
    '''
    group_name = models.CharField(max_length=180,db_index=True)
    group_name_file = models.CharField(max_length=96, blank=True, help_text=u'File path to the speech recorded group name')
    group_type = models.CharField(max_length=7,choices=GROUPTYPE[1:], default='private')
    is_active = models.CharField(max_length=9, blank=True, choices=YES_NO, default='yes')
    org = models.ForeignKey(Organization, verbose_name=u'Organization')
    objects = VikundiManager()
    
    class Meta:
        db_table = u'vikundi'
        verbose_name_plural = u'Groups'
        verbose_name = u'Group'
        ordering = [u'group_name']
        unique_together = ('group_name','org')
    
    def user_count(self):
        '''Returns the total number of users in a group/vikundi'''
        return u'%s' % UserGroups.objects.filter(group=self).count()
    user_count.admin_order_field = 'usergroups__count'
    
    def admin_count(self):
        '''Returns the total number of administrators in a group/vikundi'''
        return u'%s' % GroupAdmin.objects.filter(group=self).count()
    admin_count.admin_order_field = 'groupadmin__count'
    
    def msg_count(self):
        '''Returns a link with the total number of messages sent to a group/vikundi'''
        count = PubMessages.objects.filter(channel=self).count()
        if count > 0:
            return u'<a href="/admin/Tangaza/pubmessages/?channel__id=%s">%s</a>' % (self.id, count)
        return count
    
    msg_count.admin_order_field = 'pubmessages__count'
    msg_count.short_description = u'Number of Messages'
    msg_count.allow_tags = True
    
    def __unicode__(self):
        return self.group_name
    
    def activate(self):
        '''You can only send/receive messages if active'''
        self.is_active = 'yes'
        self.save()
        
    def deactivate(self):
        '''You can only send/receive messages if active'''
        self.is_active = 'no'
        self.save()
        
    def get_admin_count (self):
        '''Returns the total number of administrators in a group/vikundi. Deprecated'''
        admins = GroupAdmin.objects.filter (group = self)
        return admins.count()
    
    def get_user_count(self):
        '''Returns the total number of users in a group/vikundi. Deprecated'''
        user_set = UserGroups.objects.filter (group = self)
        return user_set.count()
    
    def is_public(self):
        '''
        Returns True if this is a public group and False otherwise
        '''
        return self.group_type == 'public'
    
    def is_private(self):
        '''
        Returns True if this is a private group and False otherwise
        '''
        return self.group_type == 'private'
    
    def set_quiet(self, user):
        '''Disable updates from this vikundi for this particular user'''
        usr_grp = UserGroups.objects.get(group = self, user = user)
        usr_grp.is_quiet = 'yes'
        usr_grp.save()
        
        #set heard to yes to cancel previous but unheard updates
        subs = SubMessages.objects.filter(dst_user = user, channel = self, heard = 'no')
        for s in subs:
            s.heard = 'yes'
            s.save()
        
        #TODO: Move this to signal?
        action = Actions.objects.get(action_desc = 'quieted group')
        hist = UserGroupHistory(group = self, action = action, user = user)
        hist.save()
        
    def unquiet(self, user):
        '''Enable user to start receiving updates from this group again'''
        usr_grp = UserGroups.objects.get(group = self, user = user)
        usr_grp.is_quiet = 'no'
        usr_grp.save()
        #TODO: move this to signal?
        action = Actions.objects.get(action_desc = 'unquieted group')
        hist = UserGroupHistory(group = self, action = action, user = user)
        hist.save()
        
    @classmethod
    def quiet_all(cls, user):
        '''Disable updates from all vikundi for this particular user'''
        usr_grp_list = UserGroups.objects.filter(user = user)
        for usr_grp in usr_grp_list:
            grp = usr_grp.group
            grp.set_quiet(user)
    
    @classmethod
    def unquiet_all(cls, user):
        '''Enables updates from all vikundi'''
        usr_grp_list = UserGroups.objects.filter(user = user)
        for usr_grp in usr_grp_list:
            grp = usr_grp.group
            grp.unquiet(user)
    
    def add_admin(self, admin_doing_add, admin_being_added):
        '''
        Allows the administrator to add other administrators to this group. Updates ``GroupAdmin`` to reflect this
        '''
        admin = GroupAdmin (user = admin_being_added, group = self)
        admin.save()
        #TODO: move this to signals somehow. How to send user_src to sigmal?
        add_action = Actions.objects.get (action_desc='added admin')
        history = AdminGroupHistory(group = self, action = add_action, user_src = admin_doing_add,
                                    user_dst = admin_being_added)
        history.save()
    
    def delete_admin (self, admin_doing_delete, admin_being_deleted):
        '''
        Deletes an administrator from this group. Updates the ``GroupAdmin`` model to reflect this
        '''
        GroupAdmin.objects.filter (user = self, group = group).delete()
        #TODO: move this to signals somehow. How to send user_src to sigmal?
        action = Actions.objects.get(action_desc = 'deleted admin')
        hist = AdminGroupHistory(group = self, action = action, user_src = admin_doing_delete,
                                 user_dst = admin_being_deleted)
        hist.save()
        
    def add_user (self, admin_doing_add, user_being_added):
        '''
        Adds a new user to this group. Updates the ``UserGroups`` model to reflect this
        '''
        group = UserGroups(user = user_being_added, group = self, is_quiet = 'n')
        group.save()
        #TODO: move this to signals somehow. How to send user_src to sigmal?
        action = Actions.objects.get(action_desc = 'added user')
        admin_hist = AdminGroupHistory(group = self, action = action, user_src = admin_doing_add,
                                       user_dst = user_being_added)
        admin_hist.save()
        
    def delete_user (self, admin_doing_delete, user_being_deleted):
        '''
        Deletes a user from this group. Updates the ``UserGroups`` model to reflect this
        '''
        UserGroups.objects.filter(user=user_being_deleted, group = self).delete()
        #TODO: move this to signals somehow. How to send user_src to sigmal?
        action = Actions.objects.get(action_desc = 'deleted user')
        hist = AdminGroupHistory(group = self, action = action, user_src = admin_doing_delete,
                                 user_dst = user_being_deleted)
        hist.save()
    
    @classmethod
    def resolve(cls, user, name_or_slot):
        '''Resolves the slot number or group name and returns the associated group'''
        # if name_or_slot is None, then resolve to users 'mine' group
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
            grps = Vikundi.objects.filter(group_name = name_or_slot, is_active = 'yes')
            logger.debug ("used: group %s" % grps)
            if len(grps) > 0: group  = grps[0]
            
        return group

    @classmethod
    def is_name_available (cls, name):
        '''
        Returns True if there's no other group with a similar name, and False otherwise
        '''
        grps = cls.objects.filter(group_name = name)
        return len(grps) < 1
    
    @classmethod
    def create (cls, user, group_name, slot, group_type='private', org = None):
        '''Creates a group with group admin and user groups associations and returns the created group'''
        group = Vikundi(group_name = group_name, group_type = group_type, org = org)
        group.save()
        
        grp_admin = GroupAdmin(user = user, group = group)
        grp_admin.save()
        
        usr_grp = UserGroups(group = group, user = user, is_quiet = 'no', slot = slot)
        usr_grp.save()
        
        return group
    
    #Renamed: previously delete
    @classmethod
    def destroy (cls, admin=None, group=None):
        grp = cls.objects.get(group_id = group.group_id)
        grp.is_active = 'no'
        UserGroups.objects.filter (group = group).delete()
        GroupAdmin.objects.filter (group = group).delete()
        Invitations.objects.filter (group = group).delete()
        grp.save()
        
        #TODO: move this to sgnals
        action = Actions.objects.get(action_desc = 'deleted group')
        hist = AdminGroupHistory(group = group, action = action, user_src = admin, user_dst = admin)
        hist.save()
        
    def send_msg (self, user, text, origin):
        '''
        Sends the text message to all members of the group
        Origin is set so that the system knows what sms gateway to use. Default is ke
        '''
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
        '''Checks that the group type the user selected is valid'''
        return dict(GROUP_TYPES).has_key(type_name)

class Countries(models.Model):
    '''
    Keeps a list of countries.
    '''
    country_code = models.IntegerField()
    country_name = models.CharField(max_length=27)
    
    class Meta:
        db_table = u'countries'
        ordering = [u'country_name']
        verbose_name_plural = u'Countries'
        
    @classmethod
    def phone2country(cls, phone):
        #TODO: Fix this to lookup
        return 'kenya'

class Dlr(models.Model):
    '''This should be automatically populated by kannel for each new sms'''
    smsc = models.CharField(max_length=120, blank=True)
    ts = models.CharField(max_length=120, blank=True)
    dest = models.CharField(max_length=120, blank=True)
    src = models.CharField(max_length=120, blank=True)
    service = models.CharField(max_length=120, blank=True)
    url = models.CharField(max_length=765, blank=True)
    mask = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    boxc = models.CharField(max_length=120, blank=True)
    class Meta:
        db_table = u'dlr'

class GroupAdmin(models.Model):
    '''Intermediary table for the administrators of vikundi'''
    user = models.ForeignKey(Watumiaji)
    group = models.ForeignKey(Vikundi)
    
    class Meta:
        db_table = u'group_admin'
        unique_together = ('user', 'group')
        verbose_name_plural = u'Group Leaders'
        verbose_name = u'Group Leader'
        
    def __unicode__(self):
        return self.user.name_text
        #return "Group: %s, Admin: %s" % (self.group.group_name, self.user.name_text)

class Invitations(models.Model):
    '''
    Invitations sent to join a particular group. To be a member of a private group/vikundi
    you have to either be invited or added directly by the system admin of the organization
    '''
    invitation_to = models.ForeignKey(Watumiaji, related_name='invitation_to')
    invitation_from = models.ForeignKey(Watumiaji, related_name='invitation_from')
    group = models.ForeignKey(Vikundi)
    create_stamp = models.DateTimeField(auto_now_add=True)
    completed = models.CharField(max_length=9, choices=YES_NO, default='no')
    class Meta:
        db_table = u'invitations'

 
class PubMessages(models.Model):
    '''
    Each new message sent by a user is a pub message. (See ``SubMessages``)
    '''
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u'Date Sent')
    src_user = models.ForeignKey(Watumiaji, verbose_name = u'Sender')
    channel = models.ForeignKey(Vikundi, db_column='channel', verbose_name=u'Group')
    filename = models.CharField(unique=True, max_length=96, verbose_name=u'Voice Message')
    text = models.CharField(max_length=768, blank=True, verbose_name=u'Text Message')
    class Meta:
        db_table = u'pub_messages'
        verbose_name = u'Messages'
        verbose_name_plural = u'Messages'
        
    def __unicode__(self):
        return self.filename
    
    def play_message(self):
        msg = u'/status/%s.gsm' % self.filename
        
        return u'''<a href="%s" onClick="window.open(this, '_window', 'width=400,height=200,scrollbars=no,status=no,location=no'); return false;">
<img src="/media/speaker-small.png" width="25" height="25" alt="Play" /></a>''' % msg
    
    play_message.allow_tags = True
    
class SubMessages(models.Model):
    '''
    A message associated with a member. A message is sent to a group/vikundi but each member
    of vikundi has to handle it differently
    '''
    message = models.ForeignKey(PubMessages)
    timestamp = models.DateTimeField(auto_now_add=True)
    dst_user = models.ForeignKey(Watumiaji)
    heard = models.CharField(max_length=9, choices=YES_NO, default='no')
    flagged = models.CharField(max_length=9, choices=YES_NO, default='no')
    channel = models.ForeignKey(Vikundi, db_column='channel')
    
    class Meta:
        db_table = u'sub_messages'
        ordering = [u'-timestamp']

class TermsAndPrivacy(models.Model):
    '''Users have to accept the terms and privacy statements before they start using the system'''
    user = models.ForeignKey(Watumiaji)
    accepted = models.CharField(max_length=24, choices=YES_NO, default='no')
    create_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = u'terms_and_privacy'

class UserGroupHistory(models.Model):
    '''Logs all actions performed by a member of a group/vikundi'''
    group = models.ForeignKey(Vikundi)
    action = models.ForeignKey(Actions)
    user = models.ForeignKey(Watumiaji)
    create_stamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = u'user_group_history'

class UserGroups(models.Model):
    '''Intermdiate table that links members to vikundi'''
    user = models.ForeignKey(Watumiaji)
    group = models.ForeignKey(Vikundi)
    is_quiet = models.CharField(max_length=9, choices=YES_NO, default='no', 
                                help_text=u'Would you like to stop receiving updates but still be a member?')
    slot = models.PositiveIntegerField(help_text=u"The number on the phone's keypad that will refer to this group")
    
    class Meta:
        db_table = u'user_groups'
        verbose_name_plural = u"Group Members"
        verbose_name = u'Group Member'
        unique_together = (('user','slot'), ('user','group'),)
    
    def __unicode__(self):
        return "Group: %s, User: %s, Slot: %d" % (self.group.group_name, self.user.name_text, self.slot)

class UserPhones(models.Model):
    '''
    An intermediary table that links a Tangaza member to a phone number
    '''
    country = models.ForeignKey(Countries)
    phone_number = models.CharField(unique=True, max_length=60)
    user = models.ForeignKey(Watumiaji, db_index=True)
    is_primary = models.CharField(max_length=3, choices=YES_NO, default='yes', help_text=u"Is this the main phone number?")
    class Meta:
        db_table = u'user_phones'
        verbose_name = u'User Phone'
        ordering = [u'phone_number']
    
    def __unicode__(self):
        return self.phone_number

class AdminGroupHistory(models.Model):
    '''Logs all actions performed by the administrators of vikundi'''
    group = models.ForeignKey(Vikundi)
    action = models.ForeignKey(Actions, help_text=u'What action did the vikundi administrator perform?')
    user_src = models.ForeignKey(Watumiaji,related_name='user_src', help_text=u'Which vikundi administrator performed this action?')
    user_dst = models.ForeignKey(Watumiaji,related_name='user_dst', help_text=u'Which member was this action directed at?')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = u'admin_group_history'

class Calls(models.Model):
    '''Logs all calls made to the system'''
    user = models.ForeignKey(Watumiaji, help_text=u'Who sent the message?')
    timestamp = models.DateTimeField(auto_now_add=True)
    seconds = models.IntegerField()
    cbstate = models.CharField(max_length=30, help_text=u'Did the member call us at their own cost or did the system call them?')
    class Meta:
        db_table = u'calls'


######################################################
def global_send_sms (dest_phone, text, origin = 'KE'):
    from django.conf import settings
    import urllib
    
    username = settings.SMS_VOICE['SMS_USERNAME_%s' % origin]
    password = settings.SMS_VOICE['SMS_PASSWORD_%s' % origin]
    source = settings.SMS_VOICE['SMS_FROM_%s' % origin]
    sms_url = settings.SMS_VOICE['SMS_URL_%s' % origin]
    
    sent = False
    #logger.debug('gun %s' % {'username':username, 'password':password, 'from':source,
    #                         'to':dest_phone, 'text': text[:160]})
    params = urllib.urlencode ({'username':username, 'password':password, 'from':source,
                                'to':dest_phone})#, 'text': text[:160]})
    params = '%s&text=%s' % (params, urllib.quote(text[:160].encode('UTF8')))
    
    if origin == 'KE':
        params = urllib.urlencode ({'username':username, 'password':password, 'source':source,
                                    'destination':dest_phone})#, 'message': text[:160]})
        params = '%s&message=%s' % (params, urllib.quote(text[:160].encode('UTF8')))
    
    
    
    try:
        resp = urllib.urlopen ("%s?%s" % (sms_url, params))
        logger.debug (resp.read())
        sent = True
    except URLError:
        logger.info ('failed: %s' % sms_url)
        
        return sent

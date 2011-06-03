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

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

from tangaza.Tangaza import grammar
from tangaza.Tangaza import utility

class GroupsCommandsParserTest(TestCase):
    def setUp(self):
        self.lang = utility.LanguageFactory.create_language('eng')
        
    def test_starts_with_at(self):
        '''Tests expressions starting with '@' e.g '@xyz create' '''
        tokens = '@xyz create'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': '', 'group': 'xyz', 'extras': '', 'command': 'create'})
        
    def test_has_group_keyword(self):
        '''Tests existence of 'group' in command 'e.g 'join group xyz' '''
        tokens = 'join group xyz'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': '', 'group': 'xyz', 'extras': '', 'command': 'join'})
        
    def test_has_at_after_command(self):
        '''Tests expressions with '@' e.g 'create @xyz' '''
        tokens = 'create @xyz'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': '', 'group': 'xyz', 'extras': '', 'command': 'create'})
        
    def test_starts_with_groupname(self):
        '''Tests expressions starting with group name '@' e.g 'xyz leave' '''
        tokens = 'xyz leave'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': '', 'group': 'xyz', 'extras': '', 'command': 'leave'})
        
    def test_has_user(self):
        '''Tests expressions that specify user '@' e.g 'delete user_a@xyz' '''
        tokens = 'delete user_a@xyz'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': 'user_a', 'group': 'xyz', 'extras': '', 'command': 'delete'})
        

class UserCommandsParserTest(TestCase):
    def setUp(self):
        self.lang = utility.LanguageFactory.create_language('eng')
        
    def test_starts_with_at(self):
        '''Tests expressions starting with '@' e.g '@xyz remove member_a' '''
        tokens = '@xyz remove member_a'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': 'member_a', 'group': 'xyz', 'extras': '', 'command': 'remove'})
        
    def test_has_group_keyword(self):
        '''Tests existence of 'group' in command 'e.g 'invite group xyz member_a' '''
        tokens = 'invite group xyz member_a'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': 'member_a', 'group': 'xyz', 'extras': '', 'command': 'invite'})
        
    def test_has_at_after_command(self):
        '''Tests expressions with '@' e.g 'invite @xyz member_a' '''
        tokens = 'invite @xyz member_a'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': 'member_a', 'group': 'xyz', 'extras': '', 'command': 'invite'})
        
    def test_starts_with_groupname(self):
        '''Tests expressions starting with group name '@' e.g 'xyz remove member_a' '''
        tokens = 'xyz remove member_a'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': 'member_a', 'group': 'xyz', 'extras': '', 'command': 'remove'})
        
    def test_has_user(self):
        '''Tests expressions that specify user '@' e.g 'remove member_a@xyz' '''
        tokens = 'remove member_a@xyz'.split()
        result = grammar.parse(tokens,self.lang)
        self.assertEqual(result, {'member': 'member_a', 'group': 'xyz', 'extras': '', 'command': 'remove'})
        
    def test_has_from_keyword(self):
        '''Tests expressions that have from keyword e.g. remove member1 from xyz'''
        tokens = 'remove member1 from xyz'.split()
        result = grammar.parse(tokens, self.lang)
        self.assertEqual(result, {'member': 'member1', 'group': 'xyz', 'extras': '', 'command': 'remove'})
        
    def test_has_to_keyword(self):
        '''Tests expressions that have from keyword e.g. invite member1 to xyz'''
        tokens = 'invite member1 to xyz'.split()
        result = grammar.parse(tokens, self.lang)
        self.assertEqual(result, {'member': 'member1', 'group': 'xyz', 'extras': '', 'command': 'invite'})
        
    def test_join_with_username(self):
        '''Tests joining with username provided'''
        tokens = 'join xyz as member1'.split()
        result = grammar.parse(tokens, self.lang)
        self.assertEqual(result, {'member': 'member1', 'group': 'xyz', 'extras': '', 'command': 'join'})


from tangaza.Tangaza.models import *
from tangaza.Tangaza import utility
from django.test.client import Client
from django.core.management import call_command

class SMSTest(TestCase):
    
    fixtures = ['test_admin_info.json', 'test_app_info.json']
    
    def setUp(self):
        self.invalid_member = '222111333'
        self.valid_member = '254777888999'
        self.lang = utility.LanguageFactory.create_language('eng')
        self.member = Watumiaji.objects.get(name_text = 'rodrigo')
        self.c = Client()
        
    def test_create_group(self):
        '''Tests group creation'''
        
        #tests non member trying to create group
        response = self.c.post('/tangaza/', data='create projects',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = self.invalid_member)
        self.assertEqual(response.content, self.lang.not_allowed_to_use_tangaza())
        
        #tests non admin trying to create group
        member = '255777888999'
        response = self.c.post('/tangaza/', data='create projects',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = member)
        self.assertEqual(response.content, self.lang.action_not_allowed())
        
        #tests admin creating group
        response = self.c.post('/tangaza/', data='create projects',
                               content_type='application/x-www-form-urlencoded', 
                               HTTP_X_KANNEL_FROM = self.valid_member)
        self.assertEqual(response.content, self.lang.group_created('projects', 2, 'private'))
        
    def test_join_group(self):
        '''Tests user joining group'''
        member_phone = '255777888999'
        member = Watumiaji.resolve(member_phone)
        admin = Watumiaji.resolve(self.valid_member)
        default_org = UserGroups.objects.filter(user = admin).order_by('pk')[0].group.org
        vikundi = Vikundi.create(admin, 'projects', 6, 'private', default_org)
        admin.invite_user(member, vikundi)
        
        response = self.c.post('/tangaza/', data='join projects',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = member_phone)
        self.assertEqual(response.content, self.lang.joined_group(vikundi, 2))
        
        response = self.c.post('/tangaza/', data='join projects as member1',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = member_phone)
        self.assertEqual(response.content, self.lang.joined_group(vikundi, 2))
    
    def test_delete_group(self):
        '''Tests deleting group'''
        member_phone = '255777888999'
        admin = Watumiaji.resolve(self.valid_member)
        vikundi = Vikundi.resolve(admin, 'nrc')
        
        #tests non-admin trying to delete
        response = self.c.post('/tangaza/', data='delete nrc',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = member_phone)
        self.assertEqual(response.content, self.lang.admin_privileges_required(vikundi))
        
        #tests admin trying to delete
        response = self.c.post('/tangaza/', data='delete nrc',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = self.valid_member)
        self.assertEqual(response.content, self.lang.group_deleted(vikundi))
        
    def test_invite_users(self):
        '''Tests inviting user to group'''
        invitee = '255777888999'
        member = Watumiaji.resolve(invitee)
        admin = Watumiaji.resolve(self.valid_member)
        vikundi = Vikundi.resolve(admin, 'nrc')
        response = self.c.post('/tangaza/', data='invite %s to nrc' % invitee,
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = self.valid_member)
        self.assertEqual(response.content, self.lang.invited_user(invitee, vikundi))
    
    def test_leave_group(self):
        '''Tests leaving group'''
        member_phone = '255777888999'
        member = Watumiaji.resolve(member_phone)
        vikundi = Vikundi.resolve(member, 'nrc')
        
        #tests admin trying to leave
        admin = Watumiaji.resolve(self.valid_member)
        response = self.c.post('/tangaza/', data='leave nrc',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = self.valid_member)
        self.assertEqual(response.content, self.lang.cannot_leave_when_only_admin(vikundi))
        
        #tests non-admin trying to leave
        response = self.c.post('/tangaza/', data='leave nrc',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = member_phone)
        self.assertEqual(response.content, self.lang.user_left_group(vikundi))
        
    def test_remove_user(self):
        '''Tests removing user from group'''
        member_phone = '255777888999'
        member = Watumiaji.resolve(member_phone)
        admin = Watumiaji.resolve(self.valid_member)
        vikundi = Vikundi.resolve(admin, 'nrc')
        
        #tests non-admin trying to remove a user
        response = self.c.post('/tangaza/', data='remove janedoe from nrc',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = member_phone)
        self.assertEqual(response.content, self.lang.admin_privileges_required(vikundi))
        
        #tests admin trying to remove a user
        response = self.c.post('/tangaza/', data='remove smallville from nrc',
                               content_type='application/x-www-form-urlencoded',
                               HTTP_X_KANNEL_FROM = self.valid_member)
        self.assertEqual(response.content, self.lang.deleted_user_from_group(member, vikundi))

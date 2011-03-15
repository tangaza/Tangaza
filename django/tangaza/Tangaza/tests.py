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

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

# Put commands that are called directly from kannel in here.

import re
import logging
import string

from django.http import HttpResponse
from utility import *
from appadmin import *

logger = logging.getLogger(__name__)

############################################################
#@resolve_user
def set_username (request, user, language, username):
	# check if there's another user in the organization with that name
	ug = UserGroups.objects.filter(user = user)
	if len(ug) > 0:
		groups = Vikundi.objects.filter(org = ug[0].group.org)
		
		ug_b = UserGroups.objects.filter(group__in = groups, user__name_text = username)
		
		if len(ug_b) > 0:
			# TODO: algorithm for suggesting alternative username
			return [False, language.username_taken(username)]
	
	user.set_name(username)
	return [True, language.name_set(username)]

#@resolve_user
def quiet_group (request, user, language, name_or_slot):
	group = Vikundi.resolve(user, name_or_slot)
	
	if group == None:
		return [False, language.unknown_group(name_or_slot)]
	
	if not user.is_member(group):
		return [False, language.user_not_in_group(user, group)]
	
	group.set_quiet(user)
	
	logger.info ("user %s group %s" % (user, group))
	
	return [True, language.group_quieted(group)]

#@resolve_user
def unquiet_group (request, user, language, name_or_slot):
	group = Vikundi.resolve(user, name_or_slot)
	
	if group == None:
		return [False, language.unknown_group(name_or_slot)]
	
	if not user.is_member(group):
		return [False, language.user_not_in_group(user, group)]

	group.unquiet(user)

	logger.info ("user %s group %s" % (user, group))

	return [True, language.group_unquieted(group)]

#@resolve_user
def quiet_or_unquiet_all_groups (request, user, language):
	logger.info ("user %s" % user)
	return [True, "not implemented"]

#@resolve_user
def quiet_all (request, user, language):
	Groups.quiet_all(user)
	return [True, language.quieted_all_groups()]

#@resolve_user
def unquiet_all (request, user, language):
	Groups.unquiet_all(user)
	return [True, language.unquieted_all_groups()]



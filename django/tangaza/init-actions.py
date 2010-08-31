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

import tangaza.sms.models as base

actions = ['created_group', 'deleted_user', 'deleted_admin',
           'deleted_group', 'banned_user', 'joined_group',
           'left_group', 'activated', 'deactivated',
           'created_user', 'invited_user']

for action in actions:
    a = base.Actions(action_desc=action)
    a.save()

#+-----------+-------------+
#| action_id | action_desc |
#+-----------+-------------+
#|         1 | created_group     |
#|         2 | deleted_user     |
#|         3 | deleted_admin     |
#|         4 | deleted_group     |
#|         5 | banned_user      |
#|         6 | joined_group      |
#|         7 | left_group        |
#|         8 | activated   |
#|         9 | deactivated |
#|        10 | created_user     |
#|        11 | invited_user     |
#+-----------+-------------+

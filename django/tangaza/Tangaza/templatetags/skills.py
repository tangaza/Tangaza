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

from django import template
from tangaza.Tangaza.models import *
from tangaza.Tangaza.forms import *

logger = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag('skills.html')
def show_results(change_list):
    logger.debug('stupid %s' % change_list.list_display)
    if change_list.result_list.count() > 0:
        org = change_list.result_list[0].org
        admins = GroupAdmin.objects.filter(group__org = org).order_by('user')
        unique_admins = []
        users = []
        for admin in admins:
            if admin.user not in users:
                unique_admins.append(admin)
                users.append(admin.user)
        
        return { 'admins': unique_admins }
    return {'admins':[]}

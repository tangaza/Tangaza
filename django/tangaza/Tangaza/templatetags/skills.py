
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

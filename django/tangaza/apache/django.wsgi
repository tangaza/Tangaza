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


import os
import sys

DJANGO_PATH = sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
if DJANGO_PATH not in sys.path:
   sys.path.append(DJANGO_PATH)
   sys.path.append(DJANGO_PATH + '/sms')

os.environ['DJANGO_SETTINGS_MODULE'] = 'tangaza.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

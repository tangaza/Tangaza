#! /bin/bash
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


# add the current directory and the parent directory to PYTHONPATH
# sets DJANGO_SETTINGS_MODULE

set -e

export PYTHONPATH=$PYTHONPATH:$PWD/..
export PYTHONPATH=$PYTHONPATH:$PWD
if [ -z "$1" ]; then
    x=${PWD/\/[^\/]*\/}
    export DJANGO_SETTINGS_MODULE=$x.settings
else
    export DJANGO_SETTINGS_MODULE=$1
fi

echo "DJANGO_SETTINGS_MODULE set to $DJANGO_SETTINGS_MODULE"



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
#    Author: Billy Odero
#

set -e

TANGAZA_SCRIPTS=$HOME/git/Tangaza
COMMON_SCRIPTS=$HOME/git/Common

if [ -d "/var/lib/tomcat6/webapps/ROOT/jobs" ]; then
    BUILD_BOT_HOME=/var/lib/tomcat6/webapps/ROOT/jobs
    TANGAZA_SCRIPTS=$BUILD_BOT_HOME/Tangaza/workspace
    COMMON_SCRIPTS=$BUILD_BOT_HOME/Common/workspace
fi

DEB_PATH=$TANGAZA_SCRIPTS/deb-builder/install

if [ `id -u` != 0 ]; then
    echo "You have to run the install script as root."
    exit 1
fi

#check if tangaza_1.0-1_all.deb is in the same directory
if [ ! -f "$DEB_PATH/tangaza_1.0-1_all.deb" ]; then
    echo "tangaza_1.0-1_all.deb could not be found. Installation will stop."
    #echo "Make sure install.sh and tangaza_1.0-1_all.deb are the same directory."
    exit 1
fi

echo "Initializing install process..."
#check if it has been added to sources.list and add
dpkg-scanpackages ./ /dev/null |gzip -c -9 > Packages.gz

VAR=`grep -i "^deb file://$DEB_PATH" /etc/apt/sources.list`

if [ ! -n "$VAR" ]; then
    SOURCES_CHANGED=1
    echo "Updating sources.list"
    cp /etc/apt/sources.list /etc/apt/sources.list.bak
    echo "deb file://$DEB_PATH /" >> /etc/apt/sources.list
fi

echo -n "Would you like apt-get to update [RECOMMENDED]. (If you dont know just press enter.) [Y/n]:"
read -n 1 update
echo ""

if [ "$update" != "n" ]; then
    aptitude update
fi

echo "Beginning install..."
aptitude install tangaza

#restore sources.list
if [ -n $SOURCES_CHANGED ]; then
    echo "Restoring sources.list"
    mv /etc/apt/sources.list.bak /etc/apt/sources.list
fi

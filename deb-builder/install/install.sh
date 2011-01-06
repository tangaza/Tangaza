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
#    Authors: Billy Odero
#

if [ `id -u` != 0 ]; then
    echo "You have to run the install script as root."
    exit 1
fi

#check if tangaza-1.0.deb is in the same directory
if [ ! -f "tangaza-1.0.deb" ]; then
    echo "tangaza-1.0.deb could not be found. Installation will stop."
    echo "Make sure install.sh and tangaza-1.0.deb are the same directory."
    exit 1
fi

echo "Initializing install process..."
#check if it has been added to sources.list and add
dpkg-scanpackages ./ /dev/null |gzip -c -9 > Packages.gz

VAR=`grep -i "^deb file://$PWD" /etc/apt/sources.list`

if [ ! -n "$VAR" ]; then
    SOURCES_CHANGED=1
    echo "Updating sources.list"
    cp /etc/apt/sources.list /etc/apt/sources.list.bak
    echo "deb file://$PWD /" >> /etc/apt/sources.list
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

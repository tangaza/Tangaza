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

TANGAZA_SCRIPTS=$HOME/git/Tangaza
COMMON_SCRIPTS=$HOME/git/Common
INST_LOCATION=./tangaza/usr/local/lib/tangaza

echo "Exporting Tangaza files"
cp -r $TANGAZA_SCRIPTS/* $INST_LOCATION/
rm -rf $INST_LOCATION/.git

cp -r $COMMON_SCRIPTS $INST_LOCATION/agi-bin/Nokia/
rm -rf $INST_LOCATION/agi-bin/Nokia/Common/.git

echo "Copying startup script"
#cp $TANGAZA_SCRIPTS/../daemon/tangaza ./tangaza/etc/init.d/

echo "Copying sound files"
if [ ! -d "$INST_LOCATION/../sounds/tangaza/english" ]; then
    #cp -r $TANGAZA_SCRIPTS../sounds/tangaza/english $INST_LOCATION/../sounds/tangaza/
    #cp -r $TANGAZA_SCRIPTS../sounds/tangaza/swahili $INST_LOCATION/../sounds/tangaza/
    echo ""
fi

echo "Building deb package"
dpkg-deb --build tangaza/ tangaza-1.0.deb

mv tangaza-1.0.deb install/
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
#

set -e

TANGAZA_HOME=/usr/lib/tangaza
CONF_PATH=/etc/tangaza/settings.conf
DB_HOST=`awk -F'=' '/^DB_HOST/ {print $2}'  $CONF_PATH`
DB_USER=`awk -F'=' '/^DB_USER/ {print $2}'  $CONF_PATH`
DB_PASS=`awk -F'=' '/^DB_PASS/ {print $2}'  $CONF_PATH`
DB_NAME=`awk -F'=' '/^DB_NAME/ {print $2}'  $CONF_PATH`

MYSQL="mysql -h $DB_HOST -u $DB_USER -p$DB_PASS -D $DB_NAME"
$MYSQL -BNe "show tables" | awk '{print "set foreign_key_checks=0; drop table `" $1 "`;"}' | $MYSQL

cat tangaza-schema.sql | $MYSQL

MYSQLIMPORT="mysqlimport -h $DB_HOST -p$DB_PASS -u $DB_USER --delete --local tangaza "
$MYSQLIMPORT actions.dat
$MYSQLIMPORT countries.dat 
$MYSQLIMPORT languages.dat


unset DB_HOST
unset DB_USER
unset DB_PASS
unset DB_NAME
unset MYSQL

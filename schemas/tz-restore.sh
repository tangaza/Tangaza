#! /bin/sh

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


HOST=""
USER=""
PASS=""
DB="tangaza"

MYSQL="mysql -h $HOST -u $USER -p$PASS -D $DB"
$MYSQL -BNe "show tables" | awk '{print "set foreign_key_checks=0; drop table `" $1 "`;"}' | $MYSQL

cat tangaza-schema.sql | $MYSQL

MYSQLIMPORT="mysqlimport -h $HOST -p$PASS -u $USER --delete --local tangaza "
$MYSQLIMPORT actions.dat
$MYSQLIMPORT countries.dat 
$MYSQLIMPORT languages.dat


unset HOST
unset USER
unset PASS
unset DB
unset MYSQL


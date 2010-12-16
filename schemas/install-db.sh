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

####################################################
#
# This is used to create original database during 
# setup i.e. if the database did not exist already
# tz-restore.sh simply creates the original tables
#
####################################################

# Get connection details from config file
# use that to create DB. User can change this later

TANGAZA_HOME=/usr/local/lib/tangaza
CONF_PATH=$TANGAZA_HOME/conf/settings.conf
DB_HOST=`awk -F'=' '/^DB_HOST/ {print $2}'  $CONF_PATH`
DB_USER=`awk -F'=' '/^DB_USER/ {print $2}'  $CONF_PATH`
DB_PASS=`awk -F'=' '/^DB_PASS/ {print $2}'  $CONF_PATH`
DB_NAME=`awk -F'=' '/^DB_NAME/ {print $2}'  $CONF_PATH`

Q1="create database if not exists $DB_NAME;"
Q2="create user '$DB_USER'@'$DB_HOST' identified by '$DB_PASS';"
Q3="grant all privileges on $DB_NAME.* to '$DB_USER'@'$DB_HOST' with grant option;"

echo "Checking if $DB_USER already exists. Waiting for the database root password"
SQLUSER=`mysql -u root -p -D mysql -e "select user, host from mysql.user where user='$DB_USER' and host='$DB_HOST'"`

if [ -n "$SQLUSER" ]; then
    # if user already exists dont try to recreate
    echo "$DB_USER already exists in mysql and will not be created."
    Q2=""; Q3=""
fi

echo "All checks complete. Database creation commencing. Waiting for the database root password"
mysql -u root -p -D mysql -e "$Q1 $Q2 $Q3"

CWD=$PWD
echo "Switching working dir /usr/local/lib/tangaza/schemas/"

cd $TANGAZA_HOME/schemas/
./tz-restore.sh

echo "Switching back Working dir $CWD"
cd $CWD

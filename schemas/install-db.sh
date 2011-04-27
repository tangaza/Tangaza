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

set -e

TANGAZA_HOME=/usr/lib/tangaza
CONF_PATH=/etc/tangaza/settings.conf
DB_HOST=`awk -F'=' '/^DB_HOST/ {print $2}'  $CONF_PATH`
DB_USER=`awk -F'=' '/^DB_USER/ {print $2}'  $CONF_PATH`
DB_PASS=`awk -F'=' '/^DB_PASS/ {print $2}'  $CONF_PATH`
DB_NAME=`awk -F'=' '/^DB_NAME/ {print $2}'  $CONF_PATH`

Q1="create database if not exists $DB_NAME;"
Q3="ALTER DATABASE $DB_NAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
Q3="INSERT INTO mysql.user 
    (host, user, password, select_priv, insert_priv, 
     update_priv, delete_priv, create_priv, alter_priv,
     index_priv, references_priv, drop_priv, 
     ssl_cipher, x509_issuer, x509_subject) 
VALUES 
    -- check user table for the actual values used in 
    -- ssl_cipher, x509_issuer, and x509_subject columns
    ('$DB_HOST','$DB_USER',PASSWORD('$DB_PASS'),
     'Y','Y','Y','Y','Y','Y','Y','Y','N','','','') 
ON DUPLICATE KEY UPDATE 
    password=PASSWORD('$DB_PASS'), select_priv='Y', 
    insert_priv='Y', update_priv='Y', delete_priv='Y', create_priv='Y', 
    alter_priv='Y', index_priv='Y', references_priv='Y',
    drop_priv='N',ssl_cipher='', x509_issuer='', x509_subject='';
FLUSH PRIVILEGES;"

echo "We will now check if the database and user exists and create them if not there. Waiting for the MySQL root password"
mysql -u root -p -D mysql -e "$Q1 $Q2 $Q3"

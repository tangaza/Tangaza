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


-- Script for restoring the tangaza db

--
-- Table structure for table `actions`
--

DROP TABLE IF EXISTS `actions`;
CREATE TABLE `actions` (
  `action_id` int(10) unsigned NOT NULL auto_increment,
  `action_desc` varchar(90) NOT NULL,
  PRIMARY KEY  (`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `sms_log`
--

DROP TABLE IF EXISTS `sms_log`;
CREATE TABLE `sms_log` (
  `sms_id` int(10) unsigned NOT NULL auto_increment,
  `sender` varchar(20) NOT NULL,
  `text` varchar(200) default NULL,
  PRIMARY KEY  (`sms_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `group_id` int(10) unsigned NOT NULL auto_increment,
  `group_name` varchar(60) NOT NULL,
  `group_type` enum('mine', 'private', 'public') NOT NULL default 'public',
  `is_active` enum('yes') NULL,
  PRIMARY KEY  (`group_id`),
  UNIQUE KEY `group_name` (`group_name`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_4de83ca7792de1` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add actions',9,'add_actions'),(26,'Can change actions',9,'change_actions'),(27,'Can delete actions',9,'delete_actions'),(28,'Can add groups',10,'add_groups'),(29,'Can change groups',10,'change_groups'),(30,'Can delete groups',10,'delete_groups'),(31,'Can add users',11,'add_users'),(32,'Can change users',11,'change_users'),(33,'Can delete users',11,'delete_users'),(34,'Can add admin group history',12,'add_admingrouphistory'),(35,'Can change admin group history',12,'change_admingrouphistory'),(36,'Can delete admin group history',12,'delete_admingrouphistory'),(37,'Can add countries',13,'add_countries'),(38,'Can change countries',13,'change_countries'),(39,'Can delete countries',13,'delete_countries'),(40,'Can add group admin',14,'add_groupadmin'),(41,'Can change group admin',14,'change_groupadmin'),(42,'Can delete group admin',14,'delete_groupadmin'),(43,'Can add invitations',15,'add_invitations'),(44,'Can change invitations',15,'change_invitations'),(45,'Can delete invitations',15,'delete_invitations'),(46,'Can add sms rawmessage',16,'add_smsrawmessage'),(47,'Can change sms rawmessage',16,'change_smsrawmessage'),(48,'Can delete sms rawmessage',16,'delete_smsrawmessage'),(49,'Can add user group history',17,'add_usergrouphistory'),(50,'Can change user group history',17,'change_usergrouphistory'),(51,'Can delete user group history',17,'delete_usergrouphistory'),(52,'Can add user groups',18,'add_usergroups'),(53,'Can change user groups',18,'change_usergroups'),(54,'Can delete user groups',18,'delete_usergroups'),(55,'Can add user phones',19,'add_userphones'),(56,'Can change user phones',19,'change_userphones'),(57,'Can delete user phones',19,'delete_userphones'),(58,'Can add pub messages',20,'add_pubmessages'),(59,'Can change pub messages',20,'change_pubmessages'),(60,'Can delete pub messages',20,'delete_pubmessages'),(61,'Can add sub messages',21,'add_submessages'),(62,'Can change sub messages',21,'change_submessages'),(63,'Can delete sub messages',21,'delete_submessages');

/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_321a8efef0ee9890` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_6d7fb3c2067e79cb` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
CREATE TABLE `countries` (
  `country_id` int(10) unsigned NOT NULL auto_increment,
  `country_code` smallint(6) NOT NULL,
  `country_name` varchar(9) NOT NULL,
  PRIMARY KEY  (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(9,'actions','sms','actions'),(10,'groups','sms','groups'),(11,'users','sms','users'),(12,'admin group history','sms','admingrouphistory'),(13,'countries','sms','countries'),(14,'group admin','sms','groupadmin'),(15,'invitations','sms','invitations'),(16,'sms rawmessage','sms','smsrawmessage'),(17,'user group history','sms','usergrouphistory'),(18,'user groups','sms','usergroups'),(19,'user phones','sms','userphones');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dlr`
--

DROP TABLE IF EXISTS `dlr`;
CREATE TABLE `dlr` (
  `dlr_id` int(10) unsigned NOT NULL auto_increment,
  `smsc` varchar(40) default NULL,
  `ts` varchar(40) default NULL,
  `dest` varchar(40) default NULL,
  `src` varchar(40) default NULL,
  `service` varchar(40) default NULL,
  `url` varchar(255) default NULL,
  `mask` int(10) default NULL,
  `status` int(10) default NULL,
  `boxc` varchar(40) default NULL,
  PRIMARY KEY  (`dlr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `languages`
--

DROP TABLE IF EXISTS `languages`;
CREATE TABLE `languages` (
  `language_id` tinyint(3) unsigned NOT NULL auto_increment,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY  (`language_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `sms_rawmessage`
--

DROP TABLE IF EXISTS `sms_rawmessage`;
CREATE TABLE `sms_rawmessage` (
  `id` int(11) NOT NULL auto_increment,
  `phone` varchar(120) NOT NULL,
  `timestamp` date NOT NULL,
  `text` varchar(1536) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(10) unsigned NOT NULL auto_increment,
  `user_pin` varchar(6) default NULL,
  `status` enum('good','bad','blacklisted') NOT NULL default 'good',
  `place_id` int(10) unsigned NOT NULL default '1',
  `level` enum('basic','advanced','expert') NOT NULL default 'advanced',
  `callback_limit` int(10) unsigned NOT NULL default '60',
  `invitations_remaining` int(10) unsigned NOT NULL default '100',
  `language_id` tinyint(3) unsigned NOT NULL default '1',
  `name_file` varchar(32) default NULL,
  `name_text` varchar(128) default NULL,
  `create_stamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `modify_stamp` timestamp NOT NULL default '0000-00-00 00:00:00',
  `notify_stamp` timestamp NOT NULL default '0000-00-00 00:00:00',
  `notify_period` time NOT NULL default '24:00:00',
  `dirty` enum('no','yes') NOT NULL default 'no',
  `notify_status` enum('off','on') NOT NULL default 'on',
  `accepted_terms` enum('yes','no') NOT NULL default 'no',
  `dirty_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  `notify_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  `calling_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`user_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`language_id`) REFERENCES `languages` (`language_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `calls`
--

DROP TABLE IF EXISTS `calls`;
CREATE TABLE `calls` (
  `call_id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `seconds` int(10) unsigned NOT NULL,
  `cbstate` enum('calledback','calledus') NOT NULL,
  PRIMARY KEY  (`call_id`),
  KEY `user_id` (`user_id`),
  KEY `timestamp` (`timestamp`),
  KEY `cbstate` (`cbstate`),
  CONSTRAINT `calls_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `group_admin`
--

DROP TABLE IF EXISTS `group_admin`;
CREATE TABLE `group_admin` (
  `group_admin_id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `group_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`group_admin_id`),
  KEY `user_id` (`user_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `group_admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `group_admin_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `invitations`
--

DROP TABLE IF EXISTS `invitations`;
CREATE TABLE `invitations` (
  `invitation_id` int(10) unsigned NOT NULL auto_increment,
  `invitation_to_id` int(10) unsigned NOT NULL,
  `invitation_from_id` int(10) unsigned NOT NULL,
  `group_id` int(10) unsigned NOT NULL,
  `create_stamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `completed` enum('yes','no') NOT NULL default 'no',
  PRIMARY KEY  (`invitation_id`),
  KEY `invitation_to_id` (`invitation_to_id`),
  KEY `invitation_from_id` (`invitation_from_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `invitations_ibfk_1` FOREIGN KEY (`invitation_to_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `invitations_ibfk_2` FOREIGN KEY (`invitation_from_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `invitations_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `pub_messages`
--

DROP TABLE IF EXISTS `pub_messages`;
CREATE TABLE `pub_messages` (
  `pub_id` int(10) unsigned NOT NULL auto_increment,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `src_user_id` int(10) unsigned NOT NULL,
  `channel` int(10) unsigned NOT NULL,
  `filename` varchar(32) NOT NULL,
  `text` varchar(256) default NULL,
  PRIMARY KEY  (`pub_id`),
  UNIQUE KEY `filename` (`filename`),
  KEY `src_user_id` (`src_user_id`),
  KEY `timestamp` (`timestamp`),
  KEY `channel` (`channel`),
  CONSTRAINT `pub_messages_ibfk_1` FOREIGN KEY (`src_user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `pub_messages_ibfk_2` FOREIGN KEY (`channel`) REFERENCES `groups` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `sub_messages`
--

DROP TABLE IF EXISTS `sub_messages`;
CREATE TABLE `sub_messages` (
  `sub_id` int(10) unsigned NOT NULL auto_increment,
  `message_id` int(10) unsigned NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `dst_user_id` int(10) unsigned NOT NULL,
  `heard` enum('no','yes') NOT NULL default 'no',
  `flagged` enum('no','yes') NOT NULL default 'no',
  `channel` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`sub_id`),
  KEY `dst_user_id` (`dst_user_id`),
  KEY `message_id` (`message_id`),
  KEY `heard` (`heard`),
  KEY `flagged` (`flagged`),
  KEY `timestamp` (`timestamp`),
  KEY `channel` (`channel`),
  CONSTRAINT `sub_messages_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `pub_messages` (`pub_id`),
  CONSTRAINT `sub_messages_ibfk_2` FOREIGN KEY (`dst_user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `sub_messages_ibfk_3` FOREIGN KEY (`channel`) REFERENCES `groups` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `terms_and_privacy`
--

DROP TABLE IF EXISTS `terms_and_privacy`;
CREATE TABLE `terms_and_privacy` (
  `user_id` int(10) unsigned NOT NULL,
  `status` enum('accepted','rejected') NOT NULL,
  `create_stamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  KEY `user_id` (`user_id`),
  CONSTRAINT `terms_and_privacy_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `user_group_history`
--

DROP TABLE IF EXISTS `user_group_history`;
CREATE TABLE `user_group_history` (
  `user_group_hist_id` int(10) unsigned NOT NULL auto_increment,
  `group_id` int(10) unsigned NOT NULL,
  `action_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `create_stamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`user_group_hist_id`),
  KEY `group_id` (`group_id`),
  KEY `action_id` (`action_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_group_history_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `user_group_history_ibfk_2` FOREIGN KEY (`action_id`) REFERENCES `actions` (`action_id`),
  CONSTRAINT `user_group_history_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
CREATE TABLE `user_groups` (
  `user_group_id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `group_id` int(10) unsigned NOT NULL,
  `is_quiet` enum('yes','no') NOT NULL default 'no',
  `slot` smallint(6) NOT NULL,
  PRIMARY KEY  (`user_group_id`),
  KEY `group_id` (`group_id`),
  KEY `user_groups_ibfk_1` (`user_id`),
  CONSTRAINT `user_groups_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `user_groups_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `user_phones`
--

DROP TABLE IF EXISTS `user_phones`;
CREATE TABLE `user_phones` (
  `phone_id` int(10) unsigned NOT NULL auto_increment,
  `country_id` int(10) unsigned NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_primary` enum('yes','no') NOT NULL default 'no',
  PRIMARY KEY  (`phone_id`),
  UNIQUE KEY `phone_number` (`phone_number`),
  KEY `country_id` (`country_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_phones_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`),
  CONSTRAINT `user_phones_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `admin_group_history`
--

DROP TABLE IF EXISTS `admin_group_history`;
CREATE TABLE `admin_group_history` (
  `admin_group_hist_id` int(10) unsigned NOT NULL auto_increment,
  `group_id` int(10) unsigned NOT NULL,
  `action_id` int(10) unsigned NOT NULL,
  `user_src_id` int(10) unsigned NOT NULL,
  `user_dst_id` int(10) unsigned NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`admin_group_hist_id`),
  KEY `group_id` (`group_id`),
  KEY `action_id` (`action_id`),
  KEY `user_src_id` (`user_src_id`),
  KEY `user_dst_id` (`user_dst_id`),
  CONSTRAINT `admin_group_history_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `admin_group_history_ibfk_2` FOREIGN KEY (`action_id`) REFERENCES `actions` (`action_id`),
  CONSTRAINT `admin_group_history_ibfk_3` FOREIGN KEY (`user_src_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `admin_group_history_ibfk_4` FOREIGN KEY (`user_dst_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  UNIQUE KEY `name_text` (`name_text`),
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
  `member_profile_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `member_profile_id` (`member_profile_id`),
  CONSTRAINT `auth_user_ibfk_1` FOREIGN KEY (`member_profile_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
CREATE TABLE `organization` (
  `org_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `org_name` varchar(90) NOT NULL,
  `org_admin_id` int(11) NOT NULL,
  `is_active` enum('yes') NULL,
  PRIMARY KEY (`org_id`),
  KEY `org_admin_id` (`org_admin_id`),
  CONSTRAINT `organization_ibfk_1` FOREIGN KEY (`org_admin_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `group_id` int(10) unsigned NOT NULL auto_increment,
  `group_name` varchar(60) NOT NULL,
  `group_name_file` varchar(32) NULL,
  `group_type` enum('mine', 'private', 'public') NOT NULL default 'private',
  `is_active` enum('yes') NULL,
  `is_deleted` enum('yes') NULL,
  `org_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`group_id`),
  UNIQUE KEY `group_name` (`group_name`, `is_deleted`),
  KEY `org_id` (`org_id`),
  CONSTRAINT `groups_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organization` (`org_id`)
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
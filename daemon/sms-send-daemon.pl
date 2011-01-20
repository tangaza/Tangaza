#!/usr/bin/perl
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

# TODO: 
# ****
# 1. Insert missing values indicated by ? below.

use Nokia::Common::SMSQueue;
use Nokia::Common::Tools;

die if (!defined($ENV{"NASI_CONFIG"}));

my $prefs = &read_config(undef, $ENV{"NASI_CONFIG"});
my $tmp_dir = $prefs->{paths}->{NASI_TMP};

my $server = Nokia::Common::SMSQueue->new
    ({port            => 9275,
      log_level       => 4,
      cidr_allow      => '127.0.0.0/8',
      ext_ke          => '?',    # Country code
      callout_ext_ke  => '?',    # Dialing out extension, or phone number
      sms_number_ke   => '?',    # Phone number of your SMS gateway
      sms_url_ke      => '?',  # URL that the SMS gateway uses to send out messages
      sms_username_ke => '?',  # Username for SMS gateway
      sms_password_ke => '?',  # Password for SMS gateway
      log_file => $prefs->{paths}->{NASI_LOG}.'/log/sms-send-daemon.log',
     });

$server->run;


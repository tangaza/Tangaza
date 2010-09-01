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

package Nokia::Tangaza::Network;

use Exporter;
@ISA = ('Exporter');
@EXPORT = ('get_friend_count_on_network', 'get_total_friend_count',
	   'get_msg_count_on_network', 'set_dirty_bit',
	   'set_dirty_bit_if_new_msgs', 'get_friends_on_network');

use strict;
use DBI;
use Nokia::Common::Sound;
use Nokia::Common::Tools;
use Nokia::Common::Phone;
use Nokia::Tangaza::Invitations;

######################################################################

sub get_friend_count_on_network {
    my ($self,$network) = @_;
	
    # Caveat: assumes that if its an array,
    # we want count of all networks.
	
    # This is because UI only permits selection of one particular
    # network or all of them.
	
    #0 means send to all
    $self->{server}{get_network_friend_count_sth} =
	$self->{server}{dbi}->prepare_cached
	("SELECT count(*) as friend_count from user_groups where ".
	 "is_quiet = 'no' and group_id = ? and user_id != ?");
    $self->{server}{get_network_friend_count_sth}->execute
	($network, $self->{user}->{id});
    
    my ($friend_count) = 
		$self->{server}{get_network_friend_count_sth}->fetchrow_array();
    $self->{server}{get_network_friend_count_sth}->finish();

    return $friend_count;

}

######################################################################
# returns total number of connections

sub get_total_friend_count {
    my ($self,$network) = @_;

    $self->{server}{get_network_total_friend_count_sth} =
	$self->{server}{dbi}->prepare_cached
	("SELECT count(*) as friend_count from user_groups where ".
	 "is_quiet = 'no' and user_id = ? and slot >= 0 and slot <= 9");
    $self->{server}{get_network_total_friend_count_sth}->execute ($self->{user}->{id});
    
    my ($friend_count) = 
		$self->{server}{get_network_total_friend_count_sth}->fetchrow_array();
    $self->{server}{get_network_total_friend_count_sth}->finish();

    # deduct 1 for ourselves
    $friend_count--;

    return $friend_count;

}


######################################################################
# returns reference to friends tuples

sub get_friends_on_network {
    my ($self,$channels) = @_;

    my $select = 
	"SELECT user_id from user_groups where ".
	"is_quiet='no' and group_id = ? and user_id != ?;";
    
    $self->log (4, "get_friends_on_network running select $select");
    $self->log(4, "SELECT user_id from user_groups where ".
	       "is_quiet='no' and group_id =$channels and user_id != $self->{user}->{id};");

    $self->{server}{select_friends_new_msg_sth} =
	$self->{server}{dbi}->prepare_cached ($select);

    $self->{server}{select_friends_new_msg_sth}->execute
		($channels, $self->{user}->{id});

    my $friend_tuples = undef;
    if ($self->{server}{select_friends_new_msg_sth}->rows > 0) {
	$friend_tuples =
	    $self->{server}{select_friends_new_msg_sth}->fetchall_arrayref
	    ({ user_id => 1});
    }

    $self->{server}{select_friends_new_msg_sth}->finish();
    return $friend_tuples;
}

######################################################################

sub get_msg_count_on_network {
    my ($self,$user_id,$new_only,$network, $flagged) = @_;
    
    # Caveat: assumes that if its an array,
    # we want count of all networks.

    # This is because UI only permits selection of one particular
    # network or all of them.
    if (!defined($flagged)) {
		$flagged = "";
    }
    else {
		$flagged = " AND flagged = '$flagged'";
    }
    my $select = "SELECT count(*) as msg_count from sub_messages".
		" where dst_user_id=? $flagged ";

    if ($new_only) {
		$select .= " AND heard='no'";
    }

    if (!defined($network) || ref($network) eq "ARRAY") {
		$self->{server}{get_msg_count_on_sth} =
		    $self->{server}{dbi}->prepare_cached ($select);
		$self->{server}{get_msg_count_on_sth}->execute
		    ($user_id);
		
    }
    else {
		
		$select .= " AND channel=?";
		
		$self->{server}{get_msg_count_on_sth} =
		    $self->{server}{dbi}->prepare_cached ($select);
		$self->{server}{get_msg_count_on_sth}->execute
		    ($user_id, $network);
    }

    my ($msg_count) = 
		$self->{server}{get_msg_count_on_sth}->fetchrow_array();
		
    $self->{server}{get_msg_count_on_sth}->finish();

    $self->log (4, "count $msg_count select $select");

    return $msg_count;

}

######################################################################
sub set_dirty_bit {
    my ($self,$user_id,$dirty) = @_;

    if ($dirty) {
		$self->{server}{set_dirty_bit_sth} =
		    $self->{server}{dbi}->prepare_cached
		    ("UPDATE users set dirty_time = NOW() where user_id=?");
    }
    else {
		#TODO Not sure if this is a nice way to approach it even if it solves it
		$self->{server}{set_dirty_bit_sth} =
		    $self->{server}{dbi}->prepare_cached
		    ("UPDATE users set calling_time = NOW() where user_id=?");
    }

    $self->{server}{set_dirty_bit_sth}->execute ($user_id);
    $self->{server}{set_dirty_bit_sth}->finish ();

}

######################################################################
sub set_dirty_bit_if_new_msgs {
    my ($self,$user_id) = @_;

    if (&get_msg_count_on_network ($self, $user_id, 1) > 0) {
		&set_dirty_bit ($self, $user_id, 1);
    }
}

######################################################################

1;

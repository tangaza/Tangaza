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
	   'get_msg_count_on_network', 'set_dirty_bit', 'select_network_menu',
	   'set_dirty_bit_if_new_msgs', 'get_friends_on_network');

use strict;
use DBI;
use Nokia::Common::Sound;
use Nokia::Common::Tools;
use Nokia::Common::Phone;
#use Nokia::Tangaza::Invitations;

######################################################################
sub select_network_menu {
    my ($self,$prompt,$can_select_all) = @_;

    $self->log (4, "start select_network_menu");

    my $digits = "0123456789";
    if ($can_select_all == 1) {
	$digits = "0123456789";
    }

    my $network_code = &get_unchecked_small_number
        ($self, $prompt, $digits);

    $self->log (4, "received network_code $network_code");

    if ($network_code eq 'timeout' ||
                $network_code eq 'hangup' ||
	$network_code eq 'cancel') {
	return $network_code;
    }

    $self->log (4, "end select_network_menu");

    #return the group_id based on the selected slot                                                                                            
    my $group_rs = $self->{server}{schema}->resultset('UserGroups')->search
        ({user_id => $self->{user}->{id}, slot => $network_code},
         {select => [qw/group_id/]});

    my $group = $group_rs->next;
    my $group_id = $group->group_id->id if (defined($group));
    $self->log(4, "Selected group: ".$group_id);
    return $group_id;

}


######################################################################

sub get_friend_count_on_network {
    my ($self,$network) = @_;
    
    my $friend_rs = $self->{server}{schema}->resultset('UserGroups')->search
	({is_quiet => 'no', group_id => $network, user_id => {'!=' => $self->{user}->{id}}});
    
    return ($friend_rs->count);

}

######################################################################
# returns total number of connections

sub get_total_friend_count {
    my ($self) = @_;
    
    #return member count on all vikundi that i am part of and that are active and not quiet
    my @vikundi = $self->{server}{schema}->resultset('UserGroups')->search
	({ 'group_id.is_active' => 'yes', user_id => $self->{user}->{id}, is_quiet => 'no'},
	 { join => 'group_id' , #this is a join to vikundi
	   select => qw/group_id/ });
    
    my $friend_rs = $self->{server}{schema}->resultset('UserGroups')->search
        ({ group_id => {'IN' => \@vikundi} });
    
    # -1 to exclude the caller
    return ($friend_rs->count) - 1;
}


######################################################################
# returns reference to friends tuples

sub get_friends_on_network {
    my ($self,$channels) = @_;

    my @friends = $self->{server}{schema}->resultset('UserGroups')->search
        ({is_quiet => 'no', group_id => $channels, user_id => {'!=' => $self->{user}->{id}}},
	 {select => qw/user_id/});

    
    return \@friends;
}

######################################################################

sub get_msg_count_on_network {
    my ($self,$user_id,$new_only,$network, $flagged) = @_;
    
    # Caveat: assumes that if its an array,
    # we want count of all networks.

    # This is because UI only permits selection of one particular
    # network or all of them.
    
    my $msg_rs = $self->{server}{schema}->resultset('SubMessages');
    
    $msg_rs = $msg_rs->search(flagged => $flagged) if (defined($flagged));
    
    $msg_rs = $msg_rs->search(dst_user_id => $user_id);
    
    $msg_rs = $msg_rs->search(heard => 'no') if ($new_only);
    
    $msg_rs = $msg_rs->search(channel => $network) unless (!defined($network) || ref($network) eq "ARRAY");
    
    
    my $msg_count = $msg_rs->count;
    
    $self->log (4, "count $msg_count");

    return $msg_count;

}

######################################################################
sub set_dirty_bit {
    my ($self,$user_id,$dirty) = @_;
    
    my $user_rs = $self->{server}{schema}->resultset('Watumiaji')->find($user_id);
    my $now = 'NOW()';
    
    if ($dirty) {
	$user_rs->update({dirty_time => \$now});
    }
    else {
	#TODO Not sure if this is a nice way to approach it even if it solves it
	$user_rs->update({calling_time => \$now});
    }

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

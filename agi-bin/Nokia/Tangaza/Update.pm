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

package Nokia::Tangaza::Update;

use Exporter;
@ISA = ('Exporter');
@EXPORT = ('update_main_menu');

use strict;
use DBI;
use Nokia::Tangaza::Network;
use Nokia::Common::Sound;
use Nokia::Common::Tools;

=head1 NAME

Nokia::Tangaza::Update - Module for making updates

=head1 DESCRIPTION

This module enables the use to send Tangazo to everyone on the 
selected group/vikundi.

=cut

#The values have been initialized in init
my $tmp_dir;# = '/mnt/tmpfs/';
my $tmp_rec_dir;# = $tmp_dir.'record/';

######################################################################

=head1 METHODS

=head2 can_post

Checks whether the user is allowed to send messages to the selected group/vikundi
Users can only post to groups they are members of.

Returns: 1 if the user is allowed, 0 otherwise

=cut

sub can_post {
    my ($self, $group_id) = @_;
    
    #if 'mine' group then you have to be admin to post
    my $count = 0;
    my $group = $self->{server}{schema}->resultset('Vikundi')->find
	($group_id, {select => qw/group_type/});
    
    return 1 if ('mine' ne $group->group_type);

    my $rs = $self->{server}{schema}->resultset('GroupAdmin')->search
	(group_id => $group_id, user_id => $self->{user}->{id});	
    
    return ($rs->count() > 0) ? 1 : 0;
    
}

######################################################################

=head2 init

Sets up global variables used througout the model i.e. file paths where
recordings will be saved and preferences defined in settings.conf

=cut

sub init {
    my ($self) = @_;
    
    my $prefs = $self->get_property('prefs');
    $tmp_dir = $prefs->{paths}->{NASI_TMP};
    $tmp_rec_dir = $tmp_dir.'record/';
}

######################################################################

=head2 update_main_menu

Plays the update menu, asking users to select what update actions 
they'd like to perform.

If the slot selected has no defined group, the selected group 
has no members or user has no permissions to post to the group,
the method plays back an error message to that effect and returns.

The recorded update will be saved in the path defined in settings.conf

=cut

sub update_main_menu {
    my ($self, $annotation) = @_;
    
    $self->log (4, "start update_main_menu");
    &init($self);
    
    if (&get_total_friend_count($self) == 0) {
	$self->log (4, "user has no friends");
	&play_random ($self, &msg($self,'please-add-people'), 'bummer');
	return 'ok';
    }
    
    my @select_network_prompts = &msg ($self, 'select-network');
    
    my ($channels, $has_name) = &select_network_menu ($self, \@select_network_prompts, 1);
    
    if (!defined($channels)) {
	&stream_file ($self, "no-network-defined-on-that-slot");
	return 'ok';
    }
    
    if ($has_name < 1) {
        my $rs = $self->{server}{schema}->resultset('GroupAdmin')->search
            (group_id => $channels, user_id => $self->{user}->{id});
	
        #if its the group admin ask them to record a new group name
        if ($rs->count() > 0) {
	    my $group_name_file = &set_group_name($self, $channels, &msg($self, 'record-name-for-group'));
	    
            if ($group_name_file eq 'cancel') {
                &play_random ($self, &msg($self,'cancelled-update'), 'ok');
		return 'cancel';
            }
	    
            if ($group_name_file eq 'timeout') { return 'ok'; }
	    
        }
	else {
	    &stream_file ($self, "group-not-active");
	    return 'ok';
	}
    }
    
    if (!&can_post($self, $channels)) {
    	&stream_file($self, 'you-cannot-post-to-this-group');
    	return 'ok';
    }
    
    $self->log (4, "received channel ".$channels);
    
    if ($channels eq 'timeout' ||
	$channels eq 'hangup' ||
	$channels eq 'cancel') {
	$self->log (4, "UPDATE return id ".$self->{user}->{id}.
		    " select_network_prompt $channels");
	return $channels;
    }
    
    # Make sure user has friends on in *this* network
    my $friend_count = &get_friend_count_on_network ($self, $channels);
    $self->log (4, "selected network friend count ".$friend_count);
    
    if ($friend_count <= 0) {
	&play_random ($self, &msg($self,'please-add-people-to-network'), 'bummer');
	return 'ok';
    }
    
    my $record_update_prompt = "record-update-all";
    my $update_file = &record_file ($self, &msg($self, $record_update_prompt), 20,
				    &msg($self,'to-keep-your-recording'), 0);
    
    $self->log (4, "UPDATE id ".$self->{user}->{id}." return $update_file");
    
    if ($update_file eq 'cancel') {
	&play_random ($self, &msg($self,'cancelled-update'), 'ok');
	return 'cancel';
    }
    
    if ($update_file eq 'timeout') { return 'timeout'; }
    
    if (defined($annotation)) {
	#concat the 2msgs
	my $file = $tmp_rec_dir.$update_file.".gsm";
	my $concat = "sox --combine sequence $annotation.gsm  $file $file";
	$self->log (4, "Forwarding: $concat");
	system ($concat);
    }
    
    # Move the message into the right location
    $update_file = mv_tmp_to_status_dir ($self, $update_file, 0);
    
    # move failed
    if (!defined($update_file)) {
	&play_random ($self, &msg($self,'error-has-occured'), 'bummer');
	$self->agi->stream_file(&msg($self,'please-try-again-later'), "*#", "0");
	return 'ok';
    }
    
    my $pub_id = &save_pub_message($self, $update_file, $channels);
    my $friend_tuples = &get_friends_on_network ($self, $channels);
    
    $self->log (4, "starting insert into sub_messages");
    my @dst_user_ids = ();
    
    foreach my $friend_tuple (@$friend_tuples) {
	my $dst_user_id = $friend_tuple->user_id->id;
	#my $channel = $friend_tuple->{channel};
	
	$self->log (4, "dst $dst_user_id channel $channels");
	
	# Update each person on this channel
	&save_sub_message ($self, $pub_id, $dst_user_id, $channels, \@dst_user_ids);
    }
    
    $self->log (4, "finished insert into sub_messages");
    
    # Update friends dirty bit
    foreach my $dst_user_id (@dst_user_ids) {
	$self->log (4, "dirty user_id $dst_user_id");
	&set_dirty_bit ($self, $dst_user_id, 1);
	
    }
    
    # Tell user that we are finished
    if (! &user_has_hungup($self)) {
	&stream_file($self,'sent-update', "*#", "0");
    }
    
#    eval {
#	&notify_dest($self, \@dst_user_ids, $channels);
#    };
    
    $self->log (4, "end update_main_menu");
    
    return 'ok';
}

######################################################################

=head2 notify_dest

Flashes all members in the group/vikundi to inform them that a new 
message has been sent to the group.

=cut

sub notify_dest {
    my ($self, $friends, $channel) = @_;
    $self->log(4, "Notifying users: ". join( ',', map { $_ } @$friends ));
    
    my $user_rs = $self->{server}{schema}->resultset('UserPhones')->search
	({user_id => {'IN' => [@$friends]}},
	 {select => qw/'phone_number'/});
    
    my $group = $self->{server}{schema}->resultset('Vikundi')->find($channel);
    
    while (my $phone = $user_rs->next) {
	my $num = $phone->phone_number;
	$num =~ s/^2547/07/;
	&flash_update ($self, $num);
	#&send_sms_update ($self, $$phone->phone_number, $group);
    }
    
    return 'ok';
    
}
######################################################################
sub send_sms_update {
    my ($self, $phone, $group) = @_;
    
    my $directions = "Tangaza! $self->{callerid} sent you a Tangaza \@".$group;
    &sms_enqueue ($self, $phone, $directions);
}

######################################################################

sub flash_update {
    my ($self, $phone) = @_;
    
    my $outbound = $phone;
    $outbound =~ s/^07/2547/;
    
    my $call_content =
        "Channel: SIP/nora01/1\n".
        "Context: jnctn-callback-tangaza\n".
        "Extension: 1\n".
        "CallerID: $phone\n".
	"Setvar: OUTBOUNDID=$outbound\n".
        "WaitTime: 15\n";
    
    $self->log (4, "Making missed call to $phone");
    $self->log (4, "content $call_content");                                                                            
    
    &place_call ($call_content);

}

######################################################################

=head2 save_pub_message

A message sent by a member is called a `pub_message`. This method
saves new updates to the database.

=over 4

=item Args:

$update_file - path to the recorded message

$channels - the group/vikundi that the message was sent to

=back

=cut

sub save_pub_message {
    my ($self, $update_file, $channels) = @_;
    $self->log (4, "START save_pub_message: $update_file $channels");
    
    my $now = 'NOW()';
    
    # Insert into pub_messages
    my $msg = $self->{server}{schema}->resultset('PubMessages')->create
	({src_user_id => $self->{user}->{id}, channel => $channels,
	  filename => $update_file, timestamp => \$now});
    
    my $pub_id = $msg->id;
    $self->log (4, "created pub_messages id ".$pub_id);
    
    return $pub_id;
}

######################################################################

=head2 save_sub_message

Each pub message is mapped to a user in the group - this is called sub_message.
This method attaches a message to a specific user within the group

=over 4

=item Args:
$pub_id - the pub_message this refers to

$dst_user_id - the group member to receive this message

$channel - the group/vikundi this message belongs to

$dst_user_ids - a buffer array with ids of all users who this message was sent to

=back

=cut
sub save_sub_message {
    my ($self, $pub_id, $dst_user_id, $channel, $dst_user_ids) = @_;
    my $now = 'NOW()';
    
    my $msg = $self->{server}{schema}->resultset('SubMessages')->create
	({message_id => $pub_id, dst_user_id => $dst_user_id, 
	  channel => $channel, timestamp => \$now, heard => 'no', flagged => 'no'});
    
    push (@$dst_user_ids, $dst_user_id);
}

=head1 AUTHORS

Billy Odero, Jonathan Ledlie

Copyright (C) 2010 Nokia Corporation.

=cut


1;

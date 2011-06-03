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

package Nokia::Tangaza::Listen;

use Exporter;
@ISA    = ('Exporter');
@EXPORT = ( 'listen_main_menu', 'listen_new_menu' );

use strict;
use DBI;
use Nokia::Tangaza::Network;
use Nokia::Tangaza::Update;
use Nokia::Common::Sound;
use Nokia::Common::Tools;

=head1 NAME

Nokia::Tangaza::Listen - Module for listening to updates

=cut

=head1 DESCRIPTION

This module allows the user to playback new and existing messages
sent to a particular group.

=head1 METHODS

=cut
######################################################################

sub get_all_groups {
    my ($self) = @_;
    
    my @groups = $self->{server}{schema}->resultset('UserGroups')->search
	({user_id => $self->{user}->{id}, is_quiet => 'no'},
	 {select => [qw/group_id/]});
    
    return \@groups;
}
######################################################################

=head2 listen_main_menu

Plays the listening menu options for the user to determine what actions to take.

Once users select the group/vikundi whose messages they want to listen to, they 
have the option to listen to new, old or flagged messages.
They can also flag messages for quick retrieval in future.

=cut

sub listen_main_menu {
    my ($self) = @_;
    
    $self->log( 4, "start listen_main_menu" );
    
    my $networks_w_updates_count = 0;
    my $friends_updates_count    = 0;
    
    my $updated_networks_str = '';
    
    #get all groups that arent on quiet mode nor inactive
    my $groups = &get_all_groups($self);
    
    #foreach my $network (&get_non_quiet_groups($self)) {}
    foreach my $network (@$groups) {
	my $new_msg_count =
	    &get_msg_count_on_network( $self, $self->{user}->{id}, 1, $network->group_id->id );
	
	if ( $new_msg_count > 0 ) {
	    $networks_w_updates_count++;
	}
    }
    
    my $total_msg_count =
	&get_msg_count_on_network( $self, $self->{user}->{id}, 0 );
    
    if ( $total_msg_count <= 0 ) {
	&play_random( $self, &msg( $self, 'no-messages-any-network' ),
		      'bummer' );
	return 'ok';
    }
    
    my $updated_networks_msg = &msg( $self, 'no-new-messages' );
    
    my @prompts = ( &msg( $self, 'listen-main-menu' ) );
    
    if ( $networks_w_updates_count >= 1 ) {
	
	push( @prompts, &msg( $self, 'to-hear-them-press-one' ) );
	
	my $res = &dtmf_quick_jump( $self, \&listen_new_menu, \@prompts );
	
	# the user listened to new messages or hit cancel,
	# return to main menu
	if ( $res eq 'ok' || $res eq 'cancel' ) {
	    return $res;
	}
	
	# otherwise (he timed out) proceed to picking a network
	@prompts = ( &msg( $self, 'select-network' ) );
	
    }
    else {
	$self->agi->stream_file($updated_networks_msg);
	
	# if he has no updates, just let him pick a network
	
	push( @prompts, &msg( $self, 'select-network' ) );
    }
    
    my ($channels, $has_name) = &select_network_menu( $self, \@prompts, 1 );
    
    $self->log( 4, "received channel " . $channels );
    
    if ( ref($channels) ne "ARRAY"
	 && $channels eq 'timeout' ){
	return 'timeout';
    }
    
    if ( ref($channels) ne "ARRAY" ) {
	if (   $channels eq 'timeout'
	       || $channels eq 'hangup'
	       || $channels eq 'cancel' ) {
	    $self->log( 4,
			"LISTEN return id "
			. $self->{user}->{id}
			. " select_network_prompt $channels" );
	    return $channels;
	}
    }
    my $flagged_updates_count =
	&get_msg_count_on_network( $self, $self->{user}->{id},
				   0, $channels, 'yes' );
    
    $self->log( 4,
		"user: $self->{user}->{id}, $channels, flagged message count: $flagged_updates_count"
		);
    my $network_msg_count =
	&get_msg_count_on_network( $self, $self->{user}->{id}, 0, $channels );
    if ( $network_msg_count <= 0 ) {
	&play_random( $self, &msg( $self, 'no-all-messages' ), 'bummer' );
	return 'ok';
    }
    
    my $res = '';
    
    # Loop through this channel
    # Return to main menu when finished
    
    while ( $res ne 'timeout' && $res ne 'cancel' && $res ne 'hangup' ) {
	
	my $msg_type = 3;
	my $dtmfs    = '123*';
	my $prompt   = 'listen-main-menu-2';
	
	#TODO implement the stuff below only play prompt if msg in category 1-3
	
	#if ( $friends_updates_count > 0 ) {
	#	$prompt = 'To listen to new messages, press 1. ';
	#	$dtmfs  = '1';
	#}
	#if ( $flagged_updates_count > 0 ) {
	#	$prompt .= 'To listen to flagged messages, press 2. ';
	#	$dtmfs  .= '2';
	#}
	
	#$prompt .= ' To listen to all messages, press 3. ';
	#$dtmfs  .= '3*';
	
	$self->log( 4, "prompt: $prompt, dtmfs: $dtmfs" );
	
	$msg_type =
	    &get_unchecked_small_number( $self, &msg( $self, $prompt ), $dtmfs );
	
	# New->1
	# Flagged->2
	# All->3
	
	if (   $msg_type eq 'timeout'
	       || $msg_type eq 'hangup'
	       || $msg_type eq 'cancel' ) {
	    $self->log( 4,
			"LISTEN return id "
			. $self->{user}->{id}
			. " msg_type $msg_type" );
	    return $msg_type;
	}
	
	$res = &walk_messages_menu( $self, $msg_type, $channels );
    }
    return $res;
    
}

######################################################################

=head2 listen_new_menu

This only plays new messages to the user.

=cut
sub listen_new_menu {
	my ($self) = @_;

	# Only listen to new messages
	# and return to where we came from.

	return &walk_messages_menu( $self, '1' );

}

######################################################################

=head2 walk_messages_menu

Goes through all the messages the user would like to listen to based 
on supplied arguments (below).

=over 4

=item Args:

$msg_type: '1' - new messages; '2' - flagged messages; 'undefined' - plays all

$channels: the group whose messages are to be played

=back

=cut

sub walk_messages_menu {
    my ( $self, $msg_type, $channels ) = @_;
    
    # make nice debug message
    my $debug_msg = "WALK start id " . $self->{user}->{id};
    if ( defined($channels) ) {
	$debug_msg .= " channels $channels";
    }
    else {
	$debug_msg .= " channels null";
    }
    
    $debug_msg .= " msg_type $msg_type";
    $self->log( 4, $debug_msg );
    
    die if ( !defined($msg_type) );
    
    # Base select statement
    my $msgs_rs = $self->{server}{schema}->resultset('SubMessages')->search
	({dst_user_id => $self->{user}->{id}},
	 {columns => [qw/pub_messages.timestamp id message_id heard flagged filename src_user_id/]},
	 {prefetch => 'message_id'},
	 #{order_by => 'id desc'}
	 #{order_by => {desc => 'id'}}
	 );
    
    $msgs_rs = $msgs_rs->search({'me.channel' => $channels}) if (defined($channels));
    
    # New->1
    # Flagged->2
    # All->3
    
    my $new_flagged_all = 'all';
    
    if ( $msg_type eq '1' ) {
	$msgs_rs = $msgs_rs->search({heard => 'no'});
	$new_flagged_all = 'new';
    }
    elsif ( $msg_type eq '2' ) {
	$msgs_rs = $msgs_rs->search({flagged => 'yes'});
	$new_flagged_all = 'flagged';
    }
#    else {
#	die("Should not be reached");
#    }
    
    my $dtmf = 0;
    if ( !defined( $self->{played_listen_directions} ) ) {
	
	if ( $self->{newuser} ) {
	    $dtmf = &stream_file( $self, 'listen-directions-short', "*#", "0" );
	}
	else {
	    $dtmf = &stream_file($self, 'offer-directions', "*#", "0" );
	}
	
	#&stream_file( $self, 'to-forward-with-your-annotation-press-4' );
	$self->{played_listen_directions} = 1;
    }
    
    my $digits      = "01234*#";
    my $prefs       = $self->get_property('prefs');
    my $updates_dir = $prefs->{paths}->{NASI_DATA}."/status/";
    my $done        = 0;
    
    my @msgs = $msgs_rs->all();
    $self->log( 4, "msg count " . ( $#msgs + 1 ) );
    
    for (my $m = 0; $m <= $#msgs && !$done && defined($dtmf) && $dtmf >= 0;$m++ ) {
	my $msg = $msgs[$m];
	
	$self->log( 4,
		    "m $m msg_id "
		    . $msg->message_id->id
		    . " sub_id "
		    . $msg->id
		    . " src_user_id "
		    . $msg->message_id->src_user_id->id );
	
	
	
	#TODO: add prompt telling which slot/group msg is from
	#&stream_file( $self, 'sent-from' );
	#$dtmf =
	#  $self->agi->stream_file( $nickname_file, "#", "0" );
	
	if ( defined($dtmf) && $dtmf == 0 ) {
	    $dtmf = $self->agi->get_option( $updates_dir . $msg->message_id->filename, "$digits", 250 );
	    
	    # set listened bit
	    my $sub_msg = $self->{server}{schema}->resultset('SubMessages')->find($msg->id);
	    $sub_msg->update({heard => 'yes'});
	    
	    # if the user did not hit a key while listening
	    # to that message, play a beep and give him a chance
	    # to hit a key again
	    if ( defined($dtmf) && $dtmf == 0 ) {
		$dtmf = $self->agi->get_option( &msg( $self, 'inter-msg-beep' ),
						"$digits", 2000 );
	    }
	}
	    
	# process input that might have occurred
	# while user listening to message
	
	while ( defined($dtmf) && $dtmf > 0 && !$done ) {
	    
	    my $input = chr($dtmf);
	    $dtmf = 0;
	    
	    if ( $input eq '2' ) {
		
		# repeat the message
		$m--;
		if ( $m < -1 ) { $m = -1; }
		$self->log( 4, "repeat m $m" );
		
		$dtmf = &stream_file($self, 'repeat', "*#", "0" );
	    }
	    elsif ( $input eq '3' ) {
		
		# skip ahead to the next message
		# do nothing
		
		$self->log( 4, "skip m $m" );
		
		$dtmf = &stream_file($self, 'skip', "*#", "0" );
	    }
	    elsif ( $input eq '1' ) {
		
		# jump backward
		$m -= 2;
		if ( $m < -1 ) { $m = -1; }
		$self->log( 4, "back m $m" );
		
		$dtmf = &stream_file($self, 'back', "*#", "0" );
	    }
	    elsif ( $input eq '0' ) {
		
		# repeat the message after the directions
		$m--;
		if ( $m < -1 ) { $m = -1; }
		$self->log( 4, "directions m $m" );
		
		# First give the user
		# brief directions and then give him the option of
		# hearing more.
		# The menu will react to what people type
		# while receiving help.
		
		$dtmf = $self->agi->get_option(
					       &msg( $self, 'listen-directions-short' ),
					       "*#1234567890", 500 );
		
		if ( defined($dtmf) && chr($dtmf) eq '0' ) {
		    
		    $dtmf = $self->agi->get_option(
						   &msg( $self, 'listen-directions-long' ),
						   "*#1234567890", 500 );
		}
		
	    }
	    elsif ( $input eq '#' ) {
		
		# TODO Assumption is that this doesn't change the
		# hash that we are currently working with
		# that contains the list of messages
		
		$self->log( 4, "flagging m $m" );
		
		my $sub_msg = $self->{server}{schema}->resultset("SubMessages")->find($msg->id);
		
		if ( $sub_msg->flagged eq 'yes' ) {
		    
		    $sub_msg->update({flagged => 'no'});
		    
		    $dtmf = &stream_file ($self, 'flag-removed', "*#", "0" );
		}
		else {
		    $sub_msg->update({flagged => 'yes'});
		    
		    # something like "message flagged" or "flag set"			
		    $dtmf = &stream_file ($self, 'flagged', "*#", "0" );
		}
	    }
	    elsif ( $input eq '*' ) { $done = 1; }
	    elsif ( $input eq '4' ) {
		&stream_file( $self, 'adding-your-annotation' );
		
		#stream_file ($self, 'beep');
		&update_main_menu( $self, $updates_dir . $msg->message_id->filename );
	    }
	}
    }
    
    if ( defined($dtmf) && $dtmf >= 0 && !$done ) {
	
	if ( $#msgs < 0 ) {
	    # sn-no-new-messages
	    # sn-no-flagged-messages
	    # sn-no-all-messages
	    $dtmf = &stream_file ($self, 'no-' . $new_flagged_all . '-messages', "*#", "0");
	}
	else {
	    # TODO should give person chance to rewind
	    # at least while playing this
	    $dtmf = &stream_file($self, 'end-of-messages', "*#", "0");
	}
	
    }
    
    $self->log( 4, "end walk_messages_menu" );
    return 'ok';
    
}

=head1 AUTHORS

Billy Odero, Jonathan Ledlie

Copyright (C) 2010 Nokia Corporation.

=cut

1;

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

package Nokia::Tangaza::Invitations;

use Exporter;
@ISA = ('Exporter');
@EXPORT = ('invitations_main_menu', 'invite_friends_menu', 'play_invites');

use strict;

use Nokia::Tangaza::Callback;
use Nokia::Common::Tools;
use Nokia::Common::Sound;
use Nokia::Common::Phone;


use DBI;

######################################################################
sub invitations_main_menu {
    my ($self) = @_;

    $self->log (4, "start invitations_main_menu");

    my %words = 
		('prompt' => &msg($self, 'invitations-main-menu'),
		 'pre' => &msg($self,''));

    my %dispatch =
		(1 => \&invite_friends_menu,
		 2 => \&play_invites_menu);

    &dtmf_dispatch_static ($self, \%words, \%dispatch, '12*');

    $self->log (4, "end invitations_main_menu");

}

######################################################################                                                                         

sub check_end_network_modify_menu {
    my ($self, $state, $action) = @_;

  if ($state eq 'timeout' || $state eq 'cancel' ||
      $state eq 'hangup') {

      if ($state eq 'timeout' || $state eq 'cancel') {
	  &play_random ($self, &msg($self,"cancelled-$action"), 'ok');
      }
      $self->log (4, "a $action s $state");
      return 1;
  }
    return 0;
}

######################################################################
sub invite_friends_menu {
    my ($self) = @_;
    
    $self->log (4, "start invite_friends_menu, user_id ".$self->{user}->{id});

    # check number of remaining invitations
    $self->{server}{invitations_remaining_sth} =
	$self->{server}{dbi}->prepare_cached
		("select invitations_remaining from users where user_id = ?");
	
    $self->{server}{invitations_remaining_sth}->execute ($self->{user}->{id});
	
    my $invitations_remaining = 
		$self->{server}{invitations_remaining_sth}->fetchrow_arrayref()->[0];
	
    $self->{server}{invitations_remaining_sth}->finish();

    $self->log (4, "user_id ".$self->{user}->{id}.
	       " has $invitations_remaining invitations remaining");    
	
    while (1) {
		if ($invitations_remaining <= 0) {
		    $self->agi->stream_file (&msg($self,'sorry-out-of-invitations'), "","0");
		    return;
		}
		
		my @prompts = (&msg($self,'you-have'),&msg($self,$invitations_remaining),
			       &msg($self,'invitations-remaining'),
			       &msg($self,'want-to-send-new-invitations'));
		
		my $send_new = &get_yes_no_option
		    ($self, \@prompts);
		
		if ($send_new eq 'timeout' ||
		    $send_new eq 'cancel' ||
		    $send_new eq 'hangup' ||
		    $send_new eq 'no') {
		    $self->log (4, "TELL user_id ".$self->{user}->{id}.
			      " decided not to send an invitation");
		    return;
		}
		
		my $friend_phone = &get_large_number($self, &msg($self,'tell-prompt'));
		
		# check that given number is valid
		if (!&is_valid_outbound_number($self, \$friend_phone)) {
		    $self->log (4, "not adding because number looks invalid ".
				"$friend_phone");
		    
		    $self->agi->stream_file
				(&msg($self,'sorry-invalid-number'),"1234567890*#","0");
		    
		    return 'cancel';
		}
		
		my $invited = &invite_new_friend($self, $friend_phone);
		if ($invited eq 'ok') {
		    $invitations_remaining--;
		}
    }
}

######################################################################
sub invite_new_friend {
    my ($self, $friend_phone) = @_;
    my $invites_dir = '/data/invites/messages/';
    my $nicknames_dir = '/data/invites/names/';
    
    my $friend_user_id = 0;
    my $current_channel;
    
    $friend_user_id = &get_user_id($self, $friend_phone);
    
    #check if already connected
    if ($friend_user_id > 0) {
        $current_channel = &get_network_of_friendship($self, $friend_user_id);
    }
    
    if (defined($current_channel)) {
		$self->agi->stream_file
		    (&msg($self,'already-connected-to-person'),"1234567890*#","0");
		
	  	return 'cancel';
    }
    else {
		#select network that you'd like the person to be added to
		my $current_channel = &select_network_menu
		    ($self, &msg($self,'add-to-network'), 0);
		
		#create nickname for friend
		my $nickname_file = &record_file
		    ($self, &msg($self, 'add-nickname'), 5,
		     &msg($self,'to-keep-your-nickname'), 1);
		
		if (&check_end_network_modify_menu ($self, $nickname_file, 'add')) {
		    return $nickname_file;
		}
		
		$self->log (4, "nickname $nickname_file");	
		
		#record invite message to play to friend
		my $message = &record_file
		    ($self, &msg($self, 'record-your-invite-message'), 10, 
		     &msg($self, 'To keep, press 1. To listen, press 2. '.
			  'To record new message, press 3.'), 1);
		
		if (&check_end_network_modify_menu ($self, $message, 'add')) {
		    return $message;
		}
		
		$self->log(4, "the message: $message");
		
		#Check for previous invites
		$self->{server}{check_invite_sth} =
		    $self->{server}{dbi}->prepare_cached
			("select invite_id from invitations where src_user_id = ? ".
			 "and dst_user_id = ? and status = 'pending'");
		
		$self->{server}{check_invite_sth}->execute(
		    $self->{user}->{id}, $friend_user_id);
		my ($invite_id) = $self->{server}{check_invite_sth}->fetchrow_array();
		
		$self->{server}{check_invite_sth}->finish();
		
		if (defined($invite_id)) {
		    $self->{server}{update_invite_sth} =
			$self->{server}{dbi}->prepare_cached
			("update invitations set ".
			 "invite_message = ?, channel = ?, nickname = ? where invite_id = ?");
		    
		    $self->{server}{update_invite_sth}->execute(
			$message, $current_channel, $nickname_file, $invite_id);
		    
		    $self->{server}{update_invite_sth}->finish();
		}
		else{
		    #if user already in system invite them, if not create them then invite
		    if ($friend_user_id < 1){
				my %user_desc = ();
				$user_desc{phone} = $friend_phone;
				$friend_user_id = &create_user ($self, \%user_desc);
		    }
		    
		    $self->{server}{insert_invite_sth} =
			$self->{server}{dbi}->prepare_cached
				("INSERT INTO invitations (src_user_id, dst_user_id,".
				 "invite_message, channel, nickname) VALUES (?, ?, ?, ?, ?)");
		    
		    $self->{server}{insert_invite_sth}->execute(
				$self->{user}->{id}, $friend_user_id, $message, 
				$current_channel, $nickname_file);
		    
		    $self->{server}{insert_invite_sth}->finish();
		}
		
		#Update dirty time
		&set_dirty_bit($self, $friend_user_id, 1);
		&update_invite_count($self);
		
		$self->log (4, "invited friend, phone ".$friend_phone);
		
		$self->agi->stream_file	(&msg($self,'invitation-sent'),"","0");
		
		return 'ok';
    }
    
}

######################################################################
#NOT used anymore - invitation notice sent using daemon script
sub send_invite {
    #TODO
    #sends a text message, or flash: yet to decide
    my ($self, $message, $friend_phone) = @_;
    &Nokia::Tangaza::Callback::place_call_tangaza ($friend_phone);
}


######################################################################
sub update_invite_count {
    my ($self) = @_;
    
    $self->{server}{update_invites_remaining_sth} =
	$self->{server}{dbi}->prepare_cached
		(" UPDATE users SET invitations_remaining = invitations_remaining - 1 where user_id = ?");
    $self->{server}{update_invites_remaining_sth}->execute($self->{user}->{id});
    $self->{server}{update_invites_remaining_sth}->finish();
 
}

######################################################################
sub accept_invite {
    my ($self, $invitation_id, $inviter_id, $friend_nickname, $selected_channel) = @_;
    
    my $channel = &select_network_menu
		($self, &msg($self,'add-to-network'), 0);

    if (&check_end_network_modify_menu ($self, $channel, 'add')) {
      return $channel;
    }
    
    # Create nickname for inviter
    my $nickname_file = &record_file
		($self, &msg($self, 'add-nickname'), 5,
		 &msg($self,'record-name-menu'), 1);
    
    if (&check_end_network_modify_menu ($self, $nickname_file, 'add')) {
		return $nickname_file;
    }
    
    $self->log (4, "nickname $nickname_file");
    
    $self->{server}{update_invites_status_sth} =
	$self->{server}{dbi}->prepare_cached
	    (" UPDATE invitations SET status = 'accepted',  heard = 'yes'
	    where invite_id = ?");
    $self->{server}{update_invites_status_sth}->execute($invitation_id);
    $self->{server}{update_invites_status_sth}->finish();
    
    #Dealing with side B - invited friend
    #on accept invite create the relationship
    
    #B should select network to add friend
    
    &add_friend($self, $self->{user}->{id}, $inviter_id, $nickname_file, $channel);
    
    &play_random ($self, &msg($self,"added-new-friends"), 'great');
    
    #Dealing with side A - inviter
    #Add to A's pre-selected network - selected during the invite
    
    &add_friend($self, $inviter_id, $self->{user}->{id}, $friend_nickname, $selected_channel);
    
    $self->log (4, "invitation accepted");

    return 'ok';
    
}

######################################################################
sub add_friend {
    my ($self, $src_user_id, $dest_user_id, $nickname_file, $channel) = @_;
    
    $self->{server}{friend_insert_sth} =
	$self->{server}{dbi}->prepare_cached
		("INSERT INTO friends (src_user_id, dst_user_id, channel) ".
		 "VALUES (?, ?, ?)");
    $self->{server}{friend_insert_sth}->execute
		($src_user_id, $dest_user_id, $channel);

    $self->{server}{friend_insert_sth}->finish();
    
    &set_nickname_file($self, $src_user_id, $dest_user_id, $nickname_file);
    
}

######################################################################
sub notify_inviter {
    #Notifies the inviter that the friend has accepted request/invitation
    #Should we notify inviter of rejected invites??
    my ($self, $message) = @_;
    
    #Am thinking text message should work??
    
}

######################################################################
sub reject_invite {
    my ($self, $invite_id) = @_;

    $self->{server}{update_invite_status_sth} =
	$self->{server}{dbi}->prepare_cached
	    (" UPDATE invitations SET status = 'rejected', heard = 'yes'
	    where invite_id = ?");
    $self->{server}{update_invite_status_sth}->execute($invite_id);
    $self->{server}{update_invite_status_sth}->finish();
  
}

######################################################################
sub get_invite_count {
    my ($self) = @_;
    
    $self->{server}{get_invite_count_sth} =
	$self->{server}{dbi}->prepare_cached
	    ("Select count(*) from invitations where dst_user_id = ? ".
	     " and status = 'pending'");
    
    $self->{server}{get_invite_count_sth}->execute($self->{user}->{id});

    my ($invite_count) = $self->{server}{get_invite_count_sth}->fetchrow_array();

    $self->{server}{get_invite_count_sth}->finish();

    return $invite_count;
  
}

######################################################################
sub play_invites_menu {
    my ($self) = @_;
    my $row_count = &get_invite_count($self);

    if ($row_count > 0) {
		&stream_file($self, [&msg($self, 'you-have'), 
			&msg($self, '$row_count'), &msg($self, 'new-invitations')]);
		
		my $prompt = &msg($self,'listen-to-invitations');
		my $listen_to_invites = &get_yes_no_option
		    ($self, $prompt);
	
		if ($listen_to_invites eq 'timeout' ||
		    $listen_to_invites eq 'cancel' ||
		    $listen_to_invites eq 'hangup' ||
		    $listen_to_invites eq 'no') {
		    
		    $self->log (4, "user_id ".$self->{user}->{id}.
			      " did not listen to invitations.");
		    return;
		}
		
		&play_invites($self, 'new');
    }
    else {
		&stream_file($self, 'you-have-no-new-invitations');
    }
    
}

######################################################################
sub play_invites {
    
    my ($self, $type) = @_;
    my $heard = "";
	
    if ($type eq 'new'){
		$heard = " and heard = 'no' ";
    }
    
    $self->{server}{get_new_invites_sth} =
	$self->{server}{dbi}->prepare_cached
	    ("select invite_id, src_user_id, invite_message, nickname, name_file, channel from invitations ".
	     "inner join users on invitations.src_user_id = user_id where ".
	     "invitations.status = 'pending' and dst_user_id = ? $heard");
    
    $self->{server}{get_new_invites_sth}->execute($self->{user}->{id});

    while (my ($invite_id, $src_user, $message, $nickname, $inviter, $channel) = 
	   $self->{server}{get_new_invites_sth}->fetchrow_array()){
	   	
		if (defined($inviter)) {
		    &stream_file($self, $inviter);
		}
		&stream_file($self, $message);
		
		my $prompt = &msg($self,'Do you want to add this person as a friend?');
		my $add_friend = &get_yes_no_option
		    ($self, $prompt);
		
		if ($add_friend eq 'timeout' ||
		    $add_friend eq 'cancel' ||
		    $add_friend eq 'hangup' ||
		    $add_friend eq 'no') {
		    
		    &reject_invite($self, $invite_id);
		    
		    &stream_file($self, 'invitation-rejected');
		    
		    $self->log (4, "user_id $self->{user}->{id} rejected invitation");
	
		    #return;
		}
		else {
	
		    my $invite_accepted = &accept_invite($self, $invite_id, $src_user, $nickname, $channel);
		    if ($invite_accepted eq 'ok') {
				
				&stream_file($self, 'added-new-$channel');
				$self->log (4, "user_id $self->{user}->{id} accepted invitation");
		    }
		}
    }
    
    $self->{server}{get_new_invites_sth}->finish();
}

######################################################################
1;

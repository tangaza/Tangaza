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

package Nokia::Tangaza::Entry;

use strict;
use base 'Asterisk::FastAGI';
use DBI;

use Nokia::Tangaza::Update;
use Nokia::Tangaza::Listen;
use Nokia::Tangaza::Network;
use Nokia::Common::Sound;
use Nokia::Common::Tools;
use Nokia::Common::Entry;
use Nokia::Common::Auth;
use Nokia::Common::SMSQueue;

=head1 NAME

Nokia::Tangaza::Entry - Entry point into the system

=head1 DESCRIPTION

This is the entry module into Tangaza

=head1 METHODS

=cut
######################################################################

=head2 entry

This is the the first method that should be executed when starting 
up the system.

It initializes `$self` with all the necessary information.

=cut
sub entry {

    # Start of Tangaza call
    my $self = shift;
    
    $self->log (4, "socnet start entry");

    $self->{fn_start_call} = \&start_call;
    $self->{fn_end_call} = \&end_call;
    $self->{fn_main_menu} = \&main_menu;
    $self->{welcome_msg} = 'welcome-to-socnet';

    &Nokia::Common::Entry::entry ($self);

    $self->log (4, "socnet end entry");


}


######################################################################

sub send_more_about_tangaza {

    #to send text on more info about tangaza
    my ($self) = @_;
    my $phone = $self->{user}->{phone};

    my $more_info = "All calls to Tangaza are recorded.  Privacy policy available at http://www.nokia.com/tangaza/privacy.";
    
    &send_sms ($self, $phone, $more_info);
    
    $self->log (4, "sent more about tangaza to $phone");
}

######################################################################

=head2 about_socnet_main_menu

Plays the `about page` to the user.

=cut
sub about_socnet_main_menu {
    my ($self) = @_;

    my $dtmf = $self->agi->stream_file 
	(&msg($self,'about-socnet'), "1234567890*#","0");

}

######################################################################

=head2 main_menu

This is the entry point into the system. 

It plays the welcome message, lets the user know if there are any new 
messages to listen to and gives the user the options necessary to access 
all other menus (i.e. update, listen and about menu) within the system.

=cut
sub main_menu {
    my ($self) = @_;
    
#    $self->{origin} = $self->agi->get_variable('origin');
#    $self->{callout_ext} = $self->agi->get_variable("callout-ext-$self->{origin}");
#    $self->{sms_number} = $self->agi->get_variable("sms-number-$self->{origin}");
    
#    $self->log(4, "Call Origin: ".$self->{origin}." Country Code: ".$self->agi->get_variable("ext-$self->{origin}"));
    
    if ($self->{newuser} == 1) {
	my $current_language = $self->{user}->{language};
	
	$self->log ("played intro?");
	
	if (!defined($self->{played_intro})) {
	    $self->log ("playing intro");
	    &stream_file ($self, $self->{welcome_msg}, "#");
	    $self->{played_intro} = 1;
	} else {
	    $self->log ("played intro NULL");
	}
	
	$self->log (4, "calling select language");
	#&select_language ($self);
	$self->{user}->{language_id} = 1;
	$self->log (4, "called select language");
	
	if ($self->{user}->{language} ne $current_language) {
	    &stream_file ($self, 'welcome-to-socnet', "#");
	}
	
	&send_sms_directions ($self);
    }
    
    $self->log (4, "get_total_friend_count = ".&get_total_friend_count($self));

    if (&get_total_friend_count($self) == 0) {
	$self->log (4, "sending sms on how to invite");
	&send_sms_how_to_invite ($self);
    }

    
    # Privacy notice
    # TODO removing for demo purposes
#    if (&accepted_terms_and_privacy($self) eq 'no') {
#	&stream_file ($self, 'welcome-to-socnet', "#");
	
#	if (&require_terms($self) ne 'ok') {
#	    return;
#	}
#    } 

    # JL new code
    #while (&get_unnamed_network_count ($self) > 0) {

    #}
    
    if (&get_msg_count_on_network ($self, $self->{user}->{id}, 1) > 0) {
	my @prompt = ();
	if (!defined($self->{played_intro})) {
	    push (@prompt, &msg($self,'welcome-to-socnet'));
	    $self->{played_intro} = 1;
	}
	push (@prompt, &msg($self,'you-have-new-messages'));
	push (@prompt, &msg($self,'to-hear-them-press-one'));
	
	&dtmf_quick_jump ($self, \&listen_new_menu,
			  \@prompt);
    }

    
    my @prompt = ();

    my %words = ('prompt' => &msg($self,'main-menu'));
    
    if (!defined($self->{played_intro})) {
        $words{'pre'} = &msg($self,'welcome-to-socnet');
	# insert language choice prompt here
	
        $self->{played_intro} = 1;
    }
    
    my $namefile = &get_user_name($self, $self->{user}->{id});
    if (!defined($namefile)) {
	$self->log(4, "No username set: calling set_user_name");
	$namefile  = &set_user_name ($self, $self->{user}->{id}, &msg($self, 'record-name-now'));
    }
    
    $self->{user_name} = $namefile;

    my %dispatch =
                (1 => \&update_main_menu,
                 2 => \&listen_main_menu,
                 3 => \&about_socnet_main_menu);

    my $digits = '123*';

    &dtmf_dispatch_static ($self, \%words, \%dispatch, $digits);
    

}


######################################################################

sub start_call {
    my ($self) = @_;

    $self->log (4, "socnet start_call");

    &set_dirty_bit ($self, $self->{user}->{id}, 0);

}

######################################################################

sub end_call {
    my ($self) = @_;

    $self->log (4, "socnet end_call");

    # TODO not resetting flashing for now
    #&set_dirty_bit_if_new_msgs ($self, $self->{user}->{id});

}

######################################################################
sub send_sms_directions {
    my ($self) = @_;

#    my $directions = "Tangaza, a Nokia alpha service. Empty msg for updates. Send: 'join groupname' to join. Reply: 'help' for more. Send to $self->{sms_number}. Enjoy!";
#    &sms_enqueue ($self, $self->{callerid}, $directions);
    
}

######################################################################
sub send_sms_how_to_invite {
    my ($self) = @_;
    
#    my $directions = "Send: 'invite groupname friend1 friend2' to invite your friends to Tangaza.  Use friends phone number. Send to $self->{sms_number}";
#    &sms_enqueue ($self, $self->{callerid}, $directions);
    
}

######################################################################
sub accepted_terms_and_privacy {
    my ($self) = @_;
    
    my $user = $self->{server}{schema}->resultset('Watumiaji')->find($self->{user}->{id});
    $self->log(4, "Accepted terms: $user->accepted_terms");
    return $user->accepted_terms;
}

######################################################################
sub require_terms {
    
    my ($self) = @_;
    my $ret = '';
    
    my %menu = 
		('prompt' => &msg($self,'accept-terms-and-policy'),
		 'pre' => '');
    
    my %dispatch =
		(1 => \&accept_terms,
		 2 => \&play_terms,
		 3 => \&play_privacy,
		 4 => \&reject_terms);
    
    for (my $i = 0; $i < 3 && ($ret ne 'ok'); $i++) {
	$ret = &Nokia::Common::Tools::dtmf_dispatch ($self, \%menu, \%dispatch, '1234*');
	
	if ($ret eq 'hangup') {
	    return;
	}
    }
#    $ret = &dtmf_dispatch_static ($self, \%menu, \%dispatch, '1234*');
    return $ret;
}

######################################################################
sub play_terms {
    my ($self) = @_;

    $self->log(4, 'Playing terms and conditions');

    my @terms = (#'terms-conditions-announce',
		 'terms-conditions');
    
    &stream_file($self, @terms, '*');
    
}

######################################################################
sub play_privacy {
    my ($self) = @_;

    $self->log(4, 'Playing privacy policy');

    my @prompt = (#'privacy-policy-announce',
		  'privacy-policy');

    &stream_file($self, @prompt, '*');
    
}

######################################################################
sub accept_terms {
    my ($self) = @_;
    
    #update members
    my $user = $self->{server}{schema}->resultset('Watumiaji')->find($self->{user}->{id});
    $user->update({accepted_terms => 'yes'});
    
    #log
    my $terms = $self->{server}{schema}->resultset('terms_and_privacy')->create
	({user_id => $self->{user}->{id}, status => 'accepted'});
    
    return 'ok';
}

######################################################################
sub reject_terms {
    my ($self) = @_;
    #Dont think we need to log this
    #log
    my $terms = $self->{server}{schema}->resultset('terms_and_privacy')->create
	({user_id => $self->{user}->{id}, status => 'rejected'});
    
    return 'hangup';
}

######################################################################

=head1 AUTHORS

Billy Odero, Jonathan Ledlie

Copyright (C) 2010 Nokia Corporation.

=cut

1;

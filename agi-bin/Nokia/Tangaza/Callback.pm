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

package Nokia::Tangaza::Callback;

use strict;
use base 'Asterisk::FastAGI';
use Sys::Hostname;
use Nokia::Common::Tools;
use Nokia::Common::Callback;

=head1 NAME

Nokia::Tangaza::Callback - Module for calling back users

=head1 DESCRIPTION

Nokia::Tangaza::Callback calls back a user that made a missed call to our system.

=cut

######################################################################

=head1 METHODS

=head2 callback

Checks the callback state variable `cbstate` to determine if the user 
called us or if we need to call them back. If `cbstate` == 'calledback'
it places a call.

=cut

sub callback {
    my $self = shift;    

    #&dbi_connect ($self);

    #$self->log (4, "XXX switch to sfcom specific flash");

    &Nokia::Common::Callback::callback ($self);


    if ($self->{cbstate} eq 'calledback') {
	sleep (2);
	&place_call_tangaza($self);

    }

}


######################################################################

#sub pre_server_close_hook {
#    my $self = shift;
#    &Nokia::Common::Tools::pre_server_close_hook ($self);
#}

=head2 place_call_tangaza

Places a call to the phone number in `$self->{user}->{outgoing_phone}`

=cut
sub place_call_tangaza {
    my ($self) = @_;

    my $phone = $self->{user}->{outgoing_phone};

    my $call_content = '';
    my $call_origin = $self->{origin};
    my $call_ext = $self->{callout_ext};

    if ($call_origin eq 'us') {
	$call_content = 
	    "Channel: IAX2/jnctn_out/$phone\n".
	    "CallerID: $call_ext\n";
    } else {
	$call_content = 
	    "Channel: SIP/nora01/1\n".
	    "CallerID: $phone\n";
    }

    $call_content .= 
	"Context: jnctn-callback-tangaza\n".
	"Extension: $call_ext\n".
	"Setvar: OUTBOUNDID=$self->{callerid}\n".
	"Setvar: ORIGIN=$call_origin\n".
	"WaitTime: 15\n";
    
    $self->log (4, "content $call_content");
    
    #print STDERR ("2 content $call_content");
    
    &place_call ($call_content);
    
}

=head1 AUTHORS

Billy Odero, Jonathan Ledlie

Copyright (C) 2010 Nokia Corporation.

=cut

1;

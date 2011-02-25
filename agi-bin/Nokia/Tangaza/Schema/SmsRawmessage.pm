package Nokia::Tangaza::Schema::SmsRawmessage;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("sms_rawmessage");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "phone",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 360,
  },
  "timestamp",
  { data_type => "DATE", default_value => undef, is_nullable => 0, size => 10 },
  "text",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 4608,
  },
);
__PACKAGE__->set_primary_key("id");


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-02-25 09:53:25
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:pjzcXdmPaG+HPX+zmRknUQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

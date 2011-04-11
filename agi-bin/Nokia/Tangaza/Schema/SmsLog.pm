package Nokia::Tangaza::Schema::SmsLog;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("sms_log");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "sender",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 60,
  },
  "text",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 600,
  },
  "timestamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
);
__PACKAGE__->set_primary_key("id");


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:OtsicokSP82PLk2MsfmL6w


# You can replace this text with custom content, and it will be preserved on regeneration
1;

package Nokia::Tangaza::Schema::SubMessages;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("sub_messages");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "message_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "timestamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "dst_user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "heard",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "flagged",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "channel",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "channel",
  "Nokia::Tangaza::Schema::Vikundi",
  { id => "channel" },
);
__PACKAGE__->belongs_to(
  "dst_user_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "dst_user_id" },
);
__PACKAGE__->belongs_to(
  "message_id",
  "Nokia::Tangaza::Schema::PubMessages",
  { id => "message_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:Y55vdhSQwpOhEcdmm1bjgg


# You can replace this text with custom content, and it will be preserved on regeneration
1;

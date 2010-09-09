package Nokia::Tangaza::Schema::SubMessages;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("sub_messages");
__PACKAGE__->add_columns(
  "sub_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "message_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "timestamp",
  {
    data_type => "TIMESTAMP",
    default_value => "CURRENT_TIMESTAMP",
    is_nullable => 0,
    size => 14,
  },
  "dst_user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "heard",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
  "flagged",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
  "channel",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
);
__PACKAGE__->set_primary_key("sub_id");
__PACKAGE__->belongs_to(
  "message_id",
  "Nokia::Tangaza::Schema::PubMessages",
  { pub_id => "message_id" },
);
__PACKAGE__->belongs_to(
  "dst_user_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "dst_user_id" },
);
__PACKAGE__->belongs_to(
  "channel",
  "Nokia::Tangaza::Schema::Groups",
  { group_id => "channel" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:EGFl+0vBHXFPkXgNiKGMXQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

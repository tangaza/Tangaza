package Nokia::Tangaza::Schema::PubMessages;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("pub_messages");
__PACKAGE__->add_columns(
  "pub_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "timestamp",
  {
    data_type => "TIMESTAMP",
    default_value => "CURRENT_TIMESTAMP",
    is_nullable => 0,
    size => 14,
  },
  "src_user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "channel",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "filename",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 32,
  },
  "text",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 1,
    size => 256,
  },
);
__PACKAGE__->set_primary_key("pub_id");
__PACKAGE__->add_unique_constraint("filename", ["filename"]);
__PACKAGE__->belongs_to(
  "src_user_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "src_user_id" },
);
__PACKAGE__->belongs_to(
  "channel",
  "Nokia::Tangaza::Schema::Groups",
  { group_id => "channel" },
);
__PACKAGE__->has_many(
  "sub_messages",
  "Nokia::Tangaza::Schema::SubMessages",
  { "foreign.message_id" => "self.pub_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:wgbUfOtZyYzHNRrd0MdTLA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

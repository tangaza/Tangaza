package Nokia::Tangaza::Schema::PubMessages;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("pub_messages");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "timestamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "src_user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "channel",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "filename",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 96,
  },
  "text",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 768,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("filename", ["filename"]);
__PACKAGE__->belongs_to(
  "channel",
  "Nokia::Tangaza::Schema::Vikundi",
  { id => "channel" },
);
__PACKAGE__->belongs_to(
  "src_user_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "src_user_id" },
);
__PACKAGE__->has_many(
  "sub_messages",
  "Nokia::Tangaza::Schema::SubMessages",
  { "foreign.message_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:yaTHlR5PRbzmeTcgrvyNtA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

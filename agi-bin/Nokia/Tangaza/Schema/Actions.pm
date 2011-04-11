package Nokia::Tangaza::Schema::Actions;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("actions");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "action_desc",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 270,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->has_many(
  "admin_group_histories",
  "Nokia::Tangaza::Schema::AdminGroupHistory",
  { "foreign.action_id" => "self.id" },
);
__PACKAGE__->has_many(
  "user_group_histories",
  "Nokia::Tangaza::Schema::UserGroupHistory",
  { "foreign.action_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:+AJtEaUYYrjTgim2PBRZ0w


# You can replace this text with custom content, and it will be preserved on regeneration
1;

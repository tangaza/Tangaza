package Nokia::Tangaza::Schema::AuthUserGroups;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("auth_user_groups");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("user_id", ["user_id", "group_id"]);
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::AuthGroup",
  { id => "group_id" },
);
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::AuthUser",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-02-25 09:53:25
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:5QE+DvH5JRTB5V0sNT4TZw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

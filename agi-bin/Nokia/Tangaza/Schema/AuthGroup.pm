package Nokia::Tangaza::Schema::AuthGroup;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("auth_group");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 80,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("name", ["name"]);
__PACKAGE__->has_many(
  "auth_group_permissions",
  "Nokia::Tangaza::Schema::AuthGroupPermissions",
  { "foreign.group_id" => "self.id" },
);
__PACKAGE__->has_many(
  "auth_user_groups",
  "Nokia::Tangaza::Schema::AuthUserGroups",
  { "foreign.group_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:JS8KMm5IT2bnLVx/vclbmw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

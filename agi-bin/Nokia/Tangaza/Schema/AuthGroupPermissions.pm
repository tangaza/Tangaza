package Nokia::Tangaza::Schema::AuthGroupPermissions;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("auth_group_permissions");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "permission_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("group_id", ["group_id", "permission_id"]);
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::AuthGroup",
  { id => "group_id" },
);
__PACKAGE__->belongs_to(
  "permission_id",
  "Nokia::Tangaza::Schema::AuthPermission",
  { id => "permission_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:6KAMGtuCnET3DX2yj6KSGg


# You can replace this text with custom content, and it will be preserved on regeneration
1;

package Nokia::Tangaza::Schema::AuthPermission;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("auth_permission");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 50,
  },
  "content_type_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "codename",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 100,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("content_type_id", ["content_type_id", "codename"]);
__PACKAGE__->has_many(
  "auth_group_permissions",
  "Nokia::Tangaza::Schema::AuthGroupPermissions",
  { "foreign.permission_id" => "self.id" },
);
__PACKAGE__->belongs_to(
  "content_type_id",
  "Nokia::Tangaza::Schema::DjangoContentType",
  { id => "content_type_id" },
);
__PACKAGE__->has_many(
  "auth_user_user_permissions",
  "Nokia::Tangaza::Schema::AuthUserUserPermissions",
  { "foreign.permission_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:D+SsM+4oaJFmEvx3k5y6QA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

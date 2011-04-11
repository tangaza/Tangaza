package Nokia::Tangaza::Schema::AuthUser;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("auth_user");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "username",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 30,
  },
  "first_name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 30,
  },
  "last_name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 30,
  },
  "email",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 75,
  },
  "password",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 128,
  },
  "is_staff",
  { data_type => "TINYINT", default_value => undef, is_nullable => 0, size => 1 },
  "is_active",
  { data_type => "TINYINT", default_value => undef, is_nullable => 0, size => 1 },
  "is_superuser",
  { data_type => "TINYINT", default_value => undef, is_nullable => 0, size => 1 },
  "last_login",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "date_joined",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("username", ["username"]);
__PACKAGE__->has_many(
  "auth_messages",
  "Nokia::Tangaza::Schema::AuthMessage",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "auth_user_groups",
  "Nokia::Tangaza::Schema::AuthUserGroups",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "auth_user_user_permissions",
  "Nokia::Tangaza::Schema::AuthUserUserPermissions",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "django_admin_logs",
  "Nokia::Tangaza::Schema::DjangoAdminLog",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "organizations",
  "Nokia::Tangaza::Schema::Organization",
  { "foreign.org_admin_id" => "self.id" },
);
__PACKAGE__->has_many(
  "watumiajis",
  "Nokia::Tangaza::Schema::Watumiaji",
  { "foreign.user_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:nPWAKn6L1yJvX0c9s0tQuA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

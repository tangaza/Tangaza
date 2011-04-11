package Nokia::Tangaza::Schema::DjangoAdminLog;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("django_admin_log");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "action_time",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "content_type_id",
  { data_type => "INT", default_value => undef, is_nullable => 1, size => 11 },
  "object_id",
  {
    data_type => "LONGTEXT",
    default_value => undef,
    is_nullable => 1,
    size => 4294967295,
  },
  "object_repr",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 200,
  },
  "action_flag",
  {
    data_type => "SMALLINT",
    default_value => undef,
    is_nullable => 0,
    size => 5,
  },
  "change_message",
  {
    data_type => "LONGTEXT",
    default_value => undef,
    is_nullable => 0,
    size => 4294967295,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "content_type_id",
  "Nokia::Tangaza::Schema::DjangoContentType",
  { id => "content_type_id" },
);
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::AuthUser",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:mcl1PttVviKSdH3YWvSzpQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

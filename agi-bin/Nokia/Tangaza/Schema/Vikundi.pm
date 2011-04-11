package Nokia::Tangaza::Schema::Vikundi;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("vikundi");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 180,
  },
  "group_name_file",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 96,
  },
  "group_type",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 7 },
  "is_active",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "org_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("group_name", ["group_name", "org_id"]);
__PACKAGE__->has_many(
  "admin_group_histories",
  "Nokia::Tangaza::Schema::AdminGroupHistory",
  { "foreign.group_id" => "self.id" },
);
__PACKAGE__->has_many(
  "group_admins",
  "Nokia::Tangaza::Schema::GroupAdmin",
  { "foreign.group_id" => "self.id" },
);
__PACKAGE__->has_many(
  "invitations",
  "Nokia::Tangaza::Schema::Invitations",
  { "foreign.group_id" => "self.id" },
);
__PACKAGE__->has_many(
  "pub_messages",
  "Nokia::Tangaza::Schema::PubMessages",
  { "foreign.channel" => "self.id" },
);
__PACKAGE__->has_many(
  "sub_messages",
  "Nokia::Tangaza::Schema::SubMessages",
  { "foreign.channel" => "self.id" },
);
__PACKAGE__->has_many(
  "user_group_histories",
  "Nokia::Tangaza::Schema::UserGroupHistory",
  { "foreign.group_id" => "self.id" },
);
__PACKAGE__->has_many(
  "user_groups",
  "Nokia::Tangaza::Schema::UserGroups",
  { "foreign.group_id" => "self.id" },
);
__PACKAGE__->belongs_to(
  "org_id",
  "Nokia::Tangaza::Schema::Organization",
  { id => "org_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:vp67BLanMLFGL5QPCxFdrw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

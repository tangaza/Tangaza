package Nokia::Tangaza::Schema::Watumiaji;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("watumiaji");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_pin",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 1,
    size => 18,
  },
  "status",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 33,
  },
  "place_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "level",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 24,
  },
  "callback_limit",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "invitations_remaining",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "language_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "name_file",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 96,
  },
  "name_text",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 255,
  },
  "create_stamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "modify_stamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "notify_stamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 1,
    size => 19,
  },
  "notify_period",
  { data_type => "TIME", default_value => undef, is_nullable => 0, size => 8 },
  "dirty",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "notify_status",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "accepted_terms",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "dirty_time",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 1,
    size => 19,
  },
  "notify_time",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 1,
    size => 19,
  },
  "calling_time",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 1,
    size => 19,
  },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 1, size => 11 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("user_id", ["user_id"]);
__PACKAGE__->has_many(
  "admin_group_history_user_dst_ids",
  "Nokia::Tangaza::Schema::AdminGroupHistory",
  { "foreign.user_dst_id" => "self.id" },
);
__PACKAGE__->has_many(
  "admin_group_history_user_src_ids",
  "Nokia::Tangaza::Schema::AdminGroupHistory",
  { "foreign.user_src_id" => "self.id" },
);
__PACKAGE__->has_many(
  "calls",
  "Nokia::Tangaza::Schema::Calls",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "group_admins",
  "Nokia::Tangaza::Schema::GroupAdmin",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "invitations_invitation_from_ids",
  "Nokia::Tangaza::Schema::Invitations",
  { "foreign.invitation_from_id" => "self.id" },
);
__PACKAGE__->has_many(
  "invitations_invitation_to_ids",
  "Nokia::Tangaza::Schema::Invitations",
  { "foreign.invitation_to_id" => "self.id" },
);
__PACKAGE__->has_many(
  "pub_messages",
  "Nokia::Tangaza::Schema::PubMessages",
  { "foreign.src_user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "sub_messages",
  "Nokia::Tangaza::Schema::SubMessages",
  { "foreign.dst_user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "terms_and_privacies",
  "Nokia::Tangaza::Schema::TermsAndPrivacy",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "user_group_histories",
  "Nokia::Tangaza::Schema::UserGroupHistory",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "user_groups",
  "Nokia::Tangaza::Schema::UserGroups",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->has_many(
  "user_phones",
  "Nokia::Tangaza::Schema::UserPhones",
  { "foreign.user_id" => "self.id" },
);
__PACKAGE__->belongs_to(
  "language_id",
  "Nokia::Tangaza::Schema::Languages",
  { id => "language_id" },
);
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::AuthUser",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:jeune/USleXxPxOI7SLzgw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

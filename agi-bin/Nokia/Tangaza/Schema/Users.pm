package Nokia::Tangaza::Schema::Users;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("users");
__PACKAGE__->add_columns(
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "user_pin",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 1, size => 6 },
  "status",
  { data_type => "ENUM", default_value => "good", is_nullable => 0, size => 11 },
  "place_id",
  { data_type => "INT", default_value => 1, is_nullable => 0, size => 10 },
  "level",
  {
    data_type => "ENUM",
    default_value => "advanced",
    is_nullable => 0,
    size => 8,
  },
  "callback_limit",
  { data_type => "INT", default_value => 60, is_nullable => 0, size => 10 },
  "invitations_remaining",
  { data_type => "INT", default_value => 100, is_nullable => 0, size => 10 },
  "language_id",
  { data_type => "TINYINT", default_value => 1, is_nullable => 0, size => 3 },
  "name_file",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 1,
    size => 32,
  },
  "name_text",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 1,
    size => 128,
  },
  "create_stamp",
  {
    data_type => "TIMESTAMP",
    default_value => "CURRENT_TIMESTAMP",
    is_nullable => 0,
    size => 14,
  },
  "modify_stamp",
  {
    data_type => "TIMESTAMP",
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
    size => 14,
  },
  "notify_stamp",
  {
    data_type => "TIMESTAMP",
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
    size => 14,
  },
  "notify_period",
  {
    data_type => "TIME",
    default_value => "24:00:00",
    is_nullable => 0,
    size => 8,
  },
  "dirty",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
  "notify_status",
  { data_type => "ENUM", default_value => "on", is_nullable => 0, size => 3 },
  "accepted_terms",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
  "dirty_time",
  {
    data_type => "TIMESTAMP",
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
    size => 14,
  },
  "notify_time",
  {
    data_type => "TIMESTAMP",
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
    size => 14,
  },
  "calling_time",
  {
    data_type => "TIMESTAMP",
    default_value => "0000-00-00 00:00:00",
    is_nullable => 0,
    size => 14,
  },
);
__PACKAGE__->set_primary_key("user_id");
__PACKAGE__->has_many(
  "admin_group_history_user_src_ids",
  "Nokia::Tangaza::Schema::AdminGroupHistory",
  { "foreign.user_src_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "admin_group_history_user_dst_ids",
  "Nokia::Tangaza::Schema::AdminGroupHistory",
  { "foreign.user_dst_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "calls",
  "Nokia::Tangaza::Schema::Calls",
  { "foreign.user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "group_admins",
  "Nokia::Tangaza::Schema::GroupAdmin",
  { "foreign.user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "invitations_invitation_to_ids",
  "Nokia::Tangaza::Schema::Invitations",
  { "foreign.invitation_to_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "invitations_invitation_from_ids",
  "Nokia::Tangaza::Schema::Invitations",
  { "foreign.invitation_from_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "pub_messages",
  "Nokia::Tangaza::Schema::PubMessages",
  { "foreign.src_user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "sub_messages",
  "Nokia::Tangaza::Schema::SubMessages",
  { "foreign.dst_user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "terms_and_privacies",
  "Nokia::Tangaza::Schema::TermsAndPrivacy",
  { "foreign.user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "user_group_histories",
  "Nokia::Tangaza::Schema::UserGroupHistory",
  { "foreign.user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "user_groups",
  "Nokia::Tangaza::Schema::UserGroups",
  { "foreign.user_id" => "self.user_id" },
);
__PACKAGE__->has_many(
  "user_phones",
  "Nokia::Tangaza::Schema::UserPhones",
  { "foreign.user_id" => "self.user_id" },
);
__PACKAGE__->belongs_to(
  "language_id",
  "Nokia::Tangaza::Schema::Languages",
  { language_id => "language_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:nCDUwVq4Da+bGYd5ePpAbw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

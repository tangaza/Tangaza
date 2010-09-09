package Nokia::Tangaza::Schema::Invitations;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("invitations");
__PACKAGE__->add_columns(
  "invitation_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "invitation_to_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "invitation_from_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "create_stamp",
  {
    data_type => "TIMESTAMP",
    default_value => "CURRENT_TIMESTAMP",
    is_nullable => 0,
    size => 14,
  },
  "completed",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
);
__PACKAGE__->set_primary_key("invitation_id");
__PACKAGE__->belongs_to(
  "invitation_to_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "invitation_to_id" },
);
__PACKAGE__->belongs_to(
  "invitation_from_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "invitation_from_id" },
);
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::Groups",
  { group_id => "group_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:gQd2ekQsZfzCqPtxoWZ9HA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

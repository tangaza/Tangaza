package Nokia::Tangaza::Schema::GroupAdmin;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("group_admin");
__PACKAGE__->add_columns(
  "group_admin_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
);
__PACKAGE__->set_primary_key("group_admin_id");
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "user_id" },
);
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::Groups",
  { group_id => "group_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:P0+QqBqs8FPmuhYzgRdELA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

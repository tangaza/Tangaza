package Nokia::Tangaza::Schema::UserGroups;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("user_groups");
__PACKAGE__->add_columns(
  "user_group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "is_quiet",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
  "slot",
  {
    data_type => "SMALLINT",
    default_value => undef,
    is_nullable => 0,
    size => 6,
  },
);
__PACKAGE__->set_primary_key("user_group_id");
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
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:Nq8jIKN0JmPvzGvTuCCOHQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

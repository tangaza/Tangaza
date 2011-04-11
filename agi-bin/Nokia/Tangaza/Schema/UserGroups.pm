package Nokia::Tangaza::Schema::UserGroups;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("user_groups");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "is_quiet",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
  "slot",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("user_id_2", ["user_id", "group_id"]);
__PACKAGE__->add_unique_constraint("user_id", ["user_id", "slot"]);
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::Vikundi",
  { id => "group_id" },
);
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:xiV+Rwr3/vri9tAptdZ/Kg


# You can replace this text with custom content, and it will be preserved on regeneration
1;

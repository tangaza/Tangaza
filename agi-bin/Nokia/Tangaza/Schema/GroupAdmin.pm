package Nokia::Tangaza::Schema::GroupAdmin;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("group_admin");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("user_id", ["user_id", "group_id"]);
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
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:s3YRDbplCLYfTy98mQxapw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

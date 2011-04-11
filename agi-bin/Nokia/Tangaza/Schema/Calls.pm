package Nokia::Tangaza::Schema::Calls;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("calls");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "timestamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "seconds",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "cbstate",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 30,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:0rEVzGIxD6PRako6wrOG2w


# You can replace this text with custom content, and it will be preserved on regeneration
1;

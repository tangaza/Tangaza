package Nokia::Tangaza::Schema::AdminGroupHistory;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("admin_group_history");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "action_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_src_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_dst_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "timestamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "action_id",
  "Nokia::Tangaza::Schema::Actions",
  { id => "action_id" },
);
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::Vikundi",
  { id => "group_id" },
);
__PACKAGE__->belongs_to(
  "user_dst_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "user_dst_id" },
);
__PACKAGE__->belongs_to(
  "user_src_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "user_src_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:bNAQZaGWucnYwMMOyqZVNA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

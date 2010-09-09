package Nokia::Tangaza::Schema::AdminGroupHistory;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("admin_group_history");
__PACKAGE__->add_columns(
  "admin_group_hist_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "action_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "user_src_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "user_dst_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "timestamp",
  {
    data_type => "TIMESTAMP",
    default_value => "CURRENT_TIMESTAMP",
    is_nullable => 0,
    size => 14,
  },
);
__PACKAGE__->set_primary_key("admin_group_hist_id");
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::Groups",
  { group_id => "group_id" },
);
__PACKAGE__->belongs_to(
  "action_id",
  "Nokia::Tangaza::Schema::Actions",
  { action_id => "action_id" },
);
__PACKAGE__->belongs_to(
  "user_src_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "user_src_id" },
);
__PACKAGE__->belongs_to(
  "user_dst_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "user_dst_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:z4XVTNggdS/4ndENLk7duA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

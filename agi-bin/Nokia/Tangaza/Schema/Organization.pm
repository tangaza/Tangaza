package Nokia::Tangaza::Schema::Organization;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("organization");
__PACKAGE__->add_columns(
  "org_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "org_name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 90,
  },
  "org_admin_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
);
__PACKAGE__->set_primary_key("org_id");
__PACKAGE__->has_many(
  "groups",
  "Nokia::Tangaza::Schema::Groups",
  { "foreign.org_id" => "self.org_id" },
);
__PACKAGE__->belongs_to(
  "org_admin_id",
  "Nokia::Tangaza::Schema::AuthUser",
  { id => "org_admin_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2010-12-20 11:06:11
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:I7ggo1D6dwi82cY9cwbOBQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

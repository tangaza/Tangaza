package Nokia::Tangaza::Schema::Organization;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("organization");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "org_name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 210,
  },
  "org_admin_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "toll_free_number",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 21,
  },
  "is_active",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 1, size => 9 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "org_admin_id",
  "Nokia::Tangaza::Schema::AuthUser",
  { id => "org_admin_id" },
);
__PACKAGE__->has_many(
  "vikundis",
  "Nokia::Tangaza::Schema::Vikundi",
  { "foreign.org_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:TJOCwpF9VFJ2yfRYDiyHVw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

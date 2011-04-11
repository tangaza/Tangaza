package Nokia::Tangaza::Schema::Dlr;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("dlr");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "smsc",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 120,
  },
  "ts",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 120,
  },
  "dest",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 120,
  },
  "src",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 120,
  },
  "service",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 120,
  },
  "url",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 765,
  },
  "mask",
  { data_type => "INT", default_value => undef, is_nullable => 1, size => 11 },
  "status",
  { data_type => "INT", default_value => undef, is_nullable => 1, size => 11 },
  "boxc",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 120,
  },
);
__PACKAGE__->set_primary_key("id");


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:tjmQi9EdiU30V6F8c1n9iA


# You can replace this text with custom content, and it will be preserved on regeneration
1;

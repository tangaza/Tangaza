package Nokia::Tangaza::Schema::Countries;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("countries");
__PACKAGE__->add_columns(
  "country_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "country_code",
  {
    data_type => "SMALLINT",
    default_value => undef,
    is_nullable => 0,
    size => 6,
  },
  "country_name",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
);
__PACKAGE__->set_primary_key("country_id");
__PACKAGE__->has_many(
  "user_phones",
  "Nokia::Tangaza::Schema::UserPhones",
  { "foreign.country_id" => "self.country_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:Sh4ZA5vi9u2xUgzImCMxKw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

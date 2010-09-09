package Nokia::Tangaza::Schema::UserPhones;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("user_phones");
__PACKAGE__->add_columns(
  "phone_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "country_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "phone_number",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 20,
  },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "is_primary",
  { data_type => "ENUM", default_value => "no", is_nullable => 0, size => 3 },
);
__PACKAGE__->set_primary_key("phone_id");
__PACKAGE__->add_unique_constraint("phone_number", ["phone_number"]);
__PACKAGE__->belongs_to(
  "country_id",
  "Nokia::Tangaza::Schema::Countries",
  { country_id => "country_id" },
);
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:fpu7fBs/ju5nB0KR3Skq6w


# You can replace this text with custom content, and it will be preserved on regeneration
1;

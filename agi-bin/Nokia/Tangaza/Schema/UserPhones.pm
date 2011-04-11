package Nokia::Tangaza::Schema::UserPhones;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("user_phones");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "country_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "phone_number",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 60,
  },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "is_primary",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 3 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->add_unique_constraint("phone_number", ["phone_number"]);
__PACKAGE__->belongs_to(
  "country_id",
  "Nokia::Tangaza::Schema::Countries",
  { id => "country_id" },
);
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:hXKbD3l6RMNLdAX9QULsbQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

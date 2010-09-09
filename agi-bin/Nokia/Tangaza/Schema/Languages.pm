package Nokia::Tangaza::Schema::Languages;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("languages");
__PACKAGE__->add_columns(
  "language_id",
  { data_type => "TINYINT", default_value => undef, is_nullable => 0, size => 3 },
  "name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 20,
  },
);
__PACKAGE__->set_primary_key("language_id");
__PACKAGE__->has_many(
  "users",
  "Nokia::Tangaza::Schema::Users",
  { "foreign.language_id" => "self.language_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:+wdbcHruXb1zfE+IEodW8g


# You can replace this text with custom content, and it will be preserved on regeneration
1;

package Nokia::Tangaza::Schema::Languages;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("languages");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "name",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 60,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->has_many(
  "watumiajis",
  "Nokia::Tangaza::Schema::Watumiaji",
  { "foreign.language_id" => "self.id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:JsYu6XcLQkLb2np64DvOSQ


# You can replace this text with custom content, and it will be preserved on regeneration
1;

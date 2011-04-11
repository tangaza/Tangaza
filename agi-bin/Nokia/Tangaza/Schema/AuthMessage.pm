package Nokia::Tangaza::Schema::AuthMessage;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("auth_message");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "message",
  {
    data_type => "LONGTEXT",
    default_value => undef,
    is_nullable => 0,
    size => 4294967295,
  },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::AuthUser",
  { id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:YqpXhMEgGJW8Ay0Fmgeb8A


# You can replace this text with custom content, and it will be preserved on regeneration
1;

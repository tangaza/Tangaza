package Nokia::Tangaza::Schema::Calls;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("calls");
__PACKAGE__->add_columns(
  "call_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "user_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "timestamp",
  {
    data_type => "TIMESTAMP",
    default_value => "CURRENT_TIMESTAMP",
    is_nullable => 0,
    size => 14,
  },
  "seconds",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 10 },
  "cbstate",
  { data_type => "ENUM", default_value => undef, is_nullable => 0, size => 10 },
);
__PACKAGE__->set_primary_key("call_id");
__PACKAGE__->belongs_to(
  "user_id",
  "Nokia::Tangaza::Schema::Users",
  { user_id => "user_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04005 @ 2009-11-18 14:16:53
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:zfS87m0p3VbrICEj/4FhDw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

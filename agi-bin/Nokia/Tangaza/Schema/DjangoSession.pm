package Nokia::Tangaza::Schema::DjangoSession;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("django_session");
__PACKAGE__->add_columns(
  "session_key",
  {
    data_type => "VARCHAR",
    default_value => undef,
    is_nullable => 0,
    size => 40,
  },
  "session_data",
  {
    data_type => "LONGTEXT",
    default_value => undef,
    is_nullable => 0,
    size => 4294967295,
  },
  "expire_date",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
);
__PACKAGE__->set_primary_key("session_key");


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:NvcYpi1iVkEg+NmCLUdfeg


# You can replace this text with custom content, and it will be preserved on regeneration
1;

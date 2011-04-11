package Nokia::Tangaza::Schema::Invitations;

use strict;
use warnings;

use base 'DBIx::Class';

__PACKAGE__->load_components("Core");
__PACKAGE__->table("invitations");
__PACKAGE__->add_columns(
  "id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "invitation_to_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "invitation_from_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "group_id",
  { data_type => "INT", default_value => undef, is_nullable => 0, size => 11 },
  "create_stamp",
  {
    data_type => "DATETIME",
    default_value => undef,
    is_nullable => 0,
    size => 19,
  },
  "completed",
  { data_type => "VARCHAR", default_value => undef, is_nullable => 0, size => 9 },
);
__PACKAGE__->set_primary_key("id");
__PACKAGE__->belongs_to(
  "group_id",
  "Nokia::Tangaza::Schema::Vikundi",
  { id => "group_id" },
);
__PACKAGE__->belongs_to(
  "invitation_from_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "invitation_from_id" },
);
__PACKAGE__->belongs_to(
  "invitation_to_id",
  "Nokia::Tangaza::Schema::Watumiaji",
  { id => "invitation_to_id" },
);


# Created by DBIx::Class::Schema::Loader v0.04006 @ 2011-04-11 18:46:41
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:bl4iQIA0bk1U6n8mYYq3Hw


# You can replace this text with custom content, and it will be preserved on regeneration
1;

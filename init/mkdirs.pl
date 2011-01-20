#!/usr/bin/perl

my $today = time;

for (my $day = 0; $day < (365*5); $day++) {

  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =
      localtime($today);
  $year += 1900;
  $mon++;

  my $year_dir = sprintf ("$year");

  if (! -e $year_dir) {
      mkdir $year_dir or die ("Cannot mkdir $year_dir");
  }

  my $year_mon_dir = sprintf ("$year/%02d", $mon);

  if (! -e $year_mon_dir) {
      mkdir $year_mon_dir or die ("Cannot mkdir $year_mon_dir");
  }

  my $year_mon_day_dir = sprintf ("$year/%02d/%02d", $mon, $mday);

  if (! -e $year_mon_day_dir) {
      mkdir $year_mon_day_dir or die ("Cannot mkdir $year_mon_day_dir");
  }

  $today += (3600*24);

  #mkdir "$year_month";
  #print "$stamp\n";
}


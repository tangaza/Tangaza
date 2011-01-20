#! /usr/bin/perl                                                                                                                                 
sub check_exists {
    my $mod = shift;

    eval ("use $mod");
    if ($@) {
        print "Missing";
        return 0;
    }
    else {
        return 1;
    }
}

check_exists @ARGV;

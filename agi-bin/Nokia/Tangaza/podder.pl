use strict;
use Pod::Html::HtmlTree;
use Data::Dumper;
use File::Basename;
use File::Spec::Functions qw(rel2abs);

my $p = Pod::Html::HtmlTree->new;
$p->indir    ( dirname(rel2abs($0)) );
$p->outdir   ( dirname(rel2abs($0)).'/docs/' );

#$p->mask_dir ( 0777 );    # default is 0775
#$p->mask_html( 0777 ); # default is 0664
$p->pod_exts ( [ 'pm' , 'pod' ] ); # default is [pm,pod,cgi,pl]
 # * you can use all arguments same as Pod::Html has except infile and outfile.
 # * use * 0 * for argument value which does not require to have value.
$p->args({
    css =>'../css/style.css',
    index => 0,
	 });

my $files = $p->create;
print Dumper ( $files ); 

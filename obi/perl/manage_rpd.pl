#!/usr/bin/perl

# =======================================================================
# Developed by Stewart Bryson @ Rittman Mead
# Absolutely no warranty, use at your own risk
# Please include this header in any copy or reuse of the script you make
# =======================================================================

#---- Header -----------------------------------------------------------------------------------------

# module references
use Getopt::Long;
use File::Basename;
use Pod::Usage;
use File::stat;
use Cwd;
use File::Spec;
use Path::Class;

# configurations
Getopt::Long::Configure ("bundling");

# pragmas
use strict;
use warnings;

# get program name
my $basename = basename($0);

# set the usage in a variable
my $usage	= qq{
Usage: $basename [OPTIONS]

OPTIONS:

-i              PARAMETER: The input RPD repository. This can be a binary RPD repostory file, or an MDS XML repository directory.
                NOTE: if -i is binary repository file instead of an MDS XML repository directory, then -o is ignored.
                                
-p              PARAMETER: The password for the MDS XML repository
                DEFAULT: Admin123

-o              PARAMETER: The binary RPD repository file to generate.
                DEFAULT: a filename matching the directory name specified in -i with a .rpd extension appended to it

-d              OPTION: Deploy the binary RPD repository file to the BI Server

-b              OPTION: Restart the BI Server

-a              OPTION: Restart Presentation Services

-r              OPTION: Remove the binary RPD file after deployment

-u              PARAMTER: The Weblogic administrative user
                DEFAULT: weblogic                               

-w              PARAMETER: The password for the user specified in -u
                DEFAULT: welcome1

-l              PARAMTER: Weblogic Admin Server URL
                DEFAULT: t3://localhost:7001

-v              OPTION: Provide verbose output

-e              OPTION: Debug mode

};


# create a hash to store options from the command-line
my $options = {};

# collect options from the command-line
# handle the usage as well
unless (
        GetOptions( 
                   $options,
                   "i:s",
                   "p:s",
                   "o:s",
                   "d!",
                   "b!",
		   "a!",
                   "u:s",
                   "w:s",
		   "l:s",
		   "r!",
		   "v!",
		   "e!",
                   "help|?!"
                  )
       ) {
  pod2usage($usage);
}

pod2usage($usage) if defined($options->{help});

#---- Build variables -------------------------------------------------------------------------------------
# get environment out of the way
my $sfile = file( File::Spec->rel2abs(__FILE__) );
my $dirname  = $sfile->parent;
my $updir = $dirname->parent;

# capture the input
my $input;
my $itype;
if ($options->{i}) {

  # get the absolute path of the $input
  $input = File::Spec->rel2abs($options->{i});
  print ("input file: $input\n") if $options->{e};

  # check to see if the -i option points to a directory or a file
  if (-d $input) {
    $itype = 'd';
  } elsif (-e $input) {
    $itype = 'f';
  } else {
    die "The -i option does not point to a valid file or directory\n";
  }

  print "itype: $itype\n" if $options->{e};

}

# capture the oupput
my $output = $options->{o};

my $wlstbin = q{wlst.cmd};

my $opmnctl = q{opmnctl};

my $wlspass = $options->{w}?$options->{w}:q{welcome1};

my $wlsuser = $options->{u}?$options->{u}:q{weblogic};

my $wlsurl = $options->{wlsurl}?$options->{wlsurl}:q{t3://localhost:7001};

my $pass = $options->{p}?$options->{p}:q{Admin123};

if ($options->{e} and $options->{o}) {
  print ("output: $output\n");
}

if ($options->{e}) {
  print ("wlstbin: $wlstbin\nopmnctl: $opmnctl\nbasename: $basename\ndirectory: $dirname\nparent directory: $updir\n");
}

#---- Main Body -------------------------------------------------------------------------------------

# generate the RPD
# only do this if INPUT points to a directory
# otherwise, we have a binary RPD file already
if ($input && $itype eq "d") {
  $output = GenerateRpd( $input,$output ) unless $options->{e};
}

# deploy the RPD
# only deploy the rpd if -d is supplied
if ($options->{d}) {
  DeployRpd( $output?$output:$input ) unless $options->{e};
}

# Restart the BI Server
# only restart if -b is specified
if ($options->{b}) {
  RestartBI( ) unless $options->{e};
}

# Restart Presentation Services
# only restart if -b is specified
if ($options->{a}) {
  RestartPS( ) unless $options->{e};
}

if ($options->{r} && $options->{d}) {
  
  unlink $output;
  
}

#---- Subroutines -------------------------------------------------------------------------------------

sub GenerateRpd {

  #print "GenerateRpd entered...\n";

  my ($input, $output)	= @_;

  die "-d option does not point to a directory" unless $itype eq 'd';

  $output = $output?$output:$input . '.rpd';
  
  # the name of the results file to use
  my $results = $input . '.txt';

  # now use validaterpd to push this to a valid RPD file
  # I use validaterpd instead of biserverxmlexec because biserverxmlexec doesn't work correctly
  # My testing generated a bug with Oracle Support for this
  my $stmt = qq[validaterpd -P $pass -D "$input" -O "$results" -F "$output"];
  print "Executing: $stmt\n" if $options->{v};

  # get the absolute path
  $output = File::Spec->rel2abs($output);
 
  my $stdout = qx[$stmt];
  print "$stdout\n" if $options->{v};
  
  return $output;
  
}

sub DeployRpd {

  #print "DeployRpd entered...\n";

  my ( $rpdfile )	= @_;
  #print "$rpdfile\n";
  
  my $deploy_py = File::Spec->catfile( $updir, 'wlst', 'deploy_rpd.py' );
  
  $rpdfile = File::Spec->rel2abs($rpdfile);

  my $stmt = qq{$wlstbin "$deploy_py" $wlsuser $wlspass $wlsurl "$rpdfile" $pass};
  print "Executing: $stmt\n" if $options->{v};
  
  my $stdout = qx[$stmt];
  print "$stdout\n" if $options->{v};

}

sub RestartBI {

  #print "RestartBI...\n";

  my $stmt = qq{$opmnctl restartproc process-type=OracleBIServerComponent};
  print "Executing: $stmt\n" if $options->{v};
  
  my $stdout = qx[$stmt];
  print "$stdout\n" if $options->{v};

}

sub RestartPS {

  #print "RestartPS...\n";

  my $stmt = qq{$opmnctl restartproc process-type=OracleBIPresentationServicesComponent};
  print "Executing: $stmt\n" if $options->{v};
  
  my $stdout = qx[$stmt];
  print "$stdout\n" if $options->{v};

}

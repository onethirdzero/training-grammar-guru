#!/usr/bin/env perl

# Copyright 2017 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

use strict;

my $folds = 5;  # Note: folds are zero-indexed.
my $max_fold = $folds - 1;
my $max_files = 128; # Arbitrary upper bound!

print "# Autogenerated file: do not modify!\n";

# Create declare the phony rules.
print ".PHONY: models mutations results\n";

sub model_filename {
    my ($dir, $fold) = @_;
    return "\$(MODEL_DIR)/\$(CORPUS)-$dir$fold.hdf5";
}

# Create a phony rule for models.
print "models:";
foreach my $fold (0 .. $max_fold) {
    foreach my $dir ('f', 'b') {
        print " @{[model_filename $dir, $fold]}"
    }
}
print "\n";

# Create rules for the trained models
foreach my $direction ('forwards', 'backwards') {
    my $dir = substr $direction, 0, 1;
    foreach my $fold (0 .. $max_fold) {
        print "@{[model_filename $dir, $fold]}: \$(VECTORS)\n";
        print "\tbin/train --$direction --fold $fold \$<\n";
    }
}

###
print "\n";
###

# Create a phony rule for mutations.
print "mutations:";
foreach my $fold (0 .. $max_fold) {
    print " \$(CORPUS)-mutations.$fold.sqlite3";
}
print "\n";

# Create rules for mutations.
foreach my $fold (0 .. $max_fold) {
    print "\$(CORPUS)-mutations.$fold.sqlite3:";
    print " @{[model_filename 'f', $fold]}";
    print " @{[model_filename 'b', $fold]}";
    print " \$(TEST_SET).$fold";
    print "\n";
    print "\tbin/mutate --limit $max_files $fold  \n";
}
print "\n";

# Create a rule for results
print "results.csv:";
foreach my $fold (0 .. $max_fold) {
    print " results.$fold.csv";
}
print "\n";
print "\t./concat-results.sh \$^ > \$@\n";

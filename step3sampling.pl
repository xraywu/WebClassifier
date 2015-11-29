open IN,"drugFeatureP.csv";
open TRAIN,">toTrain.csv";
open TEST,">toTest.csv";

my $header = <IN>;
print TRAIN $header;
print TEST $header;

my $P = 0.4;

while(<IN>){
	if(rand(1) < $P){ print TRAIN $_ }
	else { print TEST $_ }
}

close IN;
close TRAIN;
close TEST;
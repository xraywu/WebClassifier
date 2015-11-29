open IN,"drugFeature.txt";

my $headerLine = <IN>;
chomp $headerLine;
my @headers = split("\t",$headerLine);

open OUT,">drugFeatureP.csv";
print OUT $headers[0],",",$headers[1];

my @validIdx = (1);
for(my $i = 2; $i < @headers; $i++){
	if(!($headers[$i] =~ /^[\sA-Za-z0-9\.\(\):;,\"\'%\>\<\*\#\+-\[\]\\\/]*$/)){
		if($headers[$i] ne "。" && $headers[$i] ne "，" && $headers[$i] ne "？" && $headers[$i] ne "！" && 
			$headers[$i] ne "：" && $headers[$i] ne "；" && $headers[$i] ne "￥" && $headers[$i] ne "〉" &&
			 $headers[$i] ne "《" && $headers[$i] ne "〈" && $headers[$i] ne "》" && $headers[$i] ne "（"
			  && $headers[$i] ne "）" && $headers[$i] ne "、"){
			push(@validIdx, $i);
		}
	}
}

open FET,">featureVariables.txt";
for(my $i = 1; $i < @validIdx; $i++){
	print OUT ",v",$i;
	print FET "v",$i,"\t",$headers[$validIdx[$i]],"\n";
}
print OUT "\n";
close FET;


open DRUG,">drugList.txt";
my $lineNum = 1;
while(<IN>){
	chomp $_;
	my @fields = split("\t", $_);
	print OUT "d",$lineNum;
	print DRUG "d",$lineNum,"\t",$fields[0],"\n";
	foreach(@validIdx){ print OUT ",",$fields[$_] }
	print OUT "\n";
	$lineNum++;
}
close DRUG;
close IN;
close OUT;
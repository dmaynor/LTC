sub count_words {
    my ($input_file, $output_file) = @_;
    my %counts;

    open my $in, '<', $input_file or die $!;
    while (<$in>) {
        $counts{$_}++ for split;
    }
    close $in;

    open my $out, '>', $output_file or die $!;
    print $out "$_: $counts{$_}\n" for keys %counts;
    close $out;
}

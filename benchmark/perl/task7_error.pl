sub parse_int {
    my ($s) = @_;
    if ($s =~ /^-?\d+$/) {
        return { success => 1, value => int($s) };
    }
    return { success => 0, error => "Invalid integer format" };
}

sub double_evens {
    my @numbers = @_;
    return map { $_ * 2 } grep { $_ % 2 == 0 } @numbers;
}

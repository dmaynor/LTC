package Point;

sub new {
    my ($class, $x, $y) = @_;
    return bless { x => $x, y => $y }, $class;
}

sub distance_to {
    my ($self, $other) = @_;
    my $dx = $self->{x} - $other->{x};
    my $dy = $self->{y} - $other->{y};
    return sqrt($dx * $dx + $dy * $dy);
}

1;

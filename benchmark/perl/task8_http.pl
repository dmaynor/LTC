use LWP::Simple;

sub fetch_url {
    my ($url) = @_;
    my $content = get($url);
    if (defined $content) {
        return { success => 1, body => $content };
    }
    return { success => 0, error => "Failed to fetch URL" };
}

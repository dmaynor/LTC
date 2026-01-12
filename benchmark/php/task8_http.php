<?php
function fetch_url(string $url): array {
    $content = @file_get_contents($url);
    if ($content === false) {
        return ['success' => false, 'error' => 'Failed to fetch URL'];
    }
    return ['success' => true, 'body' => $content];
}

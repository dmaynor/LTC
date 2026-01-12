<?php
function parse_int(string $s): array {
    if (ctype_digit(ltrim($s, '-')) && strpos($s, '-') !== 1) {
        return ['success' => true, 'value' => (int)$s];
    }
    return ['success' => false, 'error' => 'Invalid integer format'];
}

<?php
function double_evens(array $numbers): array {
    return array_map(fn($n) => $n * 2, array_filter($numbers, fn($n) => $n % 2 == 0));
}

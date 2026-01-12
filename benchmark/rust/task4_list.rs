fn double_evens(numbers: &[i32]) -> Vec<i32> {
    numbers.iter().filter(|&n| n % 2 == 0).map(|n| n * 2).collect()
}

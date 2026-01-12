func doubleEvens(_ numbers: [Int]) -> [Int] {
    numbers.filter { $0 % 2 == 0 }.map { $0 * 2 }
}

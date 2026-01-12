List<int> doubleEvens(List<int> numbers) =>
    numbers.where((n) => n % 2 == 0).map((n) => n * 2).toList();

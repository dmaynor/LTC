using System.Linq;

List<int> DoubleEvens(List<int> numbers) =>
    numbers.Where(n => n % 2 == 0).Select(n => n * 2).ToList();

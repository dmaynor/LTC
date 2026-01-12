def double_evens(numbers)
  numbers.select { |n| n.even? }.map { |n| n * 2 }
end

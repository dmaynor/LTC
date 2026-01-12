function result = double_evens(numbers)
    evens = numbers(mod(numbers, 2) == 0);
    result = evens * 2;
end

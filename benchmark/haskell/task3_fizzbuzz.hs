main = mapM_ putStrLn [fizzbuzz n | n <- [1..100]]
  where
    fizzbuzz n
      | n `mod` 15 == 0 = "FizzBuzz"
      | n `mod` 3 == 0  = "Fizz"
      | n `mod` 5 == 0  = "Buzz"
      | otherwise       = show n

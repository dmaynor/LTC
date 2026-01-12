doubleEvens :: [Int] -> [Int]
doubleEvens = map (*2) . filter even

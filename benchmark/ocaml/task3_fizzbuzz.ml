for i = 1 to 100 do
  match (i mod 3, i mod 5) with
  | (0, 0) -> print_endline "FizzBuzz"
  | (0, _) -> print_endline "Fizz"
  | (_, 0) -> print_endline "Buzz"
  | _ -> print_endline (string_of_int i)
done

let parse_int s =
  match int_of_string_opt s with
  | Some n -> Ok n
  | None -> Error ("Invalid integer: " ^ s)

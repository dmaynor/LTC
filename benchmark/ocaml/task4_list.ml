let double_evens lst =
  lst |> List.filter (fun x -> x mod 2 = 0) |> List.map (fun x -> x * 2)

let count_words filename =
  let ic = open_in filename in
  let counts = Hashtbl.create 100 in
  try
    while true do
      let line = input_line ic in
      let words = String.split_on_char ' ' line in
      List.iter (fun w ->
        let w = String.lowercase_ascii w in
        if w <> "" then
          let n = try Hashtbl.find counts w with Not_found -> 0 in
          Hashtbl.replace counts w (n + 1)
      ) words
    done
  with End_of_file ->
    close_in ic;
    let oc = open_out "output.txt" in
    Hashtbl.iter (fun k v -> Printf.fprintf oc "%s: %d\n" k v) counts;
    close_out oc

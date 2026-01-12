let fetch_url url =
  let cmd = Printf.sprintf "curl -s '%s'" url in
  let ic = Unix.open_process_in cmd in
  let buf = Buffer.create 1024 in
  try
    while true do Buffer.add_channel buf ic 1 done; ""
  with End_of_file ->
    ignore (Unix.close_process_in ic);
    Buffer.contents buf

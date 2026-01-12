type point = { x : float; y : float }

let make_point x y = { x; y }

let distance_to p1 p2 =
  let dx = p2.x -. p1.x in
  let dy = p2.y -. p1.y in
  sqrt (dx *. dx +. dy *. dy)

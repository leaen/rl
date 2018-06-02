open Base__

type t = {
  x : int;
  y : int;
}

let make x y = { x = x; y = y; }

let get_x s = s.x

let get_y s = s.y

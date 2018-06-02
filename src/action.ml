open Base__

type t =
  | Up
  | Down
  | Left
  | Right

let action_space = [
  Up;
  Down;
  Left;
  Right;
]

let bound low high value =
  max low (min high value)

let move max_x max_y s a =
  let module S = State in
  match a with
  | Up -> S.make (S.get_x s) (bound 0 max_y (S.get_y s + 1))
  | Down -> S.make (S.get_x s) (bound 0 max_y (S.get_y s - 1))
  | Left -> S.make (bound 0 max_x (S.get_x s - 1)) (S.get_y s)
  | Right -> S.make (bound 0 max_x (S.get_x s + 1)) (S.get_y s)


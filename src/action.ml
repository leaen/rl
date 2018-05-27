open Base__
open Board

type action =
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

let move max_x max_y state a =
  match a with
  | Up -> Board.make_state state.x (bound 0 max_y (state.y + 1))
  | Down -> Board.make_state state.x (bound 0 max_y (state.y - 1))
  | Left -> Board.make_state (bound 0 max_x (state.x - 1)) state.y
  | Right -> Board.make_state (bound 0 max_x (state.x + 1)) state.y


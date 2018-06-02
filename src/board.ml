open Base__
open Stdio

let win_reward = 1000.0
let lose_reward = -1000.0
let survival_reward = -1.0

type cell = {
  terminal : bool;
  reward : float;
  solid : bool;
  value : string;
  starting : bool;
}

type t = {
  cells : cell list list;
}

let read_board fname =
  let s_to_cell s =
    match s with
    | "#" -> { starting = false; solid = true; terminal = false; reward = 0.0; value = "#"; }
    | "$" -> { starting = false; solid = false; terminal = true; reward = win_reward; value = "$"; }
    | "x" -> { starting = false; solid = false; terminal = true; reward = lose_reward; value = "x"; }
    | "s" -> { starting = true; solid = false; terminal = false; reward = survival_reward; value = "s"; }
    | " " -> { starting = false; solid = false; terminal = false; reward = survival_reward; value = " "; }
    | x -> { starting = false; solid = false; terminal = false; reward = 0.0; value = x } in

  let line_list_to_cells line =
    List.map line s_to_cell in

  let add_line_to_board board line =
    board @ [line_list_to_cells (String.split_on_chars ~on:[','] line)] in

  let cells = In_channel.fold_lines (In_channel.create fname) ~init:[] ~f:add_line_to_board in
  { cells = cells }

let get_states_with_property board ~f =
  let rec aux_row x y l acc =
    match l with
    | [] -> acc
    | hd :: tl when (f hd) -> aux_row (x + 1) y tl ((State.make x y) :: acc)
    | _ :: tl -> aux_row (x + 1) y tl acc in

  let rec aux y l acc =
    match l with
    | [] -> acc
    | hd :: tl -> aux (y + 1) tl ((aux_row 0 y hd []) @ acc) in

  aux 0 board.cells []

let get_starting_states board =
  get_states_with_property ~f:(fun x -> x.starting) board

let get_possible_states board =
  get_states_with_property board ~f:(fun x -> not x.solid)

let to_string b =
  let c = b.cells in
  let str_rows = List.map c ~f:(fun r -> String.concat ~sep:""  (List.map ~f:(fun c -> c.value) r)) in
  String.concat ~sep:"\n" str_rows

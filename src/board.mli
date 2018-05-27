open Base__

(** A board that holds the cells of the grid world *)
type t

(** A particular cell in the board *)
type cell

(** Default reward for winning *)
val win_reward : float

(** Default reward for losing *)
val lose_reward : float

(** Default reward for survival *)
val survival_reward : float

(** Reads in a grid world board from the path [fname] *)
val read_board : string -> cell list list

(** Prints [board] to stdout *)
val print_board : cell list list -> unit

(** Returns the list of states for which [f c] is true *)
val get_states_with_property : cell list list -> f:(cell -> bool) -> State.t list

(** Returns the list of starting states of [board] *)
val get_starting_states : cell list list -> State.t list

(** Returns the list of possible or non solid states of [board] *)
val get_possible_states : cell list list -> State.t list

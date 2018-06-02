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
val read_board : string -> t

(** Returns the list of states for which [f c] is true *)
val get_states_with_property : cell list list -> f:(cell -> bool) -> State.t list

(** Returns the list of starting states of [board] *)
val get_starting_states : cell list list -> State.t list

(** Returns the list of possible or non solid states of [board] *)
val get_possible_states : cell list list -> State.t list

(** Converts a board into a printable string *)
val to_string : t -> string

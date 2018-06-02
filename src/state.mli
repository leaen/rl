open Base__

(** The current state of the grid world *)
type t

(** Make a state from the position in grid world *)
val make : int -> int -> t

(** Get current x position *)
val get_x : t -> int

(** Get current y position *)
val get_y : t -> int

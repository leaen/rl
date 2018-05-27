open Base__

(** A policy that maps states to actions *)
type t

(** Generate a random policy for [board] *)
val get_random : Board.t -> t


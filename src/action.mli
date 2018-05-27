open Base__

(** An element of the action space of the grid world *)
type t

(** Applies the move [a] when the actor is in state [s] *)
val move : int -> int -> State.t -> t

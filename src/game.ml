open Base__

let b = Board.read_board "boards/board.txt"
let cur = List.random_element (Board.get_starting_states b)

let message = "test 123"

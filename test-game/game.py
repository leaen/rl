import random
import math
import sys
import time
import os

board_width = 4
board_height = 3

# Each tuple in blocked_states represents an unenterable state that
#   the player will 'bounce back' against
blocked_states = [(0, 1),
                  (1, 1),
                  (2, 1)]

# Each tuple in the pdf represents the probability of a starting state
#   and the state itself
starting_state_pdf = [(1, (0,0))]
starting_states = [(0,0)]

# Each tuple in the terminal_states list represents a terminal state
#   and its corresponding reward
terminal_states = {(0, 2): 1}

# Other parameters and constants
default_r = -0.04
lr = 1
gamma = 0.75
time_horizon = 50
rounds = 15
neg_inf = -math.inf

def read_board(fname):
    b_text = [s.strip() for s in open(fname).read().strip().split('\n')][::-1]

    global blocked_states, starting_state_pdf, terminal_states
    global board_width, board_height, starting_states

    board_width = len(b_text[0])
    board_height = len(b_text)

    blocked_states = []
    terminal_states = {}
    starting_states = []
    starting_state_pdf = []
    for y in range(board_height):
        for x in range(board_width):
            if b_text[y][x] == '#':
                blocked_states.append((x,y))
            elif b_text[y][x] == '$':
                terminal_states[(x, y)] = 1
            elif b_text[y][x] == 'x':
                terminal_states[(x, y)] = -1
            elif b_text[y][x] == 's':
                starting_states.append((x, y))

    for s in starting_states:
        starting_state_pdf.append((1/len(starting_states), s))

def get_states():
    for x in range(board_width):
        for y in range(board_height):
            yield (x, y)

def get_starting_state():
    x = random.random()
    c = 0

    for prob, state in starting_state_pdf:
        c += prob
        if x <= c:
            return state

def get_reward(s):
    if s in terminal_states:
        return terminal_states[s]

    return default_r

def move_up(s):
    proposed_s = (s[0], min(s[1]+1, 2))
    next_s = proposed_s if proposed_s not in blocked_states else s
    r = get_reward(next_s)
    return (next_s, r)

def move_down(s):
    proposed_s = (s[0], max(s[1]-1, 0))
    next_s = proposed_s if proposed_s not in blocked_states else s
    r = get_reward(next_s)
    return (next_s, r)

def move_left(s):
    proposed_s = (max(s[0]-1, 0), s[1])
    next_s = proposed_s if proposed_s not in blocked_states else s
    r = get_reward(next_s)
    return (next_s, r)

def move_right(s):
    proposed_s = (min(s[0]+1, 3), s[1])
    next_s = proposed_s if proposed_s not in blocked_states else s
    r = get_reward(next_s)
    return (next_s, r)

# Actions is a dictionary of letters which represent the options
#   that the agent can make from a particular position to a tuple
#   where the first element is the probability of making an action
#   and the second element is an action function that takes a state
#   and returns a tuple containing the next state and the reward
actions = {
    'U': [(0.1, move_left), (0.8, move_up), (0.1, move_right)],
    'D': [(0.1, move_right), (0.8, move_down), (0.1, move_left)],
    'L': [(0.1, move_down), (0.8, move_left), (0.1, move_up)],
    'R': [(0.1, move_up), (0.8, move_right), (0.1, move_down)],
    }

def make_action(s, a):

    if a not in actions:
        raise Exception(f'Unknown action {a}')

    pdf = actions[a]
    x = random.random()
    c = 0

    for prob, action in pdf:
        c += prob
        if x <= c:
            return action(s)

def get_random_q():
    action_space = list(actions.keys())
    state_space = list(get_states())

    # Initialise all action-values to 0
    q = {s:{a:0 for a in action_space} for s in state_space}

    return q

def get_best_action(q, s):
    best_a = -1
    best_val = -math.inf

    for a in q[s]:
        if q[s][a] > best_val:
            best_a = a
            best_val = q[s][a]

    return best_a

def update_q(q, s, a, s_prime, r):
    s_prime_ev = q[s_prime][get_best_action(q, s_prime)]
    expected_future = gamma*s_prime_ev
    q[s][a] += lr * (r + expected_future - q[s][a])
    return q

def q_step(q, s):
    a = get_best_action(q, s)
    s_prime, r = make_action(s, a)
    q = update_q(q, s, a, s_prime, r)
    return q, s_prime

def q_episode(q):
    s = get_starting_state()

    while s not in terminal_states:
        q, s = q_step(q, s)

    return q

def q_to_policy(q):
    return {s:get_best_action(q, s) for s in get_states()}

def get_random_policy():
    action_space = list(actions.keys())

    return {s:random.choice(action_space) for s in get_states()}

def td_lambda(policy, values, lam=0.7):
    eligibility = {s:0 for s in get_states()}
    new_values = {s:values[s] for s in get_states()}
    cur_s = get_starting_state()
    t = 1

    while True:
        next_s, r = make_action(cur_s, policy[cur_s])
        eligibility[cur_s] += 1

        alpha = 1/t

        for s in get_states():
            error = r + gamma*values[next_s] - values[cur_s]
            new_values[s] = new_values[s] + alpha*error*eligibility[s]
            eligibility[s] = lam*gamma*eligibility[s]

        if next_s in terminal_states or t == time_horizon:
            break

        cur_s = next_s
        t += 1

    return new_values

def print_policy(policy, cur_x = -1, cur_y = -1):
    table = [[policy[(x, y)] for x in range(board_width)] for y in range(board_height)]

    # Replace blocked states with an empty cell
    for blocked_s in blocked_states:
        x, y = blocked_s
        table[y][x] = ' '

    # Replace positive terminal states with $ and negative
    #   terminal states with x
    for terminal_s in terminal_states:
        x, y = terminal_s
        if terminal_states[terminal_s] > 0:
            table[y][x] = '$'
        else:
            table[y][x] = 'x'

    for x, y in starting_states:
        table[y][x] = 's'

    if cur_x >= 0 and cur_y >= 0:
        table[cur_y][cur_x] = 'X'

    table = table[::-1]

    s = "---------\n"
    s += '\n'.join(['|'.join([''] + row + ['']) for row in table])
    s += "\n---------"

    print(s)

def choose_policy(policy, values):
    new_policy = {}

    for s in get_states():
        best_action = ''
        best_ev = neg_inf

        for a in actions:
            ev = 0
            for prob, action_fun in actions[a]:
                next_s, r = action_fun(s)
                ev += prob * values[next_s]

            if ev > best_ev:
                best_ev = ev
                best_action = a

        new_policy[s] = best_action

    return new_policy

def main():
    if len(sys.argv) == 2:
        read_board(sys.argv[1])

    q = get_random_q()

    for episode in range(rounds):
        print(f'\nStarting episode {episode+1}, curent policy:')
        print_policy(q_to_policy(q))

        q = q_episode(q)

if __name__ == '__main__':
    main()


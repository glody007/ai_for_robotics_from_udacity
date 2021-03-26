# ----------
# User Instructions:
#
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's
# optimal path to the position specified in goal;
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making
                  # a right turn, no turn, and a left turn

def get_next_state(state, forward_move):
    move = forward[forward_move]
    next_state = []
    next_state.append(state[0] + move[0])
    next_state.append(state[1] + move[1])
    next_state.append(forward_move)
    return next_state

def can_it_go_to_state(grid, state, forward_move):
    next_state = get_next_state(state, forward_move)
    if next_state[0] < 0 or next_state[0] >= len(grid):
        return False
    if next_state[1] < 0 or next_state[1] >= len(grid[0]):
        return False
    if grid[next_state[0]][next_state[1]] == 1:
        return False
    return True

def add_state(to_search, state, past_cost, step_cost, path, move):
    new_path = [e for e in path]
    state.append(move)
    new_path.append(state)
    to_search.append([state[0], state[1], state[2], past_cost + step_cost, new_path])

def pop_state_with_cost(to_search, goal):
    i_min_cost = 0
    for i in range(len(to_search)):
        if to_search[i][3] < to_search[i_min_cost][3]:
            i_min_cost = i
    state_min_cost = to_search[i_min_cost]
    to_search.pop(i_min_cost)
    return state_min_cost


def search_helper(grid, init, goal, cost):
    to_search = []
    state = init
    add_state(to_search, state, 0, 0, [], '')
    while True:
        if len(to_search) == 0:
            return []
        state_with_path = pop_state_with_cost(to_search, goal)
        state = [state_with_path[0], state_with_path[1], state_with_path[2]]
        past_cost = state_with_path[3]
        path = state_with_path[4]
        if state[0] == goal[0] and state[1] == goal[1]:
            return path
        for i in range(len(action)):
            forward_move = (state[2] + action[i]) % len(forward)
            if can_it_go_to_state(grid, state, forward_move):
                next_state = get_next_state(state, forward_move)
                add_state(to_search, next_state, past_cost, cost[i], path, action_name[i])

def optimum_policy2D(grid,init,goal,cost):
    path = search_helper(grid, init, goal, cost)
    action = [[' ' for e in row] for row in grid]
    action[goal[0]][goal[1]] = '*'
    for i in range(len(path)):
        if i < len(path) -1:
            state = [path[i][0], path[i][1]]
            move = path[i+1][3]
            action[state[0]][state[1]] = move
    return action

action = optimum_policy2D(grid, init, goal, cost)

def show(grid):
    print("-----------------")
    for row in grid:
         print(row)

show(action)

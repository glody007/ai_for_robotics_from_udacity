# ----------
# User Instructions:
#
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']


def next_position(pos, move):
    next_pos = []
    next_pos.append(pos[0] + move[0])
    next_pos.append(pos[1] + move[1])
    return next_pos

def can_it_go_to_position(grid, pos, move):
    next_pos = next_position(pos, move)
    if next_pos[0] < 0 or next_pos[0] >= len(grid):
        return False
    if next_pos[1] < 0 or next_pos[1] >= len(grid[0]):
        return False
    if grid[next_pos[0]][next_pos[1]] == 1:
        return False
    return True

def add_pos(value, moves, to_search, pos, past_cost, step_cost, path, move):
    cost = past_cost + step_cost
    if value[pos[0]][pos[1]] > cost:
        new_path = [e for e in path]
        pos.append(move)
        value[pos[0]][pos[1]] = cost
        moves[pos[0]][pos[1]] = move
        to_search.append([pos[0], pos[1], past_cost + step_cost, new_path])


def compute_value(grid,goal,cost):
    value = [[99 for e in row] for row in grid]
    moves = [[' ' for e in row] for row in grid]
    to_search = []
    pos = goal
    add_pos(value, moves, to_search, goal, 0, 0, [], '*')
    while True:
        if len(to_search) == 0:
            return value, moves
        pos_with_path = to_search.pop(0)
        pos = [pos_with_path[0], pos_with_path[1]]
        past_cost = pos_with_path[2]
        path = pos_with_path[3]
        if pos[0] == goal[0] and pos[1] == goal[1]:
            value[goal[0]][goal[1]] = 0
        for i in range(len(delta)):
            if can_it_go_to_position(grid, pos, delta[i]):
                add_pos(value, moves, to_search, next_position(pos, delta[i]), past_cost, cost, path, delta_name[i])

def reverse(moves):
    reverse_moves = [[e for e in row] for row in moves]
    for row in range(len(moves)):
        for col in range(len(moves[0])):
            if moves[row][col] == delta_name[0]:
                reverse_moves[row][col] = delta_name[2]
            elif moves[row][col] == delta_name[1]:
                reverse_moves[row][col] = delta_name[3]
            elif moves[row][col] == delta_name[2]:
                reverse_moves[row][col] = delta_name[0]
            elif moves[row][col] == delta_name[3]:
                reverse_moves[row][col] = delta_name[1]
    return reverse_moves

def optimum_policy(grid, goal,cost):
    value, moves = compute_value(grid, goal, cost)
    return reverse(moves)

def show(grid):
    print("-----------------")
    for row in grid:
         print(row)

show(optimum_policy(grid, goal, cost))

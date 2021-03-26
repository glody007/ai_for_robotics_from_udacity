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
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
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

def can_it_go_to_position(grid, occ_grid, pos, move):
    next_pos = next_position(pos, move)
    if next_pos[0] < 0 or next_pos[0] >= len(grid):
        return False
    if next_pos[1] < 0 or next_pos[1] >= len(grid[0]):
        return False
    if grid[next_pos[0]][next_pos[1]] == 1:
        return False
    if occ_grid[next_pos[0]][next_pos[1]]:
        return False
    return True

def add_pos(to_search, pos, past_cost, step_cost):
    to_search.append([pos[0], pos[1], past_cost + step_cost])

def pop_pos_with_cost(to_search, occ_grid):
    i_min_cost = 0
    for i in range(len(to_search)):
        if to_search[i][2] < to_search[i_min_cost][2]:
            i_min_cost = i
    pos_min_cost = to_search[i_min_cost]
    to_search.pop(i_min_cost)
    occ_grid[pos_min_cost[0]][pos_min_cost[1]] = True
    return pos_min_cost

def search(grid,init,goal,cost):
    occ_grid = [[False for e in row] for row in grid]
    to_search = []
    pos = init
    add_pos(to_search, pos, 0, 0)
    while True:
        if len(to_search) == 0:
            return 'fail'
        pos_with_cost = pop_pos_with_cost(to_search, occ_grid)
        pos = [pos_with_cost[0], pos_with_cost[1]]
        past_cost = pos_with_cost[2]

        if pos[0] == goal[0] and pos[1] == goal[1]:
            return [past_cost, pos[0], pos[1]]
        for move in delta:
            if can_it_go_to_position(grid, occ_grid, pos, move):
                add_pos(to_search, next_position(pos, move), past_cost, cost)

def compute_value(grid,goal,cost):
    value = [[99 if e == 1 else 0 for e in row] for row in grid]
    for row in range(len(grid)):
        for col in range(len(grid[1])):
            if grid[row][col] == 0:
                result = search(grid, [row, col], goal, cost)
                if result == 'fail':
                    value[row][col] = 99
                else:
                    value[row][col] = result[0]
    return value

def show(grid):
    print("-----------------")
    for row in grid:
         print(row)

show(compute_value(grid, goal, cost))

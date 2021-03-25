grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

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

def add_pos(to_search, pos, past_cost, step_cost, path, move):
    new_path = [e for e in path]
    pos.append(move)
    new_path.append(pos)
    to_search.append([pos[0], pos[1], past_cost + step_cost, new_path])

def pop_pos_with_cost(to_search):
    i_min_cost = 0
    for i in range(len(to_search)):
        if to_search[i][2] < to_search[i_min_cost][2]:
            i_min_cost = i
    pos_min_cost = to_search[i_min_cost]
    to_search.pop(i_min_cost)
    return pos_min_cost

def search_helper(grid, init, goal, cost):
    to_search = []
    pos = init
    occ_grid = [[False for e in row] for row in grid]
    occ_grid[init[0]][init[1]] = True
    add_pos(to_search, pos, 0, 0, [], '')
    while True:
        if len(to_search) == 0:
            return 'fail'
        pos_with_path = pop_pos_with_cost(to_search)
        pos = [pos_with_path[0], pos_with_path[1]]
        past_cost = pos_with_path[2]
        path = pos_with_path[3]
        if pos[0] == goal[0] and pos[1] == goal[1]:
            return path
        for i in range(len(delta)):
            if can_it_go_to_position(grid, occ_grid, pos, delta[i]):
                next_pos = next_position(pos, delta[i])
                occ_grid[next_pos[0]][next_pos[1]] = True
                add_pos(to_search, next_pos, past_cost, cost, path, delta_name[i])

def search(grid,init,goal,cost):
    result = search_helper(grid, init, goal, cost)
    expand = [[' ' for e in row] for row in grid]
    expand[goal[0]][goal[1]] = '*'
    if result != 'fail':
        for i in range(len(result)):
            if i < len(result) -1:
                pos = [result[i][0], result[i][1]]
                move = result[i+1][2]
                expand[pos[0]][pos[1]] = move
    return expand

for row in search(grid, init, goal, cost):
    print(row)

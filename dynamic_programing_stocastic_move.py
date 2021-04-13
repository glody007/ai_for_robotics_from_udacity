# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def next_position(pos, move):
    next_pos = []
    next_pos.append(pos[0] + move[0])
    next_pos.append(pos[1] + move[1])
    return next_pos

def value_from_position(grid, value, pos, move, prob, collision_cost):
    next_pos = next_position(pos, move)
    if next_pos[0] < 0 or next_pos[0] >= len(grid):
        return prob * collision_cost
    if next_pos[1] < 0 or next_pos[1] >= len(grid[0]):
        return prob * collision_cost
    if grid[next_pos[0]][next_pos[1]] == 1:
        return prob * collision_cost
    return prob * value[next_pos[0]][next_pos[1]]

def value_from_move(grid, value, pos, move, success_prob, failure_prob, goal, collision_cost, step_cost):
    total_value = value_from_position(grid, value, pos, move, success_prob, collision_cost)
    if move[0] == 0:
        total_value += value_from_position(grid, value, pos, delta[0], failure_prob, collision_cost)
        total_value += value_from_position(grid, value, pos, delta[2], failure_prob, collision_cost)
    else:
        total_value += value_from_position(grid, value, pos, delta[1], failure_prob, collision_cost)
        total_value += value_from_position(grid, value, pos, delta[3], failure_prob, collision_cost)
    return total_value + step_cost

def compute_value(grid, value, policy, pos, success_prob, failure_prob, goal, collision_cost, step_cost):
    actual_value = value[pos[0]][pos[1]]
    change = False
    move = policy[pos[0]][pos[1]]
    if pos[0] == goal[0] and pos[1] == goal[1]:
        return 0, '*', change
    if grid[pos[0]][pos[1]] == 1:
        return collision_cost, ' ', change
    for i in range(len(delta)):
        value_move =  value_from_move(grid, value, pos, delta[i], success_prob, failure_prob, goal, collision_cost, step_cost)
        if value_move < actual_value:
            actual_value = value_move
            move = delta_name[i]
            change = True
    return actual_value, move, change


def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

    change = True
    value[goal[0]][goal[1]] = 0

    while change:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                value[row][col], policy[row][col], change = compute_value(grid, value, policy, [row, col], success_prob, failure_prob, goal, collision_cost, cost_step)

    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]]
goal = [0, 6]
cost_step = 1
collision_cost = 100
success_prob = 0.8

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
#[471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
#[334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977],
#[398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738],
#[700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']

def show(grid):
    print("-----------------")
    for row in grid:
         print(row)

show(value)
show(policy)

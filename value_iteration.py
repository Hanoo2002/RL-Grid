REWARD = -1
GAMMA = 0.99


NUM_ACTIONS = 4
ACTIONS = [(1,0),(0,1),(-1,0),(0,-1)]
# down left up right
ACTIONS_TEXT = ["DOWN", "RIGHT", "UP", "LEFT"]

NUM_ROWS = 3
NUM_COLS = 3



#Calculate new value of state given next action
#Pass action / next action as numbers between 0 and 3
def get_v (env_v,row,col,next_action):
    """
    Calculate v*(s')
    """
    dr = ACTIONS[next_action][0]
    dc = ACTIONS[next_action][1]
    newR = row + dr
    newC = col + dc
    if newR < 0 or newC < 0 or newR >= NUM_ROWS or newC >= NUM_ROWS :
        return env_v[row][col]
    else:
        return env_v[newR][newC]
    
def calc_v (env_v ,row, col, action):
    """
    Rs a + GAMMA sum (Pss' a) v*(s')
    """
    v = 0
    v += 0.1 * get_v(env_v, row, col, (action-1)%NUM_ACTIONS)
    v += 0.8 * get_v(env_v, row, col, action)
    v += 0.1 *  get_v(env_v, row, col, (action+1)%NUM_ACTIONS)
    v *= GAMMA
    r = -1
    if (row == 0 and col == 0) or (row == 0 and col == 2):
        r = ENV_R[row][col]
    v+=r
    return v

def value_iteration(env_v,N):
    """
    Bellman Update equation
    """
    for _ in range (0,N):
        nextv = env_v

        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if (r == 0 and c == 0) or (r == 0 and c == 2):
                    continue
                nextv[r][c] = max([calc_v(env_v, r, c, action) for action in range(NUM_ACTIONS)]) 
        
        env_v = nextv
        
    return env_v

def get_policy(env_v):
    policy = [[-1, -1, -1] for i in range(NUM_ROWS)]
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if (r == 0 and c == 0) or (r == 0 and c == 2):
                continue
            # Choose the action that maximizes the utility
            maxAction, maxU = None, -float("inf")
            for action in range(NUM_ACTIONS):
                u = calc_v(env_v, r, c, action)
                if u > maxU:
                    maxAction, maxU = action, u
            policy[r][c] = maxAction
    policy_text = [["Terminal","Terminal", "Terminal"] for i in range(NUM_ROWS)]
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if policy[r][c] == -1:
                continue
            else:
                policy_text[r][c] = ACTIONS_TEXT [policy[r][c]]
            
    return policy_text

def print_2d_grid(grid, N):
    print("+" * 4 * N)
    for row in grid:
        print(" | ".join(["{:^{width}}".format(str(elem), width=N) for elem in row]))
    print("+" * 4 * N )

diff_r = [100,3,0,-3,10]

for r in diff_r:
    print(f"FOR R = {r}")
    ENV_R = [[r,-1,10], [-1,-1,-1], [-1,-1,-1]]
    env_v = [[r,0,10],[0,0,0],[0,0,0]]
    V = value_iteration(env_v, 100)
    print_2d_grid(V,20)
    print("\n")
    p = get_policy(V)
    print_2d_grid(p,10)
    
    print("\n\n")

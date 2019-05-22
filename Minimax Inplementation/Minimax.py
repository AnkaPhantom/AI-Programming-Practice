from copy import deepcopy

with open('input1.txt','r') as f:
    N = int(f.readline())
    Grid = [[0 for x in range(N)] for y in range(N)]
    i = 0
    #save the data into the 2d array
    for line in f:
        j = 0
        for content in line:
            if content != '\n':
                Grid[i][j] = int(content)
            j += 1
        i += 1

def calculation(weight, player):
    if weight == 0:
        weight = -player
    if (player == 1 and weight == -2) or (player == 2 and weight == -1):
        weight = -3
    return weight

def update_grid(Grid, in_i, in_j, player):
    score = 1
    i = in_i
    j = in_j
    count = 0
    Grid[in_i][in_j] = player
    #down
    while i+1 < N and count < 3:
        if Grid[i+1][j] != 3:
            Grid[i+1][j] = calculation(Grid[i+1][j], player)
        else:
            break
        i += 1
        count += 1
    i = in_i
    j = in_j
    count = 0
    #up
    while i-1 >= 0 and count < 3:
        if Grid[i-1][j] != 3:
            Grid[i-1][j] = calculation(Grid[i-1][j], player)
        else:
            break
        i -= 1
        count += 1
    i = in_i
    j = in_j
    count = 0
    #left
    while j-1 >= 0 and count < 3:
        if Grid[i][j-1] != 3:
            Grid[i][j-1] = calculation(Grid[i][j-1], player)
        else:
            break
        j -= 1
        count += 1
    i = in_i
    j = in_j
    count = 0
    #right
    while j+1 < N and count < 3:
        if Grid[i][j+1] != 3:
            Grid[i][j+1] = calculation(Grid[i][j+1], player)
        else:
            break
        j += 1
        count += 1
    i = in_i
    j = in_j
    count = 0
    #down left
    while i+1 < N and j-1 >= 0 and count < 3:
        if Grid[i+1][j-1] != 3:
            Grid[i+1][j-1] = calculation(Grid[i+1][j-1], player)
        else:
            break
        i += 1
        j -= 1
        count += 1
    #up left
    i = in_i
    j = in_j
    count = 0
    while i-1 >= 0 and j-1 >= 0 and count < 3:
        if Grid[i-1][j-1] != 3:
            Grid[i-1][j-1] = calculation(Grid[i-1][j-1], player)
        else:
            break
        i -= 1
        j -= 1
        count += 1
    #down right
    i = in_i
    j = in_j
    count = 0
    while i+1 < N and j+1 < N and count < 3:
        if Grid[i+1][j+1] != 3:
            Grid[i+1][j+1] = calculation(Grid[i+1][j+1], player)
        else:
            break
        i += 1
        j += 1
        count += 1
    i = in_i
    j = in_j
    count = 0
    #up right
    while i-1 >=0 and j+1 < N and count < 3:
        if Grid[i-1][j+1] != 3:
            Grid[i-1][j+1] = calculation(Grid[i-1][j+1], player)
        else:
            break
        i -= 1
        j += 1
        count += 1

def end(grid):
    for i in xrange(N):
        for j in xrange(N):
            if grid[i][j] == 0:
                return False
    return True

def winner(grid):
	score1 = 0, score2 = 0
    for i in xrange(N):
        for j in xrange(N):
            if grid[i][j] == 1 or grid[i][j] == -1:
				score1 += 1
			elif grid[i][j] == 2 or grid[i][j] == -2:
				score2 += 1
			elif grid[i][j] == -3:
				score1 += 1
				score2 += 1
    return score1 - score2

def minimax(grid, player, depth):
    if player == 1:
        if depth == 0 or end(grid):
            player_score = winner(grid)
            return [-1, -1, player_score]
        max_score = [-1, -1, -10000]
        for i in xrange(N):
            for j in xrange(N):
                if grid[i][j] == 0:
                    temp = deepcopy(grid)
                    update_grid(temp, i, j, player)
                    score = minimax(temp, 2, depth-1)
                    score[0] = i
                    score[1] = j
                    if max_score[2] < score[2]:
                        max_score = score
        return max_score
    elif player == 2:
        if depth == 0 or end(grid):
            player_score = winner(grid)
            return [-1, -1, player_score]
        min_score = [-1, -1, 10000]
        for i in xrange(N):
            for j in xrange(N):
                if grid[i][j] == 0:
                    temp = deepcopy(grid)
                    update_grid(temp, i, j, player)
                    score = minimax(temp, 1, depth-1)
                    score[0] = i
                    score[1] = j
                    if min_score[2] > score[2]:
                        min_score = score
        return min_score

if __name__ == '__main__':
    for i in xrange(N):
        for j in xrange(N):
            if Grid[i][j] == 1 or Grid[i][j] == 2:
                update_grid(Grid, i, j, Grid[i][j])	
				
    s = minimax(Grid, 1, 4)
    print N
    print Grid
    print s
    f = open("output.txt", "w")
    f.write( str(s[0]) )
    f.write(' ')
    f.write( str(s[1]) )
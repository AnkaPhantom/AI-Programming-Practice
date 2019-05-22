from copy import deepcopy
import heapq
import time
import math
#import numpy as np

with open('input0.txt','r') as f:
    grid_width = int(f.readline())
    Grid = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
    utility_Grid = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
    for c in xrange(grid_width):
        for d in xrange(grid_width):
            utility_Grid[c][d] = ' '

    wall_num = int(f.readline())
    a = 0
    for a in xrange(wall_num):
        wall_coordinate = f.readline()
        content = wall_coordinate.split(',')
        #print content
        Grid[ int(content[0])-1 ][ int(content[1])-1 ] = 'N'
        utility_Grid[ int(content[0])-1 ][ int(content[1])-1 ] = 'N'

    reward_num = int(f.readline())
    b = 0
    for b in xrange(reward_num):
        reward_coordinate = f.readline()
        content2 = reward_coordinate.split(',')
        Grid[ int(content2[0])-1 ][ int(content2[1])-1 ] = 'E'
        #print content2
        utility_Grid[ int(content2[0])-1 ][ int(content2[1])-1 ] = int(content2[2])

    intent_p = float(f.readline())
    Rp = float(f.readline())
    Dis_factor = float(f.readline())

    for x in xrange(grid_width):
        for y in xrange(grid_width):
            if utility_Grid[x][y] == ' ':
                utility_Grid[x][y]  = Rp

Final_Grid = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
Final_Grid = Grid

def calculation_iteration(grid,r,c,act):
    if act == 'U':
        if  r-1<0:
            up = grid[r][c]
        else:
            if Grid[r-1][c]=='N':
                up = grid[r][c]
            else:
                up = grid[r-1][c]
        if r-1<0 or c-1<0:
            up1 = grid[r][c]
        else:
            if Grid[r-1][c-1]=='N':
                up1 = grid[r][c]
            else:
                up1 = grid[r-1][c-1]
        if r-1<0 or c+1>grid_width-1:
            up2 = grid[r][c]
        else:
            if Grid[r-1][c+1] == 'N':
                up2 = grid[r][c]
            else:
                up2 = grid[r-1][c+1]
        ut = float(up)*intent_p + float(up1)*( (1-intent_p)/2 ) + float(up2)*( (1-intent_p)/2 )
    elif act == 'D':
        if r+1>grid_width-1:
            down = grid[r][c]
        else:
            if Grid[r+1][c]=='N':
                down = grid[r][c]
            else:
                down = grid[r+1][c]
        if r+1>grid_width-1 or c+1>grid_width-1:
            down1 = grid[r][c]
        else:
            if Grid[r+1][c+1]=='N':
                down1 = grid[r][c]
            else:
                down1 = grid[r+1][c+1]
        if r+1>grid_width-1 or c-1<0:
            down2 = grid[r][c]
        else:
            if Grid[r+1][c-1]=='N':
                down2 = grid[r][c]
            else:
                down2 = grid[r+1][c-1]
        ut = float(down)*intent_p + float(down1)*( (1-intent_p)/2 ) + float(down2)*( (1-intent_p)/2 )
    elif act == 'L':
        if c-1<0:
            left = grid[r][c]
        else:
            if Grid[r][c-1]=='N':
                left = grid[r][c]
            else:
                left = grid[r][c-1]
        if r+1>grid_width-1 or c-1<0:
            left1 = grid[r][c]
        else:
            if Grid[r+1][c-1]=='N':
                left1 = grid[r][c]
            else:
                left1 = grid[r+1][c-1]
        if r-1<0 or c-1<0:
            left2 = grid[r][c]
        else:
            if Grid[r-1][c-1]=='N':
                left2 = grid[r][c]
            else:
                left2 = grid[r-1][c-1]
        ut = float(left)*intent_p +float(left1)*( (1-intent_p)/2 ) + float(left2)*( (1-intent_p)/2 )
    else:
        if c+1>grid_width-1:
            right = grid[r][c]
        else:
            if Grid[r][c+1]=='N':
                right = grid[r][c]
            else:
                right = grid[r][c+1]
        if r-1<0 or c+1>grid_width-1:
            right1 = grid[r][c]
        else:
            if Grid[r-1][c+1]=='N':
                right1 = grid[r][c]
            else:
                right1 = grid[r-1][c+1]
        if r+1>grid_width-1 or c+1>grid_width-1:
            right2 = grid[r][c]
        else:
            if Grid[r+1][c+1]=='N':
                right2 = grid[r][c]
            else:
                right2 = grid[r+1][c+1]
        ut = float(right)*intent_p + float(right1)*( (1-intent_p)/2 ) + float(right2)*( (1-intent_p)/2 )
        #round(ut, 3)
    #Final_Grid[r][c]=act
    return ut

def MDP(GGrid, grid, action, direction_p, R, gamma,count):
    ggrid = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
    for i in xrange(grid_width):
        for j in xrange(grid_width):
            if GGrid[i][j] == 0:
                #ggrid[i][j] = gamma * max(calculation_iteration(grid, i, j, action[0]), calculation_iteration(grid, i, j, action[1]),
                #                          calculation_iteration(grid, i, j, action[2]), calculation_iteration(grid, i, j, action[3]))
                a = calculation_iteration(grid, i, j, action[0])
                b = calculation_iteration(grid, i, j, action[1])
                c = calculation_iteration(grid, i, j, action[2])
                d = calculation_iteration(grid, i, j, action[3])
                e = max(a, b, c, d)
                ggrid[i][j] = Rp + gamma * e
                if count > 99:
                    if e == a:
                        Final_Grid[i][j] = 'U'
                    elif e == b:
                        Final_Grid[i][j] = 'D'
                    elif e == c:
                        Final_Grid[i][j] = 'L'
                    elif e == d:
                        Final_Grid[i][j] = 'R'
            else:
                ggrid[i][j] = grid[i][j]
    return ggrid

if __name__ == '__main__':

    figure_action = ['U', 'D', 'L', 'R']
    #time_schedule.sort(key=lambda x:x[-1])
    #print Grid
    #print utility_Grid
    #reward = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
    #reward = utility_Grid
    #print utility_Grid
    #print intent_p
    #print Rp
    #print Dis_factor
    #print Final_Grid
    #before = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
    #after = [[0 for x in xrange(grid_width)] for y in xrange(grid_width)]
    #print Grid
    a=0
    while(1):
        before = utility_Grid
        utility_Grid = MDP(Grid, utility_Grid, figure_action, intent_p, Rp, Dis_factor, a)
        after = utility_Grid
        #for i in xrange(grid_width):
        #    for j in xrange(grid_width):
        #        if after[i][j]-before[i][j]>0.01:
        #            break
        a+=1
        if a>100:
            break
    for i in range(grid_width):
        print utility_Grid[i]
    #print before
    #print after
    #print Grid
    print Final_Grid
    f = open("output.txt", "w")
    for w in xrange(grid_width):
        for h in xrange(grid_width):
            f.write( str(Final_Grid[w][h]) )
            if h != grid_width-1:
                f.write(',')
        f.write('\n')
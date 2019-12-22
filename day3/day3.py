#! /usr/bin/env python

import math
import sys
from collections import defaultdict

def main():
    with open(sys.argv[1]) as fp:
        wire1 = fp.readline().strip().split(',')
        wire2 = fp.readline().strip().split(',')
    board = defaultdict(lambda: defaultdict(int))
    x = 0
    y = 0
    num_steps = 0
    for move in wire1:
        direction = move[0]
        steps = int(move[1:])
        for step in range(steps):
            if direction == 'R':
                x += 1
            elif direction == 'L':
                x -= 1
            elif direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            num_steps += 1
            board[x][y] = num_steps
    x = 0
    y = 0
    num_steps = 0
    crosses = []
    for move in wire2:
        direction = move[0]
        steps = int(move[1:])
        for step in range(steps):
            if direction == 'R':
                x +=1 
            elif direction == 'L':
                x -= 1
            elif direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            num_steps +=1
            wire1_steps = board[x][y]
            if wire1_steps:
                crosses.append((x, y, wire1_steps, num_steps))

    nearest = math.inf
    fewest_steps = math.inf
    for cross in crosses:
        nearest = min(nearest, abs(cross[0]) + abs(cross[1]))
        fewest_steps = min(fewest_steps, cross[2] + cross[3])
    print(nearest, fewest_steps)

if __name__ == '__main__':
    main()

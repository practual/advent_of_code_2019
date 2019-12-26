#! /usr/bin/env python

import math
import re
import sys
from itertools import combinations


def step_in_time(moons_s, moons_v):
    for pair in combinations('0123', 2):
        moon1_s = moons_s[int(pair[0])]
        moon1_v = moons_v[int(pair[0])]
        moon2_s = moons_s[int(pair[1])]
        moon2_v = moons_v[int(pair[1])]
        for d in range(3):
            if moon1_s[d] == moon2_s[d]:
                continue
            if moon1_s[d] > moon2_s[d]:
                moon1_v[d] -= 1
                moon2_v[d] += 1
            else:
                moon1_v[d] += 1
                moon2_v[d] -= 1
    for moon in range(4):
        for d in range(3):
            moons_s[moon][d] += moons_v[moon][d]


def make_state(moons_s, moons_v, d):
    state = []
    for m in range(4):
        state.append(moons_s[m][d])
        state.append(moons_v[m][d])
    return tuple(state)


def main():
    with open(sys.argv[1]) as fp:
        orig_moons_s = []
        while True:
            moon_pos = fp.readline()
            if not moon_pos:
                break
            orig_moons_s.append(list(map(int, re.findall(r'-?[0-9]+', moon_pos))))
    moons_s = [[x for x in moon] for moon in orig_moons_s]
    moons_v = [[0, 0, 0] for moon in moons_s]
    for step in range(1000):
        step_in_time(moons_s, moons_v)
    total_energy = sum(
        sum(map(abs, moons_s[moon])) * sum(map(abs, moons_v[moon])) for moon in range(4)
    )
    print(total_energy)

    cycles = [0, 0, 0]
    for d in range(3):
        moons_s = [[x for x in moon] for moon in orig_moons_s]
        moons_v = [[0, 0, 0] for moon in moons_s]
        states = {}
        steps = 0
        state = make_state(moons_s, moons_v, d)
        while state not in states:
            states[state] = True
            step_in_time(moons_s, moons_v)
            state = make_state(moons_s, moons_v, d)
            steps += 1
        cycles[d] = steps
    lcm_x_y = int(cycles[0] * cycles[1] / math.gcd(cycles[0], cycles[1]))
    lcm_x_y_z = int(lcm_x_y * cycles[2] / math.gcd(lcm_x_y, cycles[2]))
    print(lcm_x_y_z)


if __name__ == '__main__':
    main()

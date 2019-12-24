#! /usr/bin/env python

import sys
from collections import defaultdict


def main():
    with open(sys.argv[1]) as fp:
        raw_orbits = fp.read().split()
    orbits_outwards = defaultdict(list)
    for orbit in raw_orbits:
        inner, outer = orbit.split(')')
        orbits_outwards[inner].append(outer)
    orbit_count = 0

    def count_orbits(inner, base_count):
        nonlocal orbit_count
        for outer in orbits_outwards[inner]:
            orbit_count += base_count
            count_orbits(outer, base_count + 1)

    count_orbits('COM', 1)
    print(orbit_count)

    orbits_inwards = {}
    for orbit in raw_orbits:
        inner, outer = orbit.split(')')
        orbits_inwards[outer] = inner

    inner = orbits_inwards['YOU']
    you_to_com = []
    while inner != 'COM':
        you_to_com.append(inner)
        inner = orbits_inwards[inner]

    inner = orbits_inwards['SAN']
    san_to_com = []
    while inner != 'COM':
        san_to_com.append(inner)
        inner = orbits_inwards[inner]

    adjustment = 0
    while True:
        try:
            you_ancestor = you_to_com.pop()
        except IndexError:
            break
        try:
            san_ancestor = san_to_com.pop()
        except IndexError:
            adjustment += 1
            break

        if you_ancestor != san_ancestor:
            adjustment += 2
            break
    print(len(you_to_com) + len(san_to_com) + adjustment)


if __name__ == '__main__':
    main()

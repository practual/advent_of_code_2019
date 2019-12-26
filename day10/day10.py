#! /usr/bin/env python

import math
import sys
from collections import defaultdict


def get_bearing(coords):
    angle = math.atan2(coords[1], coords[0])
    if angle < -math.pi / 2:
        angle += 2 * math.pi
    return angle


def main():
    with open(sys.argv[1]) as fp:
        asteroids = []
        while True:
            line = fp.readline()
            if not line:
                break
            asteroids.append(list(line.strip()))
    width = len(asteroids[0])
    height = len(asteroids)

    max_visible_asteroids = 0
    station_x, station_y = -1, -1
    for y in range(height):
        for x in range(width):
            if asteroids[y][x] == '.':
                continue
            visible_asteroids = {}
            for test_y in range(height):
                for test_x in range(width):
                    if test_x == x and test_y == y:
                        continue
                    if asteroids[test_y][test_x] == '.':
                        continue
                    d_x = test_x - x
                    d_y = test_y - y
                    gcd = math.gcd(d_x, d_y)
                    visible_asteroids[(int(d_x / gcd), int(d_y / gcd))] = True
            num_visible_asteroids = len(visible_asteroids.keys())
            if num_visible_asteroids > max_visible_asteroids:
                station_x, station_y = x, y
                max_visible_asteroids = num_visible_asteroids
    print(max_visible_asteroids)

    visible_asteroids = defaultdict(list)
    for y in range(height):
        for x in range(width):
            if x == station_x and y == station_y:
                continue
            if asteroids[y][x] == '.':
                continue
            d_x = x - station_x
            d_y = y - station_y
            gcd = math.gcd(d_x, d_y)
            visible_asteroids[(int(d_x / gcd), int(d_y / gcd))].append((x, y))
    clockwise_keys = sorted(visible_asteroids.keys(), key=get_bearing)
    bearing_pointer = 0
    needs_sorting = True
    asteroids_shot = 0
    while asteroids_shot < 200:
        try:
            bearing = clockwise_keys[bearing_pointer]
        except KeyError:
            bearing_pointer = 0
            needs_sorting = False
            continue
        if needs_sorting:
            # All the asteroids along this bearing, sorted with the nearest at the end.
            inline = sorted(
                visible_asteroids[bearing],
                key=lambda coords: (coords[0] - station_x)**2 + (coords[1] - station_y)**2,
                reverse=True
            )
        else:
            inline = visible_asteroids[bearing]
        try:
            last_shot = inline.pop()
        except IndexError:
            bearing_pointer += 1
            continue
        visible_asteroids[bearing] = inline
        asteroids_shot += 1
        bearing_pointer += 1
    print(last_shot)


if __name__ == '__main__':
    main()

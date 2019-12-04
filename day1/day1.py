#! /usr/bin/env python

import math
import sys

def fuel_for_mass(mass):
    return math.floor(mass / 3) - 2


def total_fuel_for_mass(mass):
    total_fuel = 0
    current_mass = mass
    while True:
        fuel = fuel_for_mass(current_mass)
        if fuel <= 0:
            break
        total_fuel += fuel
        current_mass = fuel
    return total_fuel


def main():
    with open(sys.argv[1]) as fp:
        part_1_fuel = 0
        part_2_fuel = 0
        for line in fp:
            try:
                mass = int(line.strip())
            except ValueError:
                continue
            part_1_fuel += fuel_for_mass(mass)
            part_2_fuel += total_fuel_for_mass(mass)
        print(part_1_fuel, part_2_fuel)
            

if __name__ == '__main__':
    main()

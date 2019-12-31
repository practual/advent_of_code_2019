#! /usr/bin/env python

import math
import re
import sys
from collections import defaultdict


def get_chemical(reaction_map, target, quant_needed, allow_fractional, excess=None):
    excess = excess if excess is not None else defaultdict(int)
    if not allow_fractional and excess[target]:
        consumed = min(excess[target], quant_needed)
        excess[target] -= consumed
        quant_needed -= consumed
        if quant_needed == 0:
            # Had the target chemical to spare with no more ore needed.
            return 0

    quant_produced_per_reaction = reaction_map[target]['quant']
    if allow_fractional:
        num_reactions = quant_needed / quant_produced_per_reaction
    else:
        num_reactions = math.ceil(quant_needed / quant_produced_per_reaction)
        total_quant_produced = num_reactions * quant_produced_per_reaction
        excess_produced = total_quant_produced - quant_needed
        excess[target] += excess_produced

    ore_needed = 0
    for input_chem in reaction_map[target]['inputs']:
        if input_chem[1] == 'ORE':
            ore_needed += input_chem[0] * num_reactions
        else:
            ore_needed += get_chemical(reaction_map, input_chem[1], input_chem[0] * num_reactions, allow_fractional, excess)
    return ore_needed


def main():
    with open(sys.argv[1]) as fp:
        reaction_map = {}
        while True:
            reaction_raw = fp.readline()
            if not reaction_raw:
                break
            reaction = re.match(r'(([0-9]+ [A-Z]+,?\s+)+)=> ([0-9]+ [A-Z]+)', reaction_raw)
            inputs_raw = reaction.group(1)
            output_raw = reaction.group(3)
            output_quant, output_chem = output_raw.split()
            output_quant = int(output_quant)
            inputs = [tuple(input_raw.strip().split()) for input_raw in inputs_raw.split(', ')]
            inputs = [(int(input_chem[0]), input_chem[1]) for input_chem in inputs]
            reaction_map[output_chem] = {
                'quant': output_quant,
                'inputs': inputs,
            }
    excess = defaultdict(int)
    ore_needed_per_fuel = get_chemical(reaction_map, 'FUEL', 1, False, excess=excess)
    print('ORE NEEDED FOR 1 FUEL:', ore_needed_per_fuel)

    ore_without_excess = get_chemical(reaction_map, 'FUEL', 1, True)

    excess_ore_per_cycle = ore_needed_per_fuel - ore_without_excess
    ore_available = 1000000000000
    fuel = 0
    while ore_available:
        extra_fuel = ore_available // ore_needed_per_fuel
        if not extra_fuel:
            break
        fuel += extra_fuel
        used_ore = extra_fuel * ore_needed_per_fuel
        ore_available = ore_available - used_ore + extra_fuel * excess_ore_per_cycle

    print('FUEL AVAILABLE WITH A TRILLION ORE:', fuel)


if __name__ == '__main__':
    main()

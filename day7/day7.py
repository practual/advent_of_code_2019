# `python -m day7.day7 ./day7/input`

import sys
from itertools import permutations

from intcode.computer import list_to_program, run_program


def main():
    with open(sys.argv[1]) as fp:
        orig_program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    max_output = 0
    for phases in permutations('01234', 5):
        current_input = 0
        for phase in phases:
            program = list_to_program(orig_program)
            _, current_input = run_program(program, [current_input, phase], True)
        max_output = max(max_output, current_input)
    print('PART 1 MAX OUTPUT', max_output)

    max_output = 0
    for phases in permutations('56789', 5):
        current_input = 0
        current_amp = 0
        amp_states = []
        while True:
            for phase in phases:
                inputs = [current_input]
                try:
                    program, ptr = amp_states[current_amp]
                except IndexError:
                    program = list_to_program(orig_program)
                    ptr = 0
                    amp_states.append((program, ptr))
                    inputs.append(phase)
                try:
                    ptr, current_input = run_program(program, inputs, True, True, ptr)
                except StopIteration:
                    break
                amp_states[current_amp] = (program, ptr)
                current_amp += 1
                current_amp %= 5
            else:
                continue
            break
        max_output = max(max_output, current_input)
    print('PART 2 MAX OUTPUT', max_output)


if __name__ == '__main__':
    main()

# `python -m day2.day2 ./day2/input`

import sys

from intcode.computer import run_program


def main():
    with open(sys.argv[1]) as fp:
        orig_program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    program = list(orig_program)
    program[1] = 12
    program[2] = 2
    print(run_program(program)[0])
    noun = 0
    verb = 0
    while True:
        program = list(orig_program)
        program[1] = noun
        program[2] = verb
        program_output = run_program(program)[0]
        if program_output == 19690720:
            print(100 * noun + verb)
            break
        verb += 1
        if verb == 100:
            verb = 0
            noun += 1
        if noun == 100:
            break


if __name__ == '__main__':
    main()

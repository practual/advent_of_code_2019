# `python -m day9.day9 ./day9/input`

import sys

from intcode.computer import list_to_program, run_program


def main():
    with open(sys.argv[1]) as fp:
        orig_program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    program = list_to_program(orig_program)
    run_program(program)


if __name__ == '__main__':
    main()

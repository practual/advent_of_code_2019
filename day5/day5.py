# `python -m day5.day5 ./day5/input`

import sys

from intcode.computer import run_program


def main():
    with open(sys.argv[1]) as fp:
        orig_program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    program = list(orig_program)
    run_program(program)


if __name__ == '__main__':
    main()

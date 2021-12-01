# `python -m day15.day15 ./day15/input`

import sys
from collections import defaultdict

from intcode.computer import list_to_program, run_program


def main():
    with open(sys.argv[1]) as fp:
        orig_program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    program = list_to_program(orig_program)
    context = {}
    screen = defaultdict(dict)
    while True:
        try:
            context, x = run_program(program, context=context, return_output=True, raise_halt=True)
        except StopIteration:
            break
        context, y = run_program(program, context=context, return_output=True)
        context, tile_id = run_program(program, context=context, return_output=True)
        screen[y][x] = tile_id
    blocks = 0
    for row in screen.values():
        for tile in row.values():
            if tile == 2:
                blocks += 1
    print(blocks)

    def on_input():
        nonlocal screen
        nonlocal score
        rows = sorted(screen.keys())
        row_range = range(rows[0], rows[len(rows) - 1] + 1)
        top, bottom = 0, 0
        for row in rows:
            col = screen[row]
            top = min(top, min(col.keys()))
            bottom = max(bottom, max(col.keys()))
        col_range = range(top, bottom + 1)
        glyphs = {
            0: ' ',
            1: 'W',
            2: 'B',
            3: '=',
            4: 'O',
        }
        for y in row_range:
            for x in col_range:
                print(glyphs[screen[y][x]], end='')
            print('')
        print('SCORE: ', score)
        return input('INPUT: ')

    program = list_to_program(orig_program)
    program[0] = 2
    context = {'input_callback': on_input}
    screen = defaultdict(lambda: defaultdict(dict))
    score = 0
    while True:
        try:
            context, x = run_program(program, context=context, return_output=True, raise_halt=True)
            context, y = run_program(program, context=context, return_output=True, raise_halt=True)
            context, tile_id = run_program(program, context=context, return_output=True, raise_halt=True)
        except (StopIteration, ValueError):
            print('SCOREEEE', score)
            break
        if x == -1:
            score = tile_id
        else:
            screen[y][x] = tile_id


if __name__ == '__main__':
    main()

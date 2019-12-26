# `python -m day11.day11 ./day11/input`

import sys
from collections import defaultdict

from intcode.computer import list_to_program, run_program


def update_position(x, y, direction, turn):
    direction_modifier = -1 + 2 * turn  # Maps 0 (left) to -1, and 1 (right) to +1
    direction = (direction + direction_modifier) % 4
    if direction == 0:
        y -= 1
    elif direction == 1:
        x += 1
    elif direction == 2:
        y += 1
    elif direction == 3:
        x -= 1
    else:
        raise ValueError
    return x, y, direction


def paint(program, starting_colour):
    panels = defaultdict(lambda: defaultdict(int))
    x = 0
    y = 0
    direction = 0
    context = {'inputs': [starting_colour]}
    while True:
        try:
            context, colour = run_program(
                program, context=context, return_output=True, raise_halt=True,
            )
        except StopIteration:
            break
        panels[y][x] = colour
        context, turn = run_program(program, context=context, return_output=True)
        x, y, direction = update_position(x, y, direction, turn)
        context['inputs'] = [panels[y][x]]
    return panels


def main():
    with open(sys.argv[1]) as fp:
        orig_program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    program = list_to_program(orig_program)
    panels = paint(program, 0)
    painted_panels = sum(len(row) for row in panels.values())
    print(painted_panels)

    program = list_to_program(orig_program)
    panels = paint(program, 1)
    rows = sorted(panels.keys())
    row_range = range(rows[0], rows[len(rows) - 1] + 1)
    top, bottom = 0, 0
    for row in rows:
        col = panels[row]
        top = min(top, min(col.keys()))
        bottom = max(bottom, max(col.keys()))
    col_range = range(top, bottom + 1)
    for y in row_range:
        for x in col_range:
            print('+' if panels[y][x] else ' ', end='')
        print('')


if __name__ == '__main__':
    main()

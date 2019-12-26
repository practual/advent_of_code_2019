from collections import defaultdict
from itertools import zip_longest


def add(program, param0, param1, param2, context):
    input1 = read_value(program, *param0, context)
    input2 = read_value(program, *param1, context)
    output_val = input1 + input2
    write_value(program, *param2, output_val, context)


def multiply(program, param0, param1, param2, context):
    input1 = read_value(program, *param0, context)
    input2 = read_value(program, *param1, context)
    output_val = input1 * input2
    write_value(program, *param2, output_val, context)


def read_input(program, param0, context):
    try:
        input_val = context['inputs'].pop()
    except IndexError:
        input_val = input("INPUT:")
    write_value(program, *param0, int(input_val), context)


def output(program, param0, context):
    output_val = read_value(program, *param0, context)
    context['output'] = output_val


def jump_if_true(program, param0, param1, context):
    input1 = read_value(program, *param0, context)
    input2 = read_value(program, *param1, context)
    if input1:
        context['ptr'] = input2


def jump_if_false(program, param0, param1, context):
    input1 = read_value(program, *param0, context)
    input2 = read_value(program, *param1, context)
    if not input1:
        context['ptr'] = input2


def less_than(program, param0, param1, param2, context):
    input1 = read_value(program, *param0, context)
    input2 = read_value(program, *param1, context)
    output_val = int(input1 < input2)
    write_value(program, *param2, output_val, context)


def equals(program, param0, param1, param2, context):
    input1 = read_value(program, *param0, context)
    input2 = read_value(program, *param1, context)
    output_val = int(input1 == input2)
    write_value(program, *param2, output_val, context)


def update_base(program, param0, context):
    input1 = read_value(program, *param0, context)
    context['base'] += input1


def halt(program, *args):
    raise StopIteration


OPCODES = {
    1: (3, add),
    2: (3, multiply),
    3: (1, read_input),
    4: (1, output),
    5: (2, jump_if_true),
    6: (2, jump_if_false),
    7: (3, less_than),
    8: (3, equals),
    9: (1, update_base),
    99: (0, halt),
}


def read_value(program, param, mode, context):
    if mode == 0:
        return program[param]
    elif mode == 1:
        return param
    elif mode == 2:
        return program[param + context['base']]
    raise ValueError


def write_value(program, address, mode, value, context):
    if mode == 0:
        program[address] = value
    elif mode == 2:
        program[address + context['base']] = value
    else:
        raise ValueError


def process_opcode(raw_opcode):
    raw_opcode = str(raw_opcode)
    opcode = int(raw_opcode[-2:])
    modes = list(map(int, raw_opcode[-3::-1]))
    return opcode, modes


def run_program(program, context=None, return_output=False, raise_halt=False):
    _context = {
        'ptr': 0,
        'base': 0,
        'inputs': [],
        'output': None,
    }
    _context.update(context or {})
    context = _context
    try:
        while True:
            ptr = context['ptr']
            opcode, modes = process_opcode(program[ptr])
            num_params, instruction = OPCODES[opcode]
            params_with_modes = zip_longest(
                [program[p] for p in range(ptr + 1, ptr + num_params + 1)], modes, fillvalue=0
            )
            context['ptr'] = ptr + num_params + 1
            instruction(program, *params_with_modes, context)
            if context['output'] is not None:
                output_val = context['output']
                context['output'] = None
                if return_output:
                    return context, output_val
                else:
                    print(output_val)
    except StopIteration:
        if raise_halt:
            raise
        return context


def list_to_program(program_list):
    return defaultdict(int, {ptr: instruction for ptr, instruction in enumerate(program_list)})

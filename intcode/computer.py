from itertools import zip_longest


def add(program, *args):
    input1 = get_input(program, *args[0])
    input2 = get_input(program, *args[1])
    output_val = input1 + input2
    output_ptr = args[2][0]
    program[output_ptr] = output_val


def multiply(program, *args):
    input1 = get_input(program, *args[0])
    input2 = get_input(program, *args[1])
    output_val = input1 * input2
    output_ptr = args[2][0]
    program[output_ptr] = output_val


def read_input(program, single_input, *args):
    if single_input is not None:
        input_val = single_input
    else:
        input_val = input("INPUT:")
    program[args[0][0]] = int(input_val)


def output(program, *args):
    print(program[args[0][0]])
    return program[args[0][0]]


def jump_if_true(program, *args):
    input1 = get_input(program, *args[0])
    input2 = get_input(program, *args[1])
    if input1:
        return input2


def jump_if_false(program, *args):
    input1 = get_input(program, *args[0])
    input2 = get_input(program, *args[1])
    if not input1:
        return input2


def less_than(program, *args):
    input1 = get_input(program, *args[0])
    input2 = get_input(program, *args[1])
    output_ptr = args[2][0]
    output_val = int(input1 < input2)
    program[output_ptr] = output_val


def equals(program, *args):
    input1 = get_input(program, *args[0])
    input2 = get_input(program, *args[1])
    output_ptr = args[2][0]
    output_val = int(input1 == input2)
    program[output_ptr] = output_val


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
    99: (0, halt),
}


def get_input(program, param, mode):
    if mode == 0:
        return program[param]
    return param


def process_opcode(raw_opcode):
    raw_opcode = str(raw_opcode)
    opcode = int(raw_opcode[-2:])
    modes = list(map(int, raw_opcode[-3::-1]))
    return opcode, modes


def run_program(program, inputs=None, return_output=False, raise_halt=False, ptr=0):
    try:
        while True:
            opcode, modes = process_opcode(program[ptr])
            num_params, instruction = OPCODES[opcode]
            params_with_modes = zip_longest(
                program[ptr + 1:ptr + num_params + 1], modes, fillvalue=0
            )
            if opcode == 3:
                # Special handler for taking passed inputs from a variable rather than stdin.
                single_input = inputs.pop() if inputs else None
                new_ptr = instruction(program, single_input, *params_with_modes)
            else:
                new_ptr = instruction(
                    program,
                    *params_with_modes
                )
            if opcode != 4 and new_ptr is not None:
                ptr = new_ptr
            else:
                ptr = ptr + num_params + 1
            if opcode == 4 and return_output:
                return ptr, new_ptr
    except StopIteration:
        if raise_halt:
            raise
        return ptr

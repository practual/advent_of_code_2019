#! /usr/bin/env python

import math
import sys

def run_program(values, noun, verb):
    program = list(values)
    program[1] = noun
    program[2] = verb
    ptr = 0
    while True:
        opcode = program[ptr]
        if opcode == 99:
            return program[0]
        input1_ptr = program[ptr + 1]
        input1_val = program[input1_ptr]
        input2_ptr = program[ptr + 2]
        input2_val = program[input2_ptr]
        output_ptr = program[ptr + 3]
        if opcode == 1:
            output_val = input1_val + input2_val
        else:
            output_val = input1_val * input2_val
        program[output_ptr] = output_val
        ptr = ptr + 4 

def main():
    with open(sys.argv[1]) as fp:
        program = tuple(map(lambda x: int(x.strip()), fp.readline().split(',')))
    noun = 0
    verb = 0
    while True:
        program_output = run_program(program, noun, verb)
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

#! /usr/bin/env python

def main():
    part_1_valids = 0
    part_2_valids = 0
    for potential in range(156218, 652527):
        prev = -1
        double = False
        just_double = False
        group = 0
        for digit in str(potential):
            digit = int(digit)
            if digit < prev:
                break
            if digit == prev:
                double = True
                group += 1
                group = max(group, 2)
            else:
                if group == 2:
                    just_double = True
                group = 0
            prev = digit
        else:
            if double:
                part_1_valids += 1
                if just_double or group == 2:
                    part_2_valids += 1
    print(part_1_valids, part_2_valids)

if __name__ == '__main__':
    main()

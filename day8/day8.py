#! /usr/bin/env python

import math
import sys


def main():
    with open(sys.argv[1]) as fp:
        data = fp.read().strip()
    img_width = 25
    img_height = 6
    img_size = img_width * img_height
    num_layers = int(len(data) / img_size)
    min_zeroes = math.inf
    checksum = 0
    for layer in range(num_layers):
        counters = [0, 0, 0]
        for pixel in data[layer*img_size:(layer+1)*img_size]:
            counters[int(pixel)] += 1
        if counters[0] < min_zeroes:
            min_zeroes = counters[0]
            checksum = counters[1] * counters[2]
    print(checksum)

    data = list(map(int, data))
    img = data[:img_size]
    for layer in range(1, num_layers):
        for ptr, pixel in enumerate(data[layer*img_size:(layer+1)*img_size]):
            if img[ptr] == 2:
                img[ptr] = pixel
    for ptr, pixel in enumerate(img):
        print('+' if pixel == 1 else ' ', end='')
        if not (ptr + 1) % img_width:
            print('')


if __name__ == '__main__':
    main()

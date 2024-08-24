#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import argparse

np.set_printoptions(threshold=np.inf)
np.set_printoptions(precision=0)
np.set_printoptions(linewidth=200)

parser=argparse.ArgumentParser()
parser.add_argument("file",
                    help="Name of the Flipper IR file")
parser.add_argument("num",
                    type=int,
                    help="Number of signals to plot")
args = parser.parse_args()

LEN_SIGNAL = 180
TICK = 800

signals = np.zeros((args.num, LEN_SIGNAL), dtype=np.uint8)
i = 0

with open(args.file, 'r') as file:
    for line in file:
        if not line.startswith("data"):
            continue
        line = line[6:]
        arr = line.split(' ')
        j = 0
        one_or_zero = True
        sum = 0
        for item in arr:
            sum += int(item)
            ticks = round(int(item) / TICK)
            for _ in range(ticks):
                if (one_or_zero):
                    signals[i, j] = 1
                else:
                    signals[i, j] = 0
                j += 1
            one_or_zero = not one_or_zero
        #print(round(sum / TICK))
        #print('')
        i += 1
        if (i >= args.num):
            break

#print(signals)

for i in range(args.num):
    plt.plot(signals[i])
plt.show()
plt.close()

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
args = parser.parse_args()

LEN_SIGNAL = 180
TICK_US = 800

signals = []

# read data from flipper file
with open(args.file, 'r') as file:
    for line in file:
        if not line.startswith("data"):
            continue
        new_signal = np.zeros((LEN_SIGNAL), dtype=np.uint8)
        line = line[6:].strip()
        arr = line.split(' ')
        one_or_zero = True
        i = 0
        for item in arr:
            # convert lengths to binary
            ticks = round(int(item) / TICK_US)
            for _ in range(ticks):
                if (one_or_zero):
                    new_signal[i] = 1
                else:
                    new_signal[i] = 0
                i += 1
            one_or_zero = not one_or_zero
        signals.append(new_signal)

# plot signals
for i in range(len(signals)):
    plt.plot(signals[i])
plt.show()
plt.close()

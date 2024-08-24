#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(threshold=np.inf)
np.set_printoptions(precision=0)
np.set_printoptions(linewidth=200)

NUM_LINES = 89
LEN_SIGNAL = 180
TICK = 800
FILE = "./decimal.ir"

signals = np.zeros((NUM_LINES, LEN_SIGNAL), dtype=np.uint8)
i = 0

with open(FILE, 'r') as file:
    for line in file:
        arr = line.split(' ')
        j = 0
        one_or_zero = True
        sum = 0
        for item in arr:
            sum += int(item)
            x = round(int(item) / TICK)
            for _ in range(x):
                if (one_or_zero):
                    signals[i, j] = 1
                else:
                    signals[i, j] = 0
                j += 1
            one_or_zero = not one_or_zero
            #print(x, end=' ')
        print(round(sum / TICK))
        print('')
        i += 1
        if (i >= NUM_LINES): break

print(signals[:, 108:])
#print(signals[65:, 108:])

for i in range(NUM_LINES):
    plt.plot(signals[i])
plt.show()
plt.close()

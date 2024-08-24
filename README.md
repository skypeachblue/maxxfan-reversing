# Airxcel MaxxAir MaxxFan Deluxe - IR Remote Reversing

Carrier frequency: 38kHz

## Dependencies
* bitstring
* argparse
* matplotlib
* numpy

## Usage
plot.py can be used to print IR signals captured by the Flipper Zero.

Usage:

    python3 plot.py <filename> <number of signals>

Example:

    python3 plot.py ./Maxxfan_collection.ir 97


generate.py can be used to generate IR signals for the Flipper Zero to send. The signal name can be chosen arbitrarily.

Usage:

    python3 generate.py <arguments> <signal_name>

Examples:

    python3 generate.py --off maxxfan_off  // turn maxxfan off

    python3 generate.py --auto --temp 18 auto_18C // enable automatic mode and set temperature to 18C

    python3 generate.py --open --air_out --speed 30 manual_30p // manual mode, open lid, air out, 30% fan speed

*Keep in mind that this can be used to generate signals which the original remote doesn't allow (e.g. fan spinning with lid closed), so use at your own risk :)*

## Background

As a first step I collected ~90 signals using the Flipper Zero.

<img src=img/signals.png width=600>

Plotting these signals, it became apparent that a large part of the signal always stays the same.
Only four parts of the signal (seven bits each) actually change.


##### State:

The first block of 7 bits encodes the state of the fan:

    0 1 1 0 1 1 1  # Manual mode, Open, Air in
    0 1 0 0 1 1 1  # Manual mode, Open, Air out
    0 0 1 1 1 1 1  # Manual mode, Closed
    1 0 1 1 0 1 1  # Automatic mode, Air in
    1 0 0 1 0 1 1  # Automatic mode, Air out
    1 1 1 1 1 1 1  # Off


##### Fan Speed:

For the fan speed there are only 10 possibilities (10% - 100%).
I'm not sure how this value is encoded here, so I enumerated all possibilities:

    1 0 1 0 1 1 1  # 10%
    1 1 0 1 0 1 1  # 20%
    1 0 0 0 0 1 1  # 30%
    1 1 1 0 1 0 1  # 40%
    1 0 1 1 0 0 1  # 50%
    1 1 0 0 0 0 1  # 60%
    1 0 0 1 1 1 0  # 70%
    1 1 1 1 0 1 0  # 80%
    1 0 1 0 0 1 0  # 90%
    1 1 0 1 1 0 0  # 100%


##### Temperature:

There are 40 possible temperatures for the automatic mode (-2C - 37C).
Again, I'm not sure how these values are encoded so I enumerated all possibilities.
(Can be found [here](generate.py#L33)).


##### Check sum:

Figuring out how the check sum is calculated was a bit tricky.
Through some trial and error I was able to determine this:

    checksum[0] = state[0] XOR speed[0] XOR temperature[0]
    checksum[1] = state[1] XOR speed[1] XOR temperature[1]
    checksum[2] = NOT (state[2] XOR speed[2] XOR temperature[2])
    checksum[3] = NOT (state[3] XOR speed[3] XOR temperature[3])
    checksum[4] = NOT (state[4] XOR speed[4] XOR temperature[4])
    checksum[5] = state[5] XOR speed[5] XOR temperature[5]
    checksum[6] = NOT (state[6] XOR speed[6] XOR temperature[6])

(where 0 is the leftmost bit)

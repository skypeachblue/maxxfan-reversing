# Airxcel MaxxAir MaxxFan Deluxe - IR Remote Control Reverse Engineering

This repo documents the results of reverse engineering the [MaxxFan Deluxe 07500K](https://www.maxxair.com/products/fans/maxxfan-deluxe-00-07500K/) remote control, in order to be able to control the MaxxFan in other ways.

The carrier frequency of the signal is 38kHz.

## Dependencies
* bitstring
* argparse
* matplotlib
* numpy

## Usage

**Keep in mind that this can be used to generate signals which the original remote doesn't allow (e.g. fan spinning with lid closed), so use at your own risk :)**

`plot.py` can be used to print IR signals captured by the Flipper Zero.

Usage:

    python3 plot.py <filename> <number of signals>

Example:

    python3 plot.py ./Maxxfan_collection.ir 97


`generate.py` can be used to generate IR signals for the Flipper Zero to send. The signal name can be chosen arbitrarily.

Usage:

    python3 generate.py <arguments> <signal_name>

Examples:

    python3 generate.py --off maxxfan_off  // turn maxxfan off

    python3 generate.py --auto --temp 18 auto_18C // enable automatic mode and set temperature to 18C

    python3 generate.py --open --air_out --speed 30 manual_30p // manual mode, open lid, air out, 30% fan speed
    
For automatic mode, the `temp` argument is required, `air_in` is optional (default is `air_out`).  
For manual mode, `open`/`close`, `air_in`/`air_out` and `speed` are required.  
When the fan is off, the lid is closed by default. `open` can be specified optionally to turn the fan off with the lid open.


## Background

As a first step I collected 90+ signals with a Flipper Zero.

<img src=img/signals.png width=800>

Plotting these signals, it becomes apparent that a large part of the signal always stays the same.
Only four parts of the signal (7 bits each) actually change.


##### State:
The first block of 7 bits encodes the state of the fan:

    0 1 1 0 1 1 1  # Manual mode, Open, Air in
    0 1 0 0 1 1 1  # Manual mode, Open, Air out
    0 0 1 1 1 1 1  # Manual mode, Closed
    1 0 1 1 0 1 1  # Automatic mode, Air in
    1 0 0 1 0 1 1  # Automatic mode, Air out
    1 1 1 1 1 1 1  # Off, Lid closed
    1 1 1 0 1 1 1  # Off, Lid open


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
Again, I'm not sure how these values are encoded so I enumerated all possibilities:

    0 1 0 0 0 1 1  # -2      0 0 1 1 0 0 1  # 11     0 0 1 0 1 1 0  # 24
    0 0 0 0 0 1 1  # -1      0 1 0 1 0 0 1  # 12     0 1 0 0 1 1 0  # 25
    1 1 1 1 1 0 1  # 0       0 0 0 1 0 0 1  # 13     1 0 0 0 1 1 0  # 26
    0 1 1 1 1 0 1  # 1       0 1 1 0 0 0 1  # 14     1 1 1 1 0 1 0  # 27
    0 0 1 1 1 0 1  # 2       0 0 1 0 0 0 1  # 15     1 0 1 1 0 1 0  # 28
    0 1 0 1 1 0 1  # 3       1 1 0 0 0 0 1  # 16     1 1 0 1 0 1 0  # 29
    0 0 0 1 1 0 1  # 4       1 0 0 0 0 0 1  # 17     1 0 0 1 0 1 0  # 30
    0 1 1 0 1 0 1  # 5       1 1 1 1 1 1 0  # 18     0 0 0 1 0 1 0  # 31
    1 0 1 0 1 0 1  # 6       1 0 1 1 1 1 0  # 19     0 1 1 0 0 1 0  # 32
    1 1 0 0 1 0 1  # 7       1 1 0 1 1 1 0  # 20     0 0 1 0 0 1 0  # 33
    1 0 0 0 1 0 1  # 8       0 1 0 1 1 1 0  # 21     0 1 0 0 0 1 0  # 34
    1 1 1 1 0 0 1  # 9       0 0 0 1 1 1 0  # 22     0 0 0 0 0 1 0  # 35
    1 0 1 1 0 0 1  # 10      0 1 1 0 1 1 0  # 23     1 1 1 1 1 0 0  # 36
                                                     1 0 1 1 1 0 0  # 37


##### Checksum:
Figuring out how the checksum is calculated was a bit tricky.
Through some trial and error I was able to determine this:

    checksum[0] = state[0] XOR speed[0] XOR temperature[0]
    checksum[1] = state[1] XOR speed[1] XOR temperature[1]
    checksum[2] = NOT (state[2] XOR speed[2] XOR temperature[2])
    checksum[3] = NOT (state[3] XOR speed[3] XOR temperature[3])
    checksum[4] = NOT (state[4] XOR speed[4] XOR temperature[4])
    checksum[5] = state[5] XOR speed[5] XOR temperature[5]
    checksum[6] = NOT (state[6] XOR speed[6] XOR temperature[6])

(where 0 is the leftmost bit)

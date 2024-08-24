# MaxxAir MaxxFan Deluxe Reversing

## Use at your own risk :)

### Dependencies
* bitstring
* argparse
* matplotlib
* numpy

### Usage
plot.py can be used to print IR signals captured using the Flipper Zero.

Usage:
    python3 plot.py <filename> <number of signals>
Example:
    python3 plot.py ./Maxxfan_collection.ir 80


generate.py can be used to generate IR signals for the Flipper Zero to send.

Usage:

    `python3 generate.py <arguments> signal_name`

Examples:

    `python3 generate.py --off off  // turn maxxfan off`

    `python3 generate.py --auto --temp 18 // enable automatic mode, temperature=18C`

    `python3 generate.py --open --air_out --speed 30 // manual mode, open lid, air out, 30% fan speed`




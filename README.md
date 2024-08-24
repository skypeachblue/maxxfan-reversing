# MaxxAir MaxxFan Deluxe Reversing - Use at your own risk :)

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

## Background

![Plot of Signals](https://gitlab.bjoern-b.de/julia/maxxair-reversing/-/raw/main/img/signals.png)

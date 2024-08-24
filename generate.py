#!/usr/bin/env python3

import argparse
from bitstring import BitArray

states = {
    "auto"   : BitArray(bin="1001011"),
    "open"   : BitArray(bin="0100111"),
    "closed" : BitArray(bin="0001111"),
    "air_in" : BitArray(bin="0010111"),
    "air_out": BitArray(bin="0000111"),
    "off"    : BitArray(bin="1111111"),
}

fan_speeds = {
    "10" : BitArray(bin="1010111"),
    "20" : BitArray(bin="1101011"),
    "30" : BitArray(bin="1000011"),
    "40" : BitArray(bin="1110101"),
    "50" : BitArray(bin="1011001"),
    "60" : BitArray(bin="1100001"),
    "70" : BitArray(bin="1001110"),
    "80" : BitArray(bin="1111010"),
    "90" : BitArray(bin="1010010"),
    "100": BitArray(bin="1101100")
}

temperatures = {
    "-2": BitArray(bin="0100011"),
    "-1": BitArray(bin="0000011"),
    "0 ": BitArray(bin="1111101"),
    "1 ": BitArray(bin="0111101"),
    "2 ": BitArray(bin="0011101"),
    "3 ": BitArray(bin="0101101"),
    "4 ": BitArray(bin="0001101"),
    "5 ": BitArray(bin="0110101"),
    "6 ": BitArray(bin="1010101"),
    "7 ": BitArray(bin="1100101"),
    "8 ": BitArray(bin="1000101"),
    "9 ": BitArray(bin="1111001"),
    "10": BitArray(bin="1011001"),
    "11": BitArray(bin="0011001"),
    "12": BitArray(bin="0101001"),
    "13": BitArray(bin="0001001"),
    "14": BitArray(bin="0110001"),
    "15": BitArray(bin="0010001"),
    "16": BitArray(bin="1100001"),
    "17": BitArray(bin="1000001"),
    "18": BitArray(bin="1111110"),
    "19": BitArray(bin="1011110"),
    "20": BitArray(bin="1101110"),
    "21": BitArray(bin="0101110"),
    "22": BitArray(bin="0001110"),
    "23": BitArray(bin="0110110"),
    "24": BitArray(bin="0010110"),
    "25": BitArray(bin="0100110"),
    "26": BitArray(bin="1000110"),
    "27": BitArray(bin="1111010"),
    "28": BitArray(bin="1011010"),
    "29": BitArray(bin="1101010"),
    "30": BitArray(bin="1001010"),
    "31": BitArray(bin="0001010"),
    "32": BitArray(bin="0110010"),
    "33": BitArray(bin="0010010"),
    "34": BitArray(bin="0100010"),
    "35": BitArray(bin="0000010"),
    "36": BitArray(bin="1111100"),
    "37": BitArray(bin="1011100")
}

parser=argparse.ArgumentParser()
parser.add_argument("--auto",
                    action="store_true",
                    help="Enable automatic mode (requires temperature)")
parser.add_argument("--temp",
                    help="Set Temperature (-2 to 37) for automatic mode, ignored in manual mode")
parser.add_argument("--speed",
                    help="Set fan speed in percent {10,20,30,40,50,60,70,80,90,100}, ignored in automatic mode")
parser.add_argument("--open",
                    action="store_true",
                    help="Open lid, ignored in automatic mode")
parser.add_argument("--close",
                    action="store_true",
                    help="Close lid, ignored in automatic mode")
parser.add_argument("--air_in",
                    action="store_true",
                    help="Air in")
parser.add_argument("--air_out",
                    action="store_true",
                    help="Air out")
parser.add_argument("--off",
                    action="store_true",
                    help="Turn off (ignores all other arguments)")

args=parser.parse_args()

if (args.auto and not args.temp):
    exit("You need to specify a temperature")
if (args.temp and not args.auto):
    exit("You need to enable automatic mode")
if (args.open and args.close):
    exit("Open and close are mutually exclusive")
if (args.air_in and args.air_out):
    exit("Air in and out are mutually exclusive")
if (not args.auto and ((not args.open and not args.close) or (not args.air_in and not args.air_out) or not args.speed) and not args.off):
    exit("For manual mode you need to specify open/close and air in/out and fan speed")
if args.speed:
    found_speed = False
    for speed in fan_speeds:
        if speed == args.speed:
            found_speed = True
            break
    if not found_speed:
        exit("Invalid fan speed")
if args.temp:
    found_temp = False
    for temp in temperatures:
        if temp == args.temp:
            found_temp = True
            break
    if not found_temp:
        exit("Invalid temperature")

LEN_SIGNAL = 180
TICK = 800
DEFAULT_TEMP = "20"
DEFAULT_FANSPEED = "20"

start = BitArray(bin="110100101001010110100011111111000100000001001111111010010000001000111111011001000001000011111011100111001100001")
state = BitArray(bin="0000000")
seperator = BitArray(bin="1001")
fan_speed = BitArray(bin="1000001")
temperature = BitArray(bin="0000000")
idk = BitArray(bin="000000000010011101")
check_sum = BitArray(bin="0000000")
end = BitArray(bin="0000000")



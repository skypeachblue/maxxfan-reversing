#!/usr/bin/env python3

import argparse
from bitstring import BitArray

TICK_US = 800
DEFAULT_TEMP = "20"
DEFAULT_FANSPEED = "20"

states = {
    "auto"   : BitArray(bin="1001011"),
    "manual" : BitArray(bin="0000111"),
    "open"   : BitArray(bin="0100000"),
    "air_in" : BitArray(bin="0010000"),
    "closed" : BitArray(bin="0001000"),
    "off"    : BitArray(bin="1111111"),
    #"air_out": BitArray(bin="0000000"),
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
    "0" : BitArray(bin="1111101"),
    "1" : BitArray(bin="0111101"),
    "2" : BitArray(bin="0011101"),
    "3" : BitArray(bin="0101101"),
    "4" : BitArray(bin="0001101"),
    "5" : BitArray(bin="0110101"),
    "6" : BitArray(bin="1010101"),
    "7" : BitArray(bin="1100101"),
    "8" : BitArray(bin="1000101"),
    "9" : BitArray(bin="1111001"),
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
parser.add_argument("name",
                    help="Name for the signal in flipper file")
parser.add_argument("--auto",
                    action="store_true",
                    help="Enable automatic mode (requires temperature). Default: air_out")
parser.add_argument("--temp",
                    help="Set Temperature (-2 to 37) for automatic mode, ignored in manual mode")
parser.add_argument("--speed",
                    help="Set fan speed in percent (one of 10,20,30,40,50,60,70,80,90,100), ignored in automatic mode")
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
                    help="Turn fan off (ignores other arguments except for open/close)")
args = parser.parse_args()

if (args.auto and not args.temp):
    exit("You need to specify a temperature")
if (args.temp and not args.auto):
    exit("Temperature is only valid in automatic mode")
if (args.open and args.close):
    exit("Open and close are mutually exclusive")
if (args.air_in and args.air_out):
    exit("Air in and out are mutually exclusive")
if (not args.auto and ((not args.open and not args.close) or (not args.air_in and not args.air_out) or not args.speed) and not args.off):
    exit("For manual mode you need to specify open/close, air_in/out and fan speed")
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


def gen_signal():
    signal = BitArray(bin="")
    start = BitArray(bin="110100101001010110100011111111000100000001001111111010010000001000111111011001000001000011111011100111001100001")
    state = BitArray(bin="0000000")
    separator = BitArray(bin="1001")
    speed = BitArray(bin="1000001")
    temp = BitArray(bin="0000000")
    unknown = BitArray(bin="000000000010011101")
    checksum = BitArray(bin="0000000")
    end = BitArray(bin="0000000")

    if (args.auto):
        # automatic mode: set state and temperature and air in/out
        state = states["auto"]
        if (args.air_in):
            state = state.__ior__(states["air_in"])
        speed = fan_speeds[DEFAULT_FANSPEED]
        temp = temperatures[args.temp]
    elif (args.off):
        # turn fan off
        state = states["off"]
        if (args.open):
            state[3] = 0
        speed = fan_speeds[DEFAULT_FANSPEED]
        temp = temperatures[DEFAULT_TEMP]
    else:
        # manual mode: set state, speed and temperature
        state = states["manual"]
        if (args.open):
            state = state.__ior__(states["open"])
        else:
            state = state.__ior__(states["closed"])
        if (args.air_in):
            state = state.__ior__(states["air_in"])
        speed = fan_speeds[args.speed]
        temp = temperatures[DEFAULT_TEMP]

    # calculate checksum
    checksum[0] = (state[0] ^ speed[0] ^ temp[0])
    checksum[1] = (state[1] ^ speed[1] ^ temp[1])
    checksum[2] = not (state[2] ^ speed[2] ^ temp[2])
    checksum[3] = not (state[3] ^ speed[3] ^ temp[3])
    checksum[4] = not (state[4] ^ speed[4] ^ temp[4])
    checksum[5] = (state[5] ^ speed[5] ^ temp[5])
    checksum[6] = not (state[6] ^ speed[6] ^ temp[6])

    signal.append(start)
    signal.append(state)
    signal.append(separator)
    signal.append(speed)
    signal.append(separator)
    signal.append(temp)
    signal.append(separator)
    signal.append(unknown)
    signal.append(separator)
    signal.append(checksum)
    signal.append(end)
    print(state.bin)
    return signal

def bin_to_flipper(binary, name):
    ret = f"Filetype: IR signals file\nVersion: 1\n#\nname: {name}\ntype: raw\nfrequency: 38000\nduty_cycle: 0.330000\ndata: "
    one_or_zero = 1
    num_ticks = 0
    for i in range(len(binary)):
        if (int(binary[i]) == one_or_zero):
            num_ticks += 1
        else:
            ret += str(num_ticks * TICK_US)
            ret += " "
            one_or_zero = 1 - one_or_zero # swap 0 / 1
            num_ticks = 1
    return ret

if __name__ == '__main__':
    signal = gen_signal()
    #print(signal.bin)
    #print("")
    flipper = bin_to_flipper(signal.bin, args.name)
    print(flipper)

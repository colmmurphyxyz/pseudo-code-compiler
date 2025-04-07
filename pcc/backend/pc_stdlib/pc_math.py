# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import math


def floor(a) -> int:
    return math.floor(a)

def ceil(a) -> int:
    return math.ceil(a)

def min(a, b):
    if a < b:
        return a
    return b

def min(*args):
    if len(args) == 0:
        raise ValueError("min() requires at least one argument")
    if len(args) == 1:
        return args[0]
    min_value = args[0]
    for arg in args[1:]:
        if arg < min_value:
            min_value = arg
    return min_value

def max(a, b):
    if a > b:
        return a
    return b

def max(*args):
    if len(args) == 0:
        raise ValueError("max() requires at least one argument")
    if len(args) == 1:
        return args[0]
    max_value = args[0]
    for arg in args[1:]:
        if arg > max_value:
            max_value = arg
    return max_value

def abs(a):
    if a < 0:
        return -a
    return a
# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pathlib
import sys
# add the source directory to sys.path. This is not a permanent solution
# sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from backend.pc_stdlib import *
from debugger.web_db import set_trace
set_trace(path=__file__, pc_source_code='''CUT-ROD(p, n)
    if n == 0
        return 0
    q = float("-inf")
    for i = 1 to n
        q = max(q, p[i] + CUT-ROD(p, n - i))
    return q

MEMOIZED-CUT-ROD(p, n)
    let r[0:n] be a new array
    for i = 0 to n
        r[i] = float("-inf")
    return MEMOIZED-CUT-ROD-AUX(p, n, r)

MEMOIZED-CUT-ROD-AUX(p, n, r)
    if r[n] >= 0
        return r[n]
    if n == 0
        q = 0
    else q = float("-inf")
        for i = 1 to n
            q = max(q, p[i] + MEMOIZED-CUT-ROD(p, n - i, r))
    r[n] = q
    return q

BOTTOM-UP-CUT-ROD(p, n)
    let r[0:n] be a new array
    r[0] = 0
    for j = 1 to n
        q = float("-inf")
        for i = 1 to j
            q = max(q, p[i] + r[j - i])
        r[j] = q
    return r[n]

let prices[1:10] be a new array
prices[1] = 1
prices[2] = 5
prices[3] = 8
prices[4] = 9
prices[5] = 12
prices[6] = 17
prices[7] = 17
prices[8] = 20
prices[9] = 24
prices[10] = 30
n = 4
max-price = CUT-ROD(prices, n)
print max-price
''')

def CUT_ROD(p, n): # l:1 
    if n == 0: # l:2 
        return 0 # l:3 
    
    q = float("-inf") # l:4 
    for i in range(1, n + 1): # l:5 
        q = max(q, p[i] + CUT_ROD(p, n - i)) # l:6 
    return q # l:7 

def MEMOIZED_CUT_ROD(p, n): # l:9 
    r = PcArray(0, n); # l:10 
    for i in range(0, n + 1): # l:11 
        r[i] = float("-inf") # l:12 
    return MEMOIZED_CUT_ROD_AUX(p, n, r) # l:13 

def MEMOIZED_CUT_ROD_AUX(p, n, r): # l:15 
    if r[n] >= 0: # l:16 
        return r[n] # l:17 
    
    if n == 0: # l:18 
        q = 0 # l:19 
    
    else:
        q = float("-inf") # l:20  # l:20
        for i in range(1, n + 1): # l:21 
            q = max(q, p[i] + MEMOIZED_CUT_ROD_AUX(p, n - i, r)) # l:22
    r[n] = q # l:23 
    return q # l:24 

def BOTTOM_UP_CUT_ROD(p, n): # l:26 
    r = PcArray(0, n); # l:27 
    r[0] = 0 # l:28 
    for j in range(1, n + 1): # l:29 
        q = float("-inf") # l:30 
        for i in range(1, j + 1): # l:31 
            q = max(q, p[i] + r[j - i]) # l:32 
        r[j] = q # l:33 
    return r[n] # l:34 

prices = PcArray(1, 10); # l:36 
prices[1] = 1 # l:37 
prices[2] = 5 # l:38 
prices[3] = 8 # l:39 
prices[4] = 9 # l:40 
prices[5] = 12 # l:41 
prices[6] = 17 # l:42 
prices[7] = 17 # l:43 
prices[8] = 20 # l:44 
prices[9] = 24 # l:45 
prices[10] = 30 # l:46 
rod_length = 4 # l:47
max_price = MEMOIZED_CUT_ROD(prices, rod_length) # l:48
print(max_price) # l:49 

# add the source directory to sys.path. This is not a permanent solution
# sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from backend.pc_stdlib import PcArray
# set_trace()
from debugger.web_db import set_trace
set_trace(pc_source_code='''// Section 2.1
INSERTION-SORT(A, n)
    for i = 2 to n
        key = A[i]
        // Insert A[i] into the sorted subarray A[1:i-1]
        j = i - 1
        while j > 0 and A[j] > key
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key

let A[1:5] be a new array
for i = 1 to 5
    A[i] = 6 - i
print A
INSERTION-SORT(A, 5)
print A
''')

def INSERTION_SORT(A, n): # l:2 
    for i in range(2, n + 1): # l:3 
        key = A[i] # l:4 
        j = i - 1 # l:6 
        while j > 0 and A[j] > key: # l:7 
            A[j + 1] = A[j] # l:8 
            j = j - 1 # l:9 
        A[j + 1] = key # l:10 
A = PcArray(1, 5); # l:12
for i in range(1, 5 + 1): # l:13
    A[i] = 6 - i # l:14 
print(A) # l:15 
INSERTION_SORT(A, 5) # l:16 
print(A) # l:17 

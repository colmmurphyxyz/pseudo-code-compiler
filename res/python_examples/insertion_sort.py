def INSERTION_SORT(A, n):
    for i in range(2, n + 1):
        key = A[i]
        # insert A[i] into the sorted subarray A[1:i-1]
        j = i - 1
        while j > 0 and A[j] > key:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key

A = [None, 5, 4, 3, 2, 1]
INSERTION_SORT(A, 5)
print(A)
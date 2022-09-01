import math, sys, os
try:
    from src.node_benchmark.tests.helpers import timeit
except ImportError as e:
    from tests.helpers import timeit

_num = 10000000

@timeit
def jump_search(*args, **kwargs) -> int:
    arr = list(range(_num))
    x = arr[-1]
    n = len(arr)
    step = int(math.floor(math.sqrt(n)))
    prev = 0
    while arr[min(step, n) - 1] < x:
        prev = step
        step += int(math.floor(math.sqrt(n)))
        if prev >= n:
            return -1

    while arr[prev] < x:
        prev = prev + 1
        if prev == min(step, n):
            return -1
    if arr[prev] == x:
        return prev
    return -1

@timeit
def fibonacci_search(*args, **kwargs):
    arr = list(range(_num))
    x = arr[-1]
    fibM_minus_2 = 0
    fibM_minus_1 = 1
    fibM = fibM_minus_1 + fibM_minus_2
    while (fibM < len(arr)):
        fibM_minus_2 = fibM_minus_1
        fibM_minus_1 = fibM
        fibM = fibM_minus_1 + fibM_minus_2
    index = -1
    while (fibM > 1):
        i = min(index + fibM_minus_2, (len(arr)-1))
        if (arr[i] < x):
            fibM = fibM_minus_1
            fibM_minus_1 = fibM_minus_2
            fibM_minus_2 = fibM - fibM_minus_1
            index = i
        elif (arr[i] > x):
            fibM = fibM_minus_2
            fibM_minus_1 = fibM_minus_1 - fibM_minus_2
            fibM_minus_2 = fibM - fibM_minus_1
        else :
            return i
    if(fibM_minus_1 and index < (len(arr)-1) and arr[index+1] == x):
        return index+1
    return -1


@timeit
def linear_search(*args, **kwargs) -> int:
    arr = list(range(_num//2))
    target = arr[-1]
    for index, item in enumerate(arr):
        if item == target:
            return index
    return -1

@timeit
def Binary_search(*args, **kwargs):
    arr = list(range(_num))
    target = arr[-1]
    first = 0
    last = len(arr)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first+last)//2
        if arr[mid] == target:
            index = mid
        else:
            if target<arr[mid]:
                last = mid -1
            else:
                first = mid +1
    return index

if __name__ == '__main__':    
    import random
    sys.path.append(os.path.join(os.getcwd(), './tests'))
    r = 10000000
    jump_search()
    Binary_search()
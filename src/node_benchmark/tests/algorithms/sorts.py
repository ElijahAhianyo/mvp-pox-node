import random, sys, os
sys.path.append(os.path.join(os.getcwd(), './tests'))
try:
    from src.node_benchmark.tests.helpers import timeit
except ImportError as e:
    from tests.helpers import timeit


@timeit
def bubble_sort(collection):
    collection = collection[:len(collection)//2]
    length = len(collection)
    for i in range(length - 1):
        swapped = False
        for j in range(length - 1 - i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break 
    return collection

@timeit
def bogo_sort(collection):
    collection = collection[:len(collection)//5]
    def is_sorted(collection):
        if len(collection) < 2:
            return True
        for i in range(len(collection) - 1):
            if collection[i] > collection[i + 1]:
                return False
        return True

    while not is_sorted(collection):
        random.shuffle(collection)
    return collection

@timeit
def double_sort(collection):
    collection = collection[:len(collection)//5]
    no_of_elements = len(collection)
    for i in range(0, int(((no_of_elements - 1) / 2) + 1)): 
        for j in range(0, no_of_elements - 1):
            if collection[j + 1] < collection[j]:  
                temp = collection[j + 1]
                collection[j + 1] = collection[j]
                collection[j] = temp
            if(collection[no_of_elements - 1 - j] < collection[no_of_elements - 2 - j]): 
                temp = collection[no_of_elements - 1 - j]
                collection[no_of_elements - 1 - j] = collection[no_of_elements - 2 - j]
                collection[no_of_elements - 2 - j] = temp
    return collection

@timeit
def pancake_sort(collection):
    cur = len(collection)
    while cur > 1:
        mi = collection.index(max(collection[0:cur]))
        collection = collection[mi::-1] + collection[mi + 1 : len(collection)]
        collection = collection[cur - 1 :: -1] + collection[cur : len(collection)]
        cur -= 1
    return collection

@timeit 
def pigeonhole_sort(collection):
    min_val = min(collection)  
    max_val = max(collection)  
    size = max_val - min_val + 1 
    holes = [0] * size

    for x in collection:
        assert isinstance(x, int), "integers only please"
        holes[x - min_val] += 1
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            collection[i] = count + min_val
            i += 1
    return collection

if __name__ == '__main__':
    import time, threading
    limit = 100
    _list = [random.randint(0, limit) for i in range(limit)]
    print(_list)

    t = time.time()
    double_sort(_list.copy())
    print(time.time() - t)

    print()
    t = time.time()
    thread = threading.Thread(target = double_sort, args = (_list.copy(), ))
    thread.start()
    thread.join()
    print(time.time() - t)


from random import randint
import timeit
from matplotlib import pyplot
from functools import partial


def binsearch(nums, n):
    lo, hi = 0, len(nums)
    while hi > lo:
        mid = (lo + hi) // 2   # still in range [lo, hi)
        x = nums[mid]
        if x == n:
            return mid
        if n < x:
            hi = mid
        if n > x:
            lo = mid + 1
    return None


def iterSearch(nums, n):
    for i in range(len(nums)):
        if nums[i] == n:
            return i
    return None


def numsGenerator(size):
    return sorted(randint(0, 10000) for _ in range(size))


if __name__ == '__main__':
    sizes = range(1, 1000)
    bintiming, itertiming = [], []
    runs = 3
    for size in sizes:
        nums = numsGenerator(size)
        x = nums[randint(0, size - 1)]
        x = nums[-1]
        x = -2
        bt = min(timeit.Timer(partial(binsearch, nums, x))
                 .repeat(repeat=3, number=runs))
        lt = min(timeit.Timer(partial(iterSearch, nums, x))
                 .repeat(repeat=3, number=runs))
        bintiming.append(bt)
        itertiming.append(lt)

    pyplot.plot(sizes, bintiming, label='binary search')
    pyplot.plot(sizes, itertiming, label='iterative search')
    pyplot.legend()
    pyplot.show()

import random
import timeit
from functools import partial
from matplotlib import pyplot


def merge_sort(arr: list[int]) -> list[int]:
    nums = arr.copy()
    if (len(nums) <= 1):
        return nums

    working = [None for _ in range(len(nums))]

    def merge(start: int, mid: int, end: int):
        li = start
        ri = mid
        for i in range(start, end):
            if li >= mid:
                working[i] = nums[ri]
                ri += 1
            elif ri >= end:
                working[i] = nums[li]
                li += 1
            elif nums[li] < nums[ri]:
                working[i] = nums[li]
                li += 1
            else:
                working[i] = nums[ri]
                ri += 1
        for i in range(start, end):
            nums[i] = working[i]

    def sort(start: int, end: int):
        """
        Sort from [start, end)
        """
        length = end - start
        if length <= 1:
            return
        mid = (start + end) // 2

        sort(start, mid)
        sort(mid, end)
        return merge(start, mid, end)

    sort(0, len(nums))
    return nums


def quicksort(arr):
    nums = arr.copy()

    def sort(start, end):
        if end - start <= 1:
            return

        m = random.randint(start, end - 1)
        nums[start], nums[m] = nums[m], nums[start]
        m = start

        for i in range(start + 1, end):
            if nums[i] < nums[start]:
                nums[m + 1], nums[i] = nums[i], nums[m + 1]
                m += 1
        nums[start], nums[m] = nums[m], nums[start]
        sort(start, m)
        sort(m + 1, end)

    sort(0, len(nums))
    return nums


if __name__ == '__main__':
    maxN = 15000
    repeat = 3
    runs = 5
    step_size = 40

    merge_timings_duplicates = []
    merge_timings_distinct = []
    quick_timings_duplicates = []
    quick_timings_distinct = []
    for n in range(1, maxN, step_size):
        print(f"n = {n}")
        nums_duplicate = [random.randint(10, 80) for _ in range(n)]
        nums_distinct = [random.randint(10, 80000) for _ in range(n)]

        merge_timings_duplicates.append(min(timeit.Timer(partial(merge_sort, nums_duplicate)).repeat(repeat, runs)))
        merge_timings_distinct.append(min(timeit.Timer(partial(merge_sort, nums_distinct)).repeat(repeat, runs)))

        quick_timings_duplicates.append(min(timeit.Timer(partial(quicksort, nums_duplicate)).repeat(repeat, runs)))
        quick_timings_distinct.append(min(timeit.Timer(partial(quicksort, nums_distinct)).repeat(repeat, runs)))

    pyplot.plot(range(1, maxN, step_size), merge_timings_duplicates, label='Merge sort (with duplicates)')
    pyplot.plot(range(1, maxN, step_size), merge_timings_distinct, label='Merge sort (with distinct)')
    pyplot.plot(range(1, maxN, step_size), quick_timings_duplicates, label='Quick sort (with duplicates)')
    pyplot.plot(range(1, maxN, step_size), quick_timings_distinct, label='Quick sort (with distinct)')
    pyplot.legend()
    pyplot.show()

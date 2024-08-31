import random


def merge_sort(nums: list[int]) -> list[int]:
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


if __name__ == '__main__':
    arr_size = random.randint(0, 20)
    arr = [random.randint(-10, 30) for _ in range(arr_size)]

    print("Sorting", arr)
    assert sorted(arr) == merge_sort(arr)
    print("Done!")

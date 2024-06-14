def main(nums, n):
    start = 0
    end = len(nums) - 1
    while start <= end:
        mid = (start + end) // 2
        x = nums[mid]
        if x == n:
            return mid
        if x < n:
            start = mid + 1
        if x > n:
            end = mid - 1
    return -1


if __name__ == '__main__':
    cases = (
        ([0, 3, 4, 5], 4, 2),
        ([-1, 43, 56, 87, 100], 87, 3),
        ([], 4, -1),
        ([2], 5, -1),
        ([6], 6, 0),
        ([0, 1, 3, 4], 0, 0),
        ([0, 1, 3, 4], 1, 1),
        ([0, 1, 3, 4], 3, 2),
        ([0, 1, 3, 4], 4, 3),
        ([-5, -2, 0], -5, 0),
        ([-5, -2, 0], -2, 1),
        ([-5, -2, 0],  0, 2),
        ([0, 1, 3, 4, 7], 7, 4),
        ([-5, -2, 0], -3, -1),
        ([1, 2, 3], 1, 0),  # start
        ([1, 2, 3], 3, 2),  # end
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10, -1),  # non-existent + non-empty
        ([], 10, -1),  # non-existent + empty
        ([3], 3, 0),  # solo
        ([-10, 2, 5, 6, 7, 19], 5, 2),  # off-centre + even
        ([-10, 2, 5, 6, 7, 19, 43], 5, 2),  # off-centre + odd
        ([-12, 0, 2, 6, 10, 14, 200], -0, 1),  # negative zero
        ([-12, 0, 2, 6, 10, 14, 200], 0, 1),  # positive zero
        ([-10, -9, -9, 3, 7, 8], -9, 2),  # duplicates + even
        ([-10, -9, -9, 9, 57], -9, 2)  # duplicates + odd
    )

    for a, v, expected in cases:
        print('a', a, 'v', v, 'expected', expected)
        idx = main(a, v)
        print('idx', idx)
        print('========')
        assert idx == expected

    print("ok")

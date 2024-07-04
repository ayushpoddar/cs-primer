import timeit
from matplotlib import pyplot
from functools import partial


def fizzbuzzSumLinear(n):
    sum = 0
    for i in range(1, n + 1):
        if i % 3 == 0 or i % 5 == 0:
            sum += i
    return sum


def fizzbuzzSumConstant(n):
    n3 = n // 3
    n5 = n // 5
    n15 = n // 15

    return apSum(3, 3, n3) + apSum(5, 5, n5) - apSum(15, 15, n15)


def apSum(a, d, n):
    internal = 2 * a + (n - 1) * d
    return (internal * n) // 2


# if __name__ == "__main__":
#     print("Enter the value of n")
#     n = int(input())

#     linear = fizzbuzzSumLinear(n)
#     constant = fizzbuzzSumConstant(n)
#     assert linear == constant
#     print(f"Linear: {linear}, Constant: {constant}")

if __name__ == '__main__':
    maxN = 20
    repeat = 10
    runs = 1000

    linTimings = []
    constTimings = []
    for n in range(1, maxN):
        linTiming = min(timeit.Timer(partial(fizzbuzzSumLinear, n)).repeat(repeat, runs))
        constTiming = min(timeit.Timer(partial(fizzbuzzSumConstant, n)).repeat(repeat, runs))
        linTimings.append(linTiming)
        constTimings.append(constTiming)

    pyplot.plot(range(1, maxN), linTimings, label='linear')
    pyplot.plot(range(1, maxN), constTimings, label='constant')
    pyplot.legend()
    pyplot.show()

import timeit
from matplotlib import pyplot
from functools import lru_cache, partial


@lru_cache(maxsize=None)
def exp_dumb_cached(base, n):
    if n == 0:
        return 1
    if n == 1:
        return base
    left = n // 2
    right = n - left
    return exp_dumb_cached(base, left) * exp_dumb_cached(base, right)


def exp_divide_and_rule(base, n):
    if n == 0:
        return 1
    res = exp_dumb_cached(base, n >> 1)
    return res * res


def exp_iter(base, n):
    stk = []
    while n > 0:
        if n & 1 == 0:
            stk.append(1)
        else:
            stk.append(base)
        n = n >> 1

    result = 1
    while len(stk):
        result = result * result * stk.pop()
    return result


def exp_iter_oz(base, n):
    res = 1
    while n > 0:
        if n & 1 == 1:  # odd
            res = res * base
            n = n - 1
        else:  # even
            base = base * base
            n = n >> 1
    return res


if __name__ == "__main__":
    maxN = 200
    repeat = 10
    runs = 1000
    base = 6

    cacheTimings = []
    noCacheTimings = []
    iterTimings = []
    iterOzTimings = []
    for n in range(1, maxN):
        assert exp_dumb_cached(base, n) == exp_iter(base, n) == exp_iter_oz(base, n)
        cacheTiming = min(timeit.Timer(partial(exp_dumb_cached, base, n)).repeat(repeat, runs))
        noCacheTiming = min(timeit.Timer(partial(exp_divide_and_rule, base, n)).repeat(repeat, runs))
        iterTiming = min(timeit.Timer(partial(exp_iter, base, n)).repeat(repeat, runs))
        iterOzTiming = min(timeit.Timer(partial(exp_iter_oz, base, n)).repeat(repeat, runs))
        cacheTimings.append(cacheTiming)
        noCacheTimings.append(noCacheTiming)
        iterTimings.append(iterTiming)
        iterOzTimings.append(iterOzTiming)

    pyplot.plot(range(1, maxN), cacheTimings, label='Dumb (Using cache)')
    pyplot.plot(range(1, maxN), noCacheTimings, label='Recursive - Simple divide and rule')
    pyplot.plot(range(1, maxN), iterTimings, label='Iterative - Divide and rule')
    pyplot.plot(range(1, maxN), iterOzTimings, label='Iterative - Divide and rule - Oz\'s solution')
    pyplot.legend()
    pyplot.show()

import time
from collections import deque
from functools import partial
import timeit
from matplotlib import pyplot


def basicRecursive(n):
    """the basic logic without any optimization"""
    if n <= 2:
        return (1, 1, 2)[n]
    return basicRecursive(n - 1) + basicRecursive(n - 2) + basicRecursive(n - 3)


def uniqueArrays(n):
    count = 0

    def helper(result=[]):
        nonlocal count
        remaining = n - sum(result)
        if remaining <= 2:
            count += (1, 1, 2)[remaining]
            return
        helper(result + [1])
        helper(result + [2])
        helper(result + [3])
    helper()
    return count


def linear(n):
    a, b, c = 1, 1, 2
    for _ in range(n):
        a, b, c = b, c, a + b + c
    return a


def linear2(n):
    if n == 1:
        return 1
    dp = [0 for _ in range(n + 1)]
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
    return dp[n]


def stackSol(n):
    stack = []
    sumStack = 0
    lastEle = count = 0
    while True:
        count += sumStack == n
        while (sumStack >= n or lastEle == 3 or sumStack + lastEle >= n) \
                and len(stack) > 0:
            lastEle = stack.pop()
            sumStack -= lastEle

        if lastEle == 3:
            break

        stack.append(lastEle + 1)
        sumStack += lastEle + 1
        lastEle = 0
    return count


def graphDFS(n):
    stack = deque()
    stack.append(0)  # start with position = 0
    count = 0
    while stack:
        x = stack.pop()  # get next state to evaluate
        if n - x <= 2:  # if current state is 0 or 1 or 2
            count += (1, 1, 2)[n - x]  # just add to count
            continue  # further evaluation not needed
        # Append the children to the stack
        stack.append(x + 1)
        stack.append(x + 2)
        stack.append(x + 3)
    return count


def graphBFS(n):
    count = 0
    queue = deque()
    queue.append(0)  # start with position = 0
    while queue:
        x = queue.popleft()  # get next state to evaluate
        if n - x <= 2:  # if current state is 0 or 1 or 2
            count += (1, 1, 2)[n - x]  # just add to count
            continue  # further evaluation not needed
        # Push the children to the queue
        queue.append(x + 1)
        queue.append(x + 2)
        queue.append(x + 3)
    return count


if __name__ == '__main__':
    maxN = 13
    functions = [basicRecursive, uniqueArrays,
                 linear, linear2, stackSol, graphDFS, graphBFS]
    functions = [basicRecursive, graphBFS, graphDFS, uniqueArrays, stackSol]
    timings = [[] for _ in range(len(functions))]
    for n in range(1, maxN):
        print(f"n = {n}")
        for i in range(len(functions)):
            func = functions[i]
            timeTaken = min(timeit.Timer(partial(func, n)).repeat(5, 1000))
            print(f"function = {func.__name__}, timeTaken = {timeTaken}")
            timings[i].append(timeTaken)

    for i in range(len(functions)):
        pyplot.plot(range(1, maxN), timings[i], label=functions[i].__name__)
    pyplot.legend()
    pyplot.show()


def measure_runtime(func, n):
    start_time = time.perf_counter()
    result = func(n)
    end_time = time.perf_counter()
    return end_time - start_time, result

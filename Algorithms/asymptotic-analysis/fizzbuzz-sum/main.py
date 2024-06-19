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


if __name__ == "__main__":
    print("Enter the value of n")
    n = int(input())

    linear = fizzbuzzSumLinear(n)
    constant = fizzbuzzSumConstant(n)
    assert linear == constant
    print(f"Linear: {linear}, Constant: {constant}")

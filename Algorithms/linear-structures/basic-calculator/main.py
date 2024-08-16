OPERATORS = ("+", "-", "*", "/")
DIGITS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")


def find(list, fn):
    for item in list:
        if fn(item):
            return item
    return None


def is_number(var):
    return isinstance(var, (int, float, complex))


def is_integer(var):
    return isinstance(var, int)


def operate(operator, x, y):
    if (operator == "+"):
        return x + y
    if (operator == "-"):
        return x - y
    if (operator == "*"):
        return x * y
    if (operator == "/"):
        return x / y


def is_operator(char):
    return char in OPERATORS


def is_opening_bracket(char):
    return char == "("


def is_closing_bracket(char):
    return char == ")"


def is_bracket(char):
    return is_opening_bracket(char) or is_closing_bracket(char)


def is_operator_gt_prev_operator(operator, prev_operator):
    return OPERATORS.index(operator) > OPERATORS.index(prev_operator)


def calculate(expr):
    stack = []
    tokens = tokenize(expr)

    def is_stack_top_operator():
        return len(stack) > 0 and is_operator(stack[-1])

    def is_stack_top_number():
        return len(stack) > 0 and is_number(stack[-1])

    def upcoming_token(curr_idx):
        return tokens[curr_idx + 1] if curr_idx + 1 < len(tokens) else None

    for i, token in enumerate(tokens):
        item = token
        if is_opening_bracket(item):
            stack.append(item)
            continue

        if is_closing_bracket(item):
            item = stack.pop()
            if is_opening_bracket(item):
                # Encontered something like this ["(", ")"]
                continue
            # Encountered something like this ["(", 2, ")"]
            stack.pop()

        if is_operator(item):
            stack.append(item)
            continue

        while is_number(item):
            if not is_stack_top_operator():
                stack.append(item)
                break

            next_token = upcoming_token(i)
            if not is_operator(next_token):
                operator = stack.pop()
                operand = stack.pop()
                item = operate(operator, operand, item)
                continue

            prev_operator = stack.pop()
            if not is_operator_gt_prev_operator(next_token, prev_operator):
                operand = stack.pop()
                item = operate(prev_operator, operand, item)
                continue

            stack.append(prev_operator)
            stack.append(item)
            break

    return 0 if not len(stack) else stack.pop()


def tokenize(expr):
    result = []
    currNumber = ""

    def isLastTokenNumber():
        return len(result) > 0 and is_integer(result[-1])

    def isLastTokenCloseBrace():
        return len(result) > 0 and is_closing_bracket(result[-1])

    def isLastTokenNumberOrCloseBrace():
        return isLastTokenNumber() or isLastTokenCloseBrace()

    for char in expr:
        if len(currNumber) > 0 and char not in DIGITS:
            result.append(int(currNumber))
            currNumber = ""

        if char == "-" and not isLastTokenNumberOrCloseBrace():
            currNumber += char
            continue
        if char == " ":
            continue
        if char in DIGITS:
            currNumber += char
            continue
        if is_operator(char):
            result.append(char)
            continue
        if is_bracket(char):
            result.append(char)
            continue

    if len(currNumber) > 0:
        result.append(int(currNumber))
    return result


if __name__ == "__main__":
    test_cases = (
        "(4*5)",
        "(4 + 5 - 2 +1)",
        "(12 + 13 - 56 + 5)",
        "(4 + 2 - 32 + 78)",
        "5 + 8 + 78",
        "(-2 + 8 + -65)",
        "(4 - -8 + 9)",
        "7 + 8 + -9 - (6 * 3 * 2) + -21 + (54 / 23) + (21 / -4 * -2)",
        "5 + 3 * 2",
        "(5 + 3) * 2",
        "10 - 5 + 3",
        "20 / 4 * 2 + 7",
        "(8 + 2 * 3) - (6 / 2)",
        "7 * (3 + 2)",
        "-5 + 10",
        "3 * (-4 + 2)",
        "15 / (3 + 2) * 4",
        "(10 - 5) * (2 + 3)",
        "8 + 3 * 2 - 4 / 2",
        "((4 + 2) * 3) - 5",
        "7 * 2 + (4 - 1) * 3",
        "20 - (8 + 3) * 2",
        "(7 - 3) * (2 + 4) / 2",
        "5 * (-3 + 7) - 2",
        "(9 + 3) / (2 + 1) * 4",
        "12 / 3 - 2 * (5 + 1)",
        "(15 - 5) / (1 + 1) + 3 * 2",
        "6 * (2 + 3 * (4 - 1)) - 5",
        # More complex cases
        "((10 + 5) * 3 - 2) / (4 + 1) * 2",
        "8 * (3 + 2) * (5 - (2 + 1)) - 10 / 2",
        "(20 - (4 + 2) * 3) + (15 / (3 + 2)) * 4",
        "7 * (2 + (3 - 1) * 4) - (10 + 5) / 3",
        "((9 - 3) * 2 + 4) / (3 + (2 - 1) * 2) - 5",
        "100 / (2 + 3) * 4 - 5 * (6 + 2 - 3)",
        "(15 - (3 + 2) * 2) * (4 + 2 * 3) / (2 + 1)",
        "5 * (3 + (2 - 1) * 4) - (8 + 2) * 3 + 15 / 3",
        "((20 + 5) / 5 * 3 - 6) * (2 + 4) - 10",
        "12 * (3 + (4 - 2) * 5) / ((6 + 3 - 1) * 2) - 7",
        # New cases with negative numbers at the beginning
        "-10 + 5 * 3",
        "-7 * (2 + 3) + 20",
        "-15 / 3 + 8 * 2",
        # "-(5 + 3) * 2 + 15",
        # More complicated nesting and confusing arrangements
        "(((3 + 2) * 4 - 6) / 2) * (7 - 3)",
        "5 * (3 - (2 + 1)) * (4 + 2) / 2 - 3",
        "10 - (4 + 2) * 3 + 8 / (2 * 2)",
        "((8 - 3) * (2 + 1) - 5) / (2 + 3 * (1 - 1))",
        "7 * (3 + (2 - 1) * 4) - (5 + 2) * (3 - 1)",
        "20 / (4 + 1) * 2 - 3 * (2 + 5) + 6",
        "((15 / (3 + 2)) * 4 - 6) * (2 + 1) - 9",
        "8 - 3 * (2 + 4) / 2 + 7 * (3 - 1)",
        "(10 + 5 * 2) / (4 - 1) - 3 * (2 + 3)",
        "6 * (2 + (3 - 1) * 2) - 4 * (5 + 1) / 2"
    )

    isAllTestsPass = True
    for expr in test_cases:
        expected = eval(expr)
        print("Testing", expr, "with expectation of", expected)
        calculated = calculate(expr)
        try:
            assert calculated == expected
        except AssertionError:
            print("calculated value", calculated, "is not equal to", expected)
            isAllTestsPass = False

    if isAllTestsPass:
        print("ok")

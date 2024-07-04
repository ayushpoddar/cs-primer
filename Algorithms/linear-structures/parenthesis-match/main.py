from types import SimpleNamespace


def test_parenthesis_matching():
    # Test case 1: empty string, expect True because there are no parentheses to match
    assert parenthesis_matching("") is True

    # Test case 2: no parentheses, expect True because there are no parentheses to match
    assert parenthesis_matching("abcdef") is True

    # Test case 3: simple valid parentheses, expect True
    assert parenthesis_matching("()") is True

    # Test case 4: valid nested parentheses, expect True
    assert parenthesis_matching("(())") is True

    # Test case 5: valid multiple sets of parentheses, expect True
    assert parenthesis_matching("()()") is True

    # Test case 6: valid complex case, expect True
    assert parenthesis_matching("(a(b)c(d)e(f)g)") is True

    # Test case 7: single opening parenthesis, expect False
    assert parenthesis_matching("(") is False

    # Test case 8: single closing parenthesis, expect False
    assert parenthesis_matching(")") is False

    # Test case 9: mismatched parentheses, expect False
    assert parenthesis_matching("(a(b)c(d)e(f)g") is False

    # Test case 10: another mismatch with different characters, expect False
    assert parenthesis_matching(")a(b)c(d)e(f)g(") is False

    # Test case 11: closing before opening, expect False
    assert parenthesis_matching(")(") is False

    # Test case 12: extra opening parenthesis, expect False
    assert parenthesis_matching("((())") is False

    # Test case 13: extra closing parenthesis, expect False
    assert parenthesis_matching("())") is False

    # Test case 14: complex string with invalid parentheses, expect False
    assert parenthesis_matching("(a(b)c))((d)e(f)g") is False

    # Test case 15: string with other types of brackets, expect True
    assert parenthesis_matching("[{()}]") is True

    # Test case 16: string with mixed types of brackets, expect False
    assert parenthesis_matching("[{(})]") is False

    # Add more cases if needed for specific scenarios or edge cases
    print("All test cases passed.")


MATCHES = {")": "(", "]": "[", "}": "{"}
OPEN = set(MATCHES.values())
CLOSE = set(MATCHES.keys())


def parenthesis_matching(s: str) -> bool:
    stack = []
    for char in s:
        if char in OPEN:
            stack.append(char)
            continue
        if char not in CLOSE:
            continue
        if len(stack) == 0:
            return False
        if stack.pop() != MATCHES[char]:
            return False
    return len(stack) == 0


def read_file_lines(filepath):
    with open(filepath, 'r') as file:
        return file.read().splitlines()


def make_char_position(char, lineNumber, columnNumber):
    result = SimpleNamespace()
    result.char = char
    result.lineNumber = lineNumber
    result.columnNumber = columnNumber
    return result


if __name__ == "__main__":
    # String tests
    test_parenthesis_matching()

    # Linting file
    lines = read_file_lines("stretch.rkt")

    stack = []
    lineNumber = 0
    for line in lines:
        lineNumber += 1
        columnNumber = 0
        for char in line:
            columnNumber += 1
            if char == ";":
                # Skip comments
                break
            if char in OPEN:
                charPosition = make_char_position(char,
                                                  lineNumber,
                                                  columnNumber)
                stack.append(charPosition)
                continue
            if char not in CLOSE:
                continue
            if len(stack) == 0:
                print(f"Extra closing parenthesis {char} on line {lineNumber} column {columnNumber}")
                exit(1)
            popped = stack.pop()
            if popped.char != MATCHES[char]:
                print(f"Mismatched closing parenthesis {char} found on line {lineNumber} column {columnNumber}")
                print(f"Expected {popped.char} on line {popped.lineNumber} column {popped.columnNumber} to close")
                exit(1)
    while len(stack) > 0:
        popped = stack.pop()
        print(f"Expected {popped.char} on line {popped.lineNumber} column {popped.columnNumber} to close")

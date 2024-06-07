mapping = {
    1: {
        "normal": "I",
        "fifth": "V",
    },
    10: {
        "normal": "X",
        "fifth": "L",
    },
    100: {
        "normal": "C",
        "fifth": "D",
    },
    1000: {
        "normal": "M",
    }
}

pairs = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


def ozSol(num):
    for n, r in pairs:
        if num >= n:
            return r + ozSol(num - n)
    return ""


def main(num):
    place = 1
    result = ""
    while (num > 0):
        digit = num % 10
        result = digitToRoman(digit, place) + result
        num = num // 10
        place = place * 10
    return result


def digitToRoman(digit, place):
    normal = "normal"
    fifth = "fifth"
    placeMapping = mapping[place]
    if (digit == 0):
        return ""
    if (digit <= 3):
        return placeMapping[normal] * digit
    if (digit == 4):
        return placeMapping[normal] + placeMapping[fifth]
    diff = digit - 5
    if (diff <= 3):
        return placeMapping[fifth] + digitToRoman(diff, place)
    if (diff == 4):
        return placeMapping[normal] + digitToRoman(1, place * 10)


testCases = (
    (39, "XXXIX"),
    (246, "CCXLVI"),
    (789, "DCCLXXXIX"),
    (2421, "MMCDXXI"),
    (160, "CLX"),
    (207, "CCVII"),
    (1009, "MIX"),
    (1066, "MLXVI"),
)

if __name__ == "__main__":
    for num, expected in testCases:
        print("test", num, expected)
        assert main(num) == expected
        assert ozSol(num) == expected

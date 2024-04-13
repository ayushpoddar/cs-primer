def decode(data):
    n = 0
    for byte in reversed(data):
        payload = byte & 0x7f
        n <<= 7
        n = n | payload
    return n


def encode(num):
    parts = []
    while num > 0:
        part = num & 0x7f
        num >>= 7
        if num > 0:
            part = part | 0x80
        parts.append(part)

    return bytes(parts)


assert encode(150) == b'\x96\x01'
assert decode(b'\x96\x01') == 150
assert encode(
    18446744073709551615) == b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'
print('both ok')
for n in range(1 << 10):
    print(f'encoding {n}')
    assert decode(encode(n)) == n

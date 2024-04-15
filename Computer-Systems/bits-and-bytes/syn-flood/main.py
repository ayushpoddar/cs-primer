import struct

print('=====')
with open('synflood.pcap', 'rb') as f:
    magicNumber, majorVersion, minorVersion, _, _, \
        snapLength, linkHeaderType = struct.unpack('<IHHIIII', f.read(24))
    # Confirms that the capture file is in little endian
    assert magicNumber == 0xa1b2c3d4
    assert majorVersion == 2
    assert minorVersion == 4
    assert linkHeaderType == 0

    packetsCount = ackCount = synCount = 0
    while True:
        packetHeader = f.read(16)
        if (len(packetHeader) == 0):
            break
        packetsCount += 1
        timestamp, microseconds, packetLen, origPacketLen = \
            struct.unpack('<IIII', packetHeader)
        assert packetLen == origPacketLen
        # assert packetLen == 44
        packetData = f.read(packetLen)

        linkLayerHeader = packetData[0:4]
        assert struct.unpack('<I', linkLayerHeader)[0] == 2  # ipv4

        packetData = packetData[4:]
        ipHeaderLength = (packetData[0] & 0x0f) << 2
        assert ipHeaderLength == 20

        packetData = packetData[ipHeaderLength:]

        sourcePort, destinationPort = struct.unpack('>HH', packetData[:4])
        assert 80 in (sourcePort, destinationPort)

        flagsByte = packetData[13]
        synFlag = (packetData[13] & 0x06) > 0
        ackFlag = (packetData[13] & 0x10) > 0

        if (ackFlag):
            assert sourcePort == 80
            ackCount += 1
        else:
            assert destinationPort == 80
            synCount += 1

    print(f'Total of {packetsCount} packets parsed')
    print(f'{ackCount} packets acknowledged for {synCount} sync packets')
    print(f'{(ackCount * 100 / synCount):.2f}% of packets acknowledged')

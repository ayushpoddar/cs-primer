from typing import List
import struct
import math
from functools import lru_cache
import sys


def appendByteObject(data: List, byteObject):
    for i in range(len(byteObject)):
        data.append(byteObject[i:i+1])


@lru_cache(maxsize=None)
def sine(degrees):
    return math.sin(math.radians(degrees))


@lru_cache(maxsize=None)
def cos(degrees):
    return math.cos(math.radians(degrees))


class Pixel():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    # Define class method
    @classmethod
    def bilinearTransformPixels(cls, p00, p01, p10, p11, tx, ty):
        def color(c00, c01, c10, c11):
            c1 = c01 * (1 - tx) + c11 * tx
            c0 = c00 * (1 - tx) + c10 * tx
            c = c0 * (1 - ty) + c1 * ty
            return max(0, min(255, int(c)))

        r = color(p00.r, p01.r, p10.r, p11.r)
        g = color(p00.g, p01.g, p10.g, p11.g)
        b = color(p00.b, p01.b, p10.b, p11.b)
        return cls(r, g, b)


class ImageRow():
    def __init__(self):
        self.pixels: List[Pixel] = []
        self.paddingBytes = 0

    def replacePixel(self, offset: int, pixel: Pixel):
        self.pixels[offset] = pixel

    def addPixelAsRgb(self, r, g, b):
        pixel = Pixel(r, g, b)
        self.addPixel(pixel)

    def addPixel(self, pixel):
        self.pixels.append(pixel)

    def addPadding(self, paddingBytes):
        self.paddingBytes = paddingBytes

    def reversedRow(self):
        row = ImageRow()
        row.pixels = self.pixels[::-1]
        return row

    def pixelAtIndex(self, index):
        return self.pixels[index]

    def length(self):
        return len(self.pixels)

    def bytesArray(self):
        bytesArray = []
        for pixel in self.pixels:
            bytesArray.append(struct.pack('<B', pixel.r))
            bytesArray.append(struct.pack('<B', pixel.g))
            bytesArray.append(struct.pack('<B', pixel.b))

        for _ in range(self.paddingBytes):
            bytesArray.append(struct.pack('<B', 0))
        return bytesArray


class ImageMetaData():
    def __init__(self, data, width=None, height=None):
        self.data = data
        self.width = width
        self.height = height

    def imageStartIndex(self):
        return self.__extractFromData(10, 4)

    def calculatedFileSize(self):
        return self.imageStartIndex() + self.calculatedImageSize()

    def fileSize(self):
        return self.__extractFromData(2, 4)

    def dibHeaderSize(self):
        return self.__extractFromData(14, 4)

    def dibZeroPadding(self):
        return self.dibHeaderSize() - 40

    def bytesPerPixel(self):
        bits = self.__extractFromData(28, 2)
        return bits // 8

    def pixelsPerRow(self):
        self.width = self.width or self.__extractFromData(18, 4)
        return self.width

    def bytesPerRow(self):
        return self.pixelsPerRow() * self.bytesPerPixel()

    def pixelsPerColumn(self):
        self.height = self.height or self.__extractFromData(22, 4)
        return self.height

    def calculatedImageSize(self):
        return self.pixelsPerColumn() * (self.bytesPerRow() + self.paddingBytesForRowEnd())

    def imageSize(self):
        return self.__extractFromData(34, 4)

    def bytesPerColumn(self):
        return self.pixelsPerColumn() * self.bytesPerPixel()

    def paddingBytesForRowEnd(self):
        remainder = self.bytesPerRow() % 4
        return 0 if remainder == 0 else (4 - remainder)

    def __extractFromData(self, index, size):
        dataBytes = self.data[index:index + size]
        return int.from_bytes(dataBytes, byteorder='little')

    def rotateBy90(self):
        return self.rotateByAngle(90)

    def rotateByAngle(self, degrees):
        y, x = self.pixelsPerColumn(), self.pixelsPerRow()

        height = x * sine(degrees) + y * cos(degrees)
        width = x * cos(degrees) + y * sine(degrees)

        result = ImageMetaData(self.data, round(width), round(height))
        return result

    def bytesArray(self):
        res = []
        appendByteObject(res, b'BM')  # BM Header
        appendByteObject(res, struct.pack(
            '<I', self.calculatedFileSize()))  # File size
        appendByteObject(res, struct.pack('<H', 0))  # Reserved
        appendByteObject(res, struct.pack('<H', 0))  # Reserved
        # Image data offset
        appendByteObject(res, struct.pack('<I', self.imageStartIndex()))
        # DIB header size
        appendByteObject(res, struct.pack('<I', self.dibHeaderSize()))
        appendByteObject(res, struct.pack('<i', self.pixelsPerRow()))  # Width
        appendByteObject(res, struct.pack(
            '<i', self.pixelsPerColumn()))  # Height
        appendByteObject(res, struct.pack(
            '<H', self.__extractFromData(26, 2)))  # Planes
        appendByteObject(res, struct.pack(
            '<H', self.bytesPerPixel() * 8))  # Bit depth
        # Compression
        appendByteObject(res, struct.pack('<I', self.__extractFromData(30, 4)))
        appendByteObject(res, struct.pack(
            '<I', self.calculatedImageSize()))  # Image size
        # Resolution (horizontal)
        appendByteObject(res, struct.pack('<i', self.__extractFromData(38, 4)))
        # Resolution (vertical)
        appendByteObject(res, struct.pack('<i', self.__extractFromData(42, 4)))
        # Number of colors in the palette
        appendByteObject(res, struct.pack('<I', self.__extractFromData(46, 4)))
        # "Important" colors
        appendByteObject(res, struct.pack('<I', self.__extractFromData(50, 4)))
        for byte in self.data[54:self.imageStartIndex()]:
            # Zero padding
            appendByteObject(res, struct.pack('<B', byte))
        return res


class ImageData():
    def __init__(self, metaData: ImageMetaData):
        self.rows: List[ImageRow] = []
        self.metaData = metaData

    def addPixelToCurrentRow(self, r, g, b):
        self.currentRow.addPixelAsRgb(r, g, b)

    def startNewRow(self):
        self.currentRow = ImageRow()
        self.rows.append(self.currentRow)

    def addPaddingToCurrentRow(self):
        self.currentRow.addPadding(self.metaData.paddingBytesForRowEnd())

    def addPixelsToCurrentRow(self, byteRow, bytesPerPixel):
        for i in range(0, len(byteRow), bytesPerPixel):
            r = byteRow[i]
            g = byteRow[i + 1]
            b = byteRow[i + 2]
            self.addPixelToCurrentRow(r, g, b)

    def __fillWithBlackPixels(self):
        for _ in range(self.metaData.pixelsPerColumn()):
            self.startNewRow()
            for _ in range(self.metaData.pixelsPerRow()):
                self.addPixelToCurrentRow(220, 220, 220)
            self.addPaddingToCurrentRow()

    def __replacePixel(self, x: int, y: int, pixel: Pixel):
        row = self.rows[y]
        row.replacePixel(x, pixel)

    def getPixel(self, x: int, y: int):
        row = self.rows[y]
        return row.pixelAtIndex(x)

    def rotateBy90(self):
        return self.rotateByAngle(90)

    def rotateByAngle(self, deg):
        if (deg > 90):
            return self.rotateByAngle(90).rotateByAngle(deg - 90)

        rotatedImageMetaData = self.metaData.rotateByAngle(deg)
        rotatedImageData = ImageData(rotatedImageMetaData)
        rotatedImageData.__fillWithBlackPixels()

        w = self.metaData.pixelsPerRow()
        h = self.metaData.pixelsPerColumn()
        for y, row in enumerate(rotatedImageData.rows):
            for x in range(row.length()):
                a = x * cos(deg) - y * sine(deg) + w * sine(deg) * sine(deg)
                b = x * sine(deg) - w * sine(deg) * cos(deg) + y * cos(deg)

                if (a < 0 or a >= w - 1 or b < 0 or b >= h - 1):
                    continue

                try:
                    a1 = math.ceil(a)
                    b1 = math.ceil(b)
                    a0 = math.floor(a)
                    b0 = math.floor(b)

                    tx = a - a0
                    ty = b - b0

                    p00 = self.getPixel(a0, b0)
                    p01 = self.getPixel(a0, b1)
                    p10 = self.getPixel(a1, b0)
                    p11 = self.getPixel(a1, b1)

                    pixel = Pixel.bilinearTransformPixels(
                        p00, p01, p10, p11, tx, ty)
                    rotatedImageData.__replacePixel(x, y, pixel)
                except IndexError:
                    print("a:", a, "b:", b, "w:", w, "h:", h, "x:", x, "y:", y)
                    print("a0:", a0, "a1:", a1, "b0:", b0, "b1:", b1)
                    raise

        return rotatedImageData

    def bytesArray(self):
        bytesArray: List = self.metaData.bytesArray()
        for row in self.rows:
            rowBytesArray = row.bytesArray()
            bytesArray.extend(rowBytesArray)
        return bytesArray


def main():
    with open('stretch-goal.bmp', 'rb') as f:
        data = f.read()

    data = list(data)
    metaData = ImageMetaData(data)
    imageData = ImageData(metaData)

    i = metaData.imageStartIndex()
    while (i < len(data)):
        imageData.startNewRow()
        row = data[i:i + metaData.bytesPerRow()]
        imageData.addPixelsToCurrentRow(row, metaData.bytesPerPixel())

        imageData.addPaddingToCurrentRow()
        i += metaData.bytesPerRow() + metaData.paddingBytesForRowEnd()

    degrees = int(sys.argv[1])
    rotatedImageBytes = imageData.rotateByAngle(degrees).bytesArray()
    with open('output.bmp', 'wb') as f:
        for i, b in enumerate(rotatedImageBytes):
            f.write(b)


if __name__ == '__main__':
    result = main()

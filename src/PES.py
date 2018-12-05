from struct import pack
from svgpathtools import *
import math
import random

def encodeU8(num):
    return pack("<B", int(num))

def encodeU16(num):
    return pack("<H", int(num))

def encodeS16(num):
    return pack("<h", int(num))

def encodeU32(num):
    return pack("<I", int(num))

def encodeFloat(num):
    return pack("<f", num)

'''
The EmbroideryDesign class is used to build
the stitches that will be exported. To actually
export them, the object is converted to a PES
object.
'''
class EmbroideryDesign:

    def __init__(self):
        None

'''
The PES object and all the objects that follow it 
are for easy encoding to the PES format.
'''
class PES:
    colors = [('None', 0,0,0),
              ('Prussian Blue', 26, 10, 148),
              ('Blue', 15, 117, 255),
              ('Teal Green', 0, 147, 76),
              ('Corn Flower Blue', 186, 189, 254),
              ('Red', 236, 0, 0),
              ('Reddish Brown', 228, 153, 90),
              ('Magenta', 204, 72, 171),
              ('Light Lilac', 253, 196, 250),
              ('Lilac', 221, 132, 205),
              ('Mint Green', 107, 211, 138),
              ('Deep Gold', 228, 169, 69),
              ('Orange', 255, 189, 66),
              ('Yellow', 255, 230, 0),
              ('Lime Green', 108, 217, 0),
              ('Brass', 193, 169, 65),
              ('Silver', 181, 173, 151),
              ('Russet Brown', 186, 156, 95),
              ('Cream Brown', 250, 245, 158),
              ('Pewter', 128, 128, 128),
              ('Black', 0, 0, 0),
              ('Ultramarine', 0, 28, 223),
              ('Royal Purple', 223, 0, 184),
              ('Dark Gray', 98, 98, 98),
              ('Dark Brown', 105, 38, 13),
              ('Deep Rose', 255, 0, 96),
              ('Light Brown', 191, 130, 0),
              ('Salmon Pink', 243, 145, 120),
              ('Vermilion', 255, 104, 5),
              ('White', 240, 240, 240),
              ('Violet', 200, 50, 205),
              ('Seacrest', 176, 191, 155),
              ('Sky Blue', 101, 191, 235),
              ('Pumpkin', 255, 186, 4),
              ('Cream Yellow', 255, 240, 108),
              ('Khaki', 254, 202, 21),
              ('Clay Brown', 243, 129, 1),
              ('Leaf Green', 55, 169, 35),
              ('Peacock Blue', 35, 70, 95),
              ('Gray', 166, 166, 149),
              ('Warm Gray', 206, 191, 166),
              ('Dark Olive', 150, 170, 2),
              ('Linen', 255, 227, 198),
              ('Pink', 255, 153, 215),
              ('Deep Green', 0, 112, 4),
              ('Lavender', 237, 204, 251),
              ('Wisteria Violet', 192, 137, 216),
              ('Beige', 231, 217, 180),
              ('Carmine', 233, 14, 134),
              ('Amber Red', 207, 104, 41),
              ('Olive Green', 64, 134, 21),
              ('Dark Fuchsia', 219, 23, 151),
              ('Tangerine', 255, 167, 4),
              ('Light Blue', 185, 255, 255),
              ('Emerald Green', 34, 137, 39),
              ('Purple', 182, 18, 205),
              ('Moss Green', 0, 170, 0),
              ('Flesh Pink', 254, 169, 220),
              ('Harvest Gold', 254, 213, 16),
              ('Electric Blue', 0, 151, 223),
              ('Lemon Yellow', 255, 255, 132),
              ('Fresh Green', 207, 231, 116),
              ('Applique Material', 255, 200, 100),
              ('Applique Position', 255, 200, 200),
              ('Applique', 255, 200, 200)]

    @classmethod
    def getClosestColor(cls, color):
        # Black by default
        closest = 19
        lastDist = 9999.0
        for i, cur in enumerate(cls.colors):
            red =  math.pow( cur[1] - color[0], 2)
            green = math.pow(cur[2] - color[1], 2)
            blue = math.pow(cur[3] - color[2], 2)
            dist = math.sqrt( red + green + blue )
            if dist < lastDist:
                lastDist = dist
                closest = i

        return (closest,
        cls.colors[closest][0],
        cls.colors[closest][1],
        cls.colors[closest][2],
        cls.colors[closest][3])

    def __init__(self, PEC, shape):
        self.magic = "#PES"
        self.version = "0001"
        self.sections = []
        self.PEC = PEC
        self.shape = shape

    def encode(self):
        b = bytearray()
        b.extend(self.magic)
        b.extend(self.version)
        # Save a spot for the PEC offset that we will
        # change later to the actual offset
        pecOffsetLocation = len(b)
        b.extend([0x0C, 0x00, 0x00, 0x00])

        b.extend(encodeU16(1))
        b.extend(encodeU16(1))
        # Number of sew segment blocks
        b.extend(encodeU16(0))
        #b.extend([0x00, 0x00, 0x00, 0x00])

        # CEmbOne section
        # b.extend(encodeU16(7))
        # b.extend("CEmbOne")
        #
        # # Standard block geometry
        # left, right, bottom, top = self.shape.bbox()
        # b.extend(encodeS16(left))
        # b.extend(encodeS16(top))
        # b.extend(encodeS16(right))
        # b.extend(encodeS16(bottom))
        # b.extend(encodeS16(left))
        # b.extend(encodeS16(top))
        # b.extend(encodeS16(right))
        # b.extend(encodeS16(bottom))
        #
        # b.extend(encodeFloat(1.0))
        # b.extend(encodeFloat(0.0))
        # b.extend(encodeFloat(0.0))
        # b.extend(encodeFloat(1.0))
        # b.extend(encodeFloat(0.0))
        # b.extend(encodeFloat(0.0))
        #
        # # Nobody knows what this value is but it's usually 1
        # b.extend(encodeU16(1))
        #
        # # Coordinate translation?
        # b.extend(encodeS16(0))
        # b.extend(encodeS16(0))
        #
        # # Width/height
        # b.extend(encodeS16(self.PEC.size.real))
        # b.extend(encodeS16(self.PEC.size.imag))
        #
        # # Eight zeros for whatever reason
        # b.extend([0,0,0,0,0,0,0,0])
        # # CSewSeg block count (1)
        # b.extend(encodeU16(1))
        #
        # # Means that more blocks follow.
        # b.extend([0xFF, 0xFF, 0x00, 0x00])
        #
        #
        # # CSewSeg
        # b.extend(encodeU16(7))
        # b.extend("CSewSeg")
        # # Encode stitch list
        # b.extend(encodeU16(0))
        # b.extend(encodeU16(1))
        # testStitchCount = 100
        # b.extend(encodeU16(testStitchCount))
        # for x in range(0, testStitchCount):
        #     Stitch(toPoint=complex(random.uniform(-100, 100), random.uniform(-100, 100))).encodeForCSewSeg(b)
        #
        # # Encode color list
        # b.extend(encodeU16(1))
        # b.extend(encodeU16(0))
        # b.extend(encodeU16(10))
        #
        # # No more blocks follow
        # b.extend([0x00, 0x00, 0x00, 0x00])


        pecOffset = len(b)
        self.PEC.encode(b)

        b[pecOffsetLocation:pecOffsetLocation+4] = encodeU32(pecOffset)

        # Old code for the PES section
        #  that I decided to try excluding.
        # # Assume 100mm x 100mm hoop size
        # b.extend(encodeU16(0))
        # # Use existing design area (don't know what this does.)
        # b.extend(encodeU16(0))
        # # Segment block count
        # b.extend(encodeU16( len(self.sections) ))
        #
        # if len(self.sections) is 0:
        #     # No sections follow
        #     b.extend("0000")
        #     b.extend("0000")
        # else:
        #     # Write sections
        #     for section in self.sections:
        #         section.encode(b)

        return b

class PEC:
    def __init__(self, label, colors, commands, size):
        self.label = label
        self.colors = colors
        self.size = size

        # Commands include stitches, jumps, and color changes
        self.commands = commands
        # First stitch must be a jump stitch.
        self.commands[0].type = Stitch.TYPE_JUMP

        self.thumbnailWidth = 6
        self.thumbnailHeight = 38


    def encode(self, b):
        # The label is always 19 bytes
        # "LA:" + name + spaces to make it 19 bytes total + carriage return
        pecStart = len(b)
        b.extend("LA:" + self.label[:16].ljust(16))
        b.extend("\r")
        # Lots of values that aren't understood but probably have to be there.
        b.extend([0x20] * 11)

        b.extend([0xFF])

        b.extend([0x00])
        b.extend([0xFF])

        # Thumbnail width and height
        b.extend([self.thumbnailWidth])
        b.extend([self.thumbnailHeight])

        b.extend([0x20, 0x20, 0x20, 0x20, 0x64, 0x20, 0x00, 0x20, 0x00, 0x20, 0x20, 0x20])

        # Number of colors - 1
        b.extend([ (len(self.colors) - 1) & 0xFF])

        # Write colors indices
        for c in self.colors:
            b.extend([c[0] & 0xFF])

        # Palette section padding?
        b.extend([0x20] *  (462 - (len(self.colors) - 1) ))

        # Second section of PEC header

        b.extend([0x00, 0x00])

        # Offset to image thumbnail relative to the beginning of the second section
        # Set to zero for now because we don't know how many stitches we have yet.
        thumbnailMarker = len(b)
        b.extend([0x00, 0x00])

        b.extend([0x00, 0x31])
        b.extend([0xFF, 0xF0])

        # Width and height
        print("PEC has Width: {} Height: {}".format(self.size.real, self.size.imag))
        # b.extend(encodeS16(self.size.real))
        # b.extend(encodeS16(self.size.imag))
        b.extend(encodeS16(1000))
        b.extend(encodeS16(1000))

        b.extend([0xE0, 0x01])
        b.extend([0xB0, 0x01])

        b.extend([0x00] * 4)

        for command in self.commands:
            command.encode(b)

        # End of stitch list
        b.extend([0xFF, 0, 0, 0, 0])

        # Write the thumbnails
        thumbStart = len(b)
        for i in range(0, 2):
            for x in range(0, len(self.colors)):
                for r in range(0, self.thumbnailHeight):
                    for p in range(0, self.thumbnailWidth):
                        b.extend([0xFF & int(random.uniform(0, 255))])

        b[thumbnailMarker:thumbnailMarker+2] = encodeU16(thumbStart - 512 - pecStart)




class CEmbOne:
    def __init__(self):
        None

    def encode(self, b):
        b.extend(encodeU16(7))
        b.extend("CEmbOne")
        b.extend()


class BlockGeometry:
    def __init__(self):
        None
    def encode(self, b):
        None


class CSewSeg:
    def __init__(self):
        None

class Stitch:
    TYPE_REGULAR = 0xFFFF
    TYPE_SHORT = 0x00
    TYPE_LONG = 0x8000
    TYPE_JUMP = 0x9000
    TYPE_TRIM = 0xA000

    lastPoint = (0+0j)

    # Initialize a new stitch from the previous location
    #  to the new location.
    def __init__(self, toPoint):
        assert(isinstance(toPoint, complex))
        self.point = toPoint
        self.type = Stitch.TYPE_REGULAR


    def encode(self, b):
        # Decide whether to make long or not.
        if self.type == Stitch.TYPE_REGULAR:
            if Line(Stitch.lastPoint, self.point).length() > 63:
                self.type = Stitch.TYPE_LONG
            else:
                self.type = Stitch.TYPE_SHORT

        self.encodePoint(self.point - Stitch.lastPoint, b)
        Stitch.lastPoint = complex( int(round(self.point.real)), int(round(self.point.imag)))

    def encodePoint(self, point, b):
        self.encodeCoordinate(point.real, b)
        self.encodeCoordinate(point.imag, b)

    def encodeCoordinate(self, coordinate, b):
        if coordinate > 2047 or coordinate < -2047:
            raise Exception("Coordinate movement too big: {}".format(coordinate))

        if self.type == Stitch.TYPE_SHORT:
            b.extend([ (int(round(coordinate)) & 0x7F) ])
        else:
            total = self.type + ( int(round(coordinate)) & 0xFFF )
            b.extend([ ((total & 0xFF00) >> 8), total & 0xFF])

    def encodeForCSewSeg(self, b):
        b.extend(encodeS16(self.point.real))
        b.extend(encodeS16(self.point.imag))

    def length(self):
        return self.line.length()

    # Flips the start and end points of a stitch
    def reverse(self):
        self.line = Line(start=self.line.end, end=self.line.start)

class ColorChange:
    TYPE_COLOR_CHANGE_left = 0xFE
    TYPE_COLOR_CHANGE_right = 0xB0

    def __init__(self, colorIndex, indexInColorList):
        self.colorIndex = colorIndex
        self.indexInColorList = indexInColorList

    def encode(self, b):
        b.extend([ ColorChange.TYPE_COLOR_CHANGE_left ])
        b.extend([ ColorChange.TYPE_COLOR_CHANGE_right ])
        b.extend([ self.indexInColorList & 0xFF ])
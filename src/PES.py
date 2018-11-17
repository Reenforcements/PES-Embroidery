from struct import pack

def encodeU8(num):
    return pack("<B", num)

def encodeU16(num):
    return pack("<H", num)

def encodeU32(num):
    return pack("<I", num)

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

    def __init__(self):
        self.magic = "#PES"
        self.version = "0001"
        self.sections = []

    def encode(self):
        b = bytearray()
        b.extend(self.magic)
        b.extend(self.version)
        # Save a spot for the PEC offset that we will
        # change later to the actual offset
        b.extend("0000")

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
    def __init__(self):
        self.label = "default"
        self.numberOfColors = 1
        self.stitches = []


    def encode(self, b):
        # The label is always 19 bytes
        # "LA:" + name + spaces to make it 19 bytes total + carriage return
        b.extend("LA:" + self.label[:16].ljust(16))
        b.extend("\r")
        # Lots of values that aren't understood but probably have to be there.
        b.extend([0x20] * 11)

        b.extend(0xFF)

        b.extend(0x00)
        b.extend(0xFF)

        # Thumbnail width and height
        b.extend(6)
        b.extend(38)

        b.extend([0x20, 0x20, 0x20, 0x20, 0x64, 0x20, 0x00, 0x20, 0x00, 0x20, 0x20, 0x20])

        # Number of colors - 1
        b.extend((self.numberOfColors - 1) & 0xFF)
        #TEMP, assign color palette indices
        for i in self.numberOfColors:
            b.extend(i & 0xFF)
        # Palette section padding?
        b.extend([0x20] *  (462 - self.numberOfColors))

        # Second section of PEC header

        b.extend([0x00, 0x00])

        # Offset to image thumbnail relative to the beginning of the second section
        # Set to zero for now because we don't know how many stitches we have yet.
        b.extend([0x00, 0x00])

        b.extend([0x31, 0x00])
        b.extend([0xF0, 0xFF])

        # Width and height
        # TEMP values
        b.extend([0x0A, 0x0A])
        b.extend([0x0A, 0x0A])

        b.extend([0x01, 0xE0])
        b.extend([0x01, 0xB0])

        b.extend([0x00] * 4)

        for stitch in self.stitches:
            stitch.encode(b)

        # End of stitch list
        b.extend(0xFF)





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
    TYPE_JUMP = 0
    TYPE_
    def __init__(self, start, end):
        if type(start) != complex:
            raise Exception("Stitch - start point not a point object.")

        if type(end) != complex:
            raise Exception("Stitch - end point not a point object.")

        self.start = start
        self.end = end

    def encode(self, b):
        None
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
    def __init__(self, start, end):
        if type(start) != complex:
            raise Exception("Stitch - start point not a point object.")

        if type(end) != complex:
            raise Exception("Stitch - end point not a point object.")

        self.start = start
        self.end = end
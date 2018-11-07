import struct

class PES:

    def __init__(self):
        self.version = "#PES0001"
        # PEC seek value (4 byte little endian integer)

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
import argparse
import struct

parser = argparse.ArgumentParser(description="Converts an SVG file into a PES embroidery file.")

parser.add_argument("-i", dest="inputFile", type=str, action='store', required=True)

args = parser.parse_args()

def read(file, amount, format):
    bytes = file.read(amount)
    if len(bytes) is not amount:
        return None

    return (struct.unpack(format, bytes), bytes)

def printW(string, raw):
    raw = bytearray(raw)
    print("{}  {}".format(string, " ".join(format(x, "02x") for x in raw) ))

def assertContinue(f):
    h1 = f.read(2)
    h2 = f.read(2)
    h1 = struct.unpack("<H", h1)[0]
    h2 = struct.unpack("<H", h2)[0]
    if h1 != 0xFFFF or h2 != 0:
        raise Exception("Didn't get continue bytes.")
    else:
        print("Got continue block: {} {}".format(h1, h2))

with open(args.inputFile, "r") as f:

    b = f.read(8)
    print("PES Header: {}".format(b))

    b = f.read(4)
    print("PEC offset: {}".format( struct.unpack("<I", b)[0] ))

    b = f.read(2)
    print("Hoop size: {}".format(struct.unpack("<H", b)[0]))

    b = f.read(2)
    print("Use existing design area: {}".format(struct.unpack("<H", b)[0]))

    b = f.read(2)
    print("CSewSeg block count: {}".format(struct.unpack("<H", b)[0]))
    print("")

    assertContinue(f)

    b = f.read(2)
    l = struct.unpack("<H", b)[0]
    print("Header string length: {}".format( l ))
    print("Header string: {}".format( f.read(l) ))

    for y in range(0,2):
        b = f.read(2)
        print("Top: {}".format(struct.unpack("<H", b)[0]))
        b = f.read(2)
        print("Left: {}".format(struct.unpack("<H", b)[0]))
        b = f.read(2)
        print("Right: {}".format(struct.unpack("<H", b)[0]))
        b = f.read(2)
        print("Bottom: {}".format(struct.unpack("<H", b)[0]))

    for y in range(0, 6):
        b = f.read(4)
        print("Matrix: {}".format(struct.unpack("<f", b)[0]))

    b = f.read(2)
    print("Typically 1: {}".format(struct.unpack("<H", b)[0]))

    b = f.read(2)
    print("CSewSeg X?: {}".format(struct.unpack("<h", b)[0]))
    b = f.read(2)
    print("CSewSeg Y?: {}".format(struct.unpack("<h", b)[0]))

    b = f.read(2)
    print("CSewSeg width: {}".format(struct.unpack("<h", b)[0]))
    b = f.read(2)
    print("CSewSeg height: {}".format(struct.unpack("<h", b)[0]))

    b = f.read(8)
    print("Eight zeros: {}".format(b))

    b = f.read(2)
    print("CSewSeg block count: {}".format(struct.unpack("<H", b)[0]))
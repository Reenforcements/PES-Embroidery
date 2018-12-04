import sys
import pyglet
import struct
import random
import math
import time
from ctypes import c_byte, c_short

# Make a new window to render into
window = pyglet.window.Window()
window.set_size(1000,1000)
window.set_location(300, 0)
pyglet.gl.glClearColor(0.4,0.4,0.4,1)

#filepath = "/Users/imaustyn/Documents/MiamiUniversity/ECE 487/Project/Understanding2/tux.pes"
#filepath = "/Users/imaustyn/Downloads/Circle embroidery designs/Circle.pes"
filepath = "/Users/imaustyn/Documents/MiamiUniversity/ECE 487/Project/PES-Embroidery/TestOutput/simple.PES"
#filepath = "/Users/imaustyn/Documents/MiamiUniversity/ECE 487/Project/PES-Embroidery/TestOutput/simpleTry.PES"

# Global variables
class Global:
    colorLookup = [
              ('None', 26, 10, 148),
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

    pauseEmbroidery = False
    batch = pyglet.graphics.Batch()
    x = 0
    y = 0
    file = None
    xScale = 2.0
    yScale = 2.0
    xOffset = 500.0
    yOffset = 500.0
    testColors = [(244, 238, 66), (255,255,255), (0,0,0)]
    colorIndex = 0

    @classmethod
    def addLine(cls, x1, y1, x2, y2, r, g, b):

        cls.batch.add(2, pyglet.gl.GL_LINES, None,
                         ('v2f', ((x1 / cls.xScale) + cls.xOffset,
                                  (y1 / cls.yScale) + cls.yOffset,
                                  (x2 / cls.xScale) + cls.xOffset,
                                  (y2 / cls.yScale) + cls.yOffset )),
                         ('c3B', (r,g,b, r,g,b))
                         )
        print("addLine from ({}, {}) to ({}, {})".format(x1, y1, x2, y2) )
        cls.x = int(x2)
        cls.y = int(y2)

    @classmethod
    def readPECHeader(cls):
        if cls.file is None:
            return

        f = cls.file # type: file
        print(f.read(8))
        PECOffset = struct.unpack("<I", f.read(4))[0]
        print("Seeking to byte: {}".format(PECOffset))
        f.seek(PECOffset)
        # Skip stuff
        cls.label = f.read(20)
        print("Label: {}".format(cls.label))
        f.read(14)

        # Read thumbnail width and height
        thumbWidth = struct.unpack("B", f.read(1))[0]
        thumbHeight = struct.unpack("B", f.read(1))[0]
        print("Thumbnail dimensions: {} by {}".format(8 * thumbWidth, thumbHeight))

        f.read(12)
        cls.numberOfColors = struct.unpack("B", f.read(1))[0] + 1
        print("Number of colors: {}".format(cls.numberOfColors))

        cls.colors = []
        for c in range(0, cls.numberOfColors):
            color = struct.unpack("B", f.read(1))[0]
            cls.colors.append(color)
            print("    Color {}: {}".format(c, color))


        f.read(462 - (cls.numberOfColors-1))
        # blank = struct.unpack("BB", f.read(2))
        # if blank is not (0,0):
        #     print("nope: {}".format(blank) )
        #     sys.exit(0)
        f.read(2)

        # Thumbnail offset
        thumbOffset = struct.unpack("<H", f.read(2))[0] + 512 + PECOffset
        print("Thumbnail starts at byte {}".format(thumbOffset))

        # Print thumbnail
        lastPosition = f.tell()
        f.seek(thumbOffset)
        for c in range(0, cls.numberOfColors):
            for row in range(0, thumbHeight):
                for b in range(0, thumbWidth):
                    pixels = struct.unpack("B", f.read(1))[0]
                    for x in range(0, 8):
                        if ((0x80 >> (7-x)) & pixels) > 0:
                            c = "1"
                        else:
                            c = "0"
                        sys.stdout.write(c)
                sys.stdout.write("\n")

        f.seek(lastPosition)

        f.read(4)
        width, height = struct.unpack("<hh", f.read(4))
        f.read(8)
        print("Width and height of design: {}, {}".format(width, height))
        print("Starting stitches at location: {}".format(f.tell()))

        Global.addLine(Global.x, Global.y, width, 0,
                       (Global.testColors[Global.colorIndex])[0],
                       (Global.testColors[Global.colorIndex])[1],
                       (Global.testColors[Global.colorIndex])[2])
        Global.addLine(Global.x, Global.y, Global.x + 0, Global.y + height,
                       (Global.testColors[Global.colorIndex])[0],
                       (Global.testColors[Global.colorIndex])[1],
                       (Global.testColors[Global.colorIndex])[2])
        Global.addLine(Global.x, Global.y, Global.x + -width, Global.y + 0,
                       (Global.testColors[Global.colorIndex])[0],
                       (Global.testColors[Global.colorIndex])[1],
                       (Global.testColors[Global.colorIndex])[2])
        Global.addLine(Global.x, Global.y, Global.x + 0, Global.y + -height,
                       (Global.testColors[Global.colorIndex])[0],
                       (Global.testColors[Global.colorIndex])[1],
                       (Global.testColors[Global.colorIndex])[2])

        # Get the starting point
        #while True:
        Global.x = Global.getCoordinate(f)
        Global.y = -Global.getCoordinate(f)

            #if Global.x != 0 or Global.y != 0:
            #    break
        print("Starting at coordinates: ({}, {})".format(Global.x, Global.y))




    # I'm pretty sure one coordinate can be the long form
    #  and the second one is short or vice versa. I initially
    #  thought they had to come in pairs but that didn't seem
    #  to be working so let's try it this way.
    @classmethod
    def getCoordinate(cls, f):
        peek = f.read(1)
        f.seek(f.tell() - 1)
        if len(peek) is 0 or peek is None:
            return "End"

        peekByte = struct.unpack("B", peek)[0]

        if (0xFF & peekByte) == 0xFF:
            print("End stitches")
            return "End"

        print("Peek byte: {:02x}".format(peekByte))
        if (peekByte & 0x80) > 0:
            print("Long")
            # Double length
            c = struct.unpack(">H", Global.readBytes(f, 2))[0]
            #print("Beep: {}".format(hex(c)))

            # Color change
            if c == 0xFEB0:
                Global.colorIndex = struct.unpack("b", Global.readBytes(f, 1))[0]
                print("Color change to {}".format(Global.colorIndex))
                return None

            # Verify
            if (c & 0x8000) == 0:
                print("Double length stitch didn't have leading 1.")
                sys.exit(0)

            c = c_short((c & 0x07FF) + (0xF800 if ((c & 0x0800) > 0) else 0)).value
            return c
        else:
            print("Short")
            # Single length coordinate
            c = struct.unpack("B", Global.readBytes(f, 1))[0]

            if (c & 0x80) != 0:
                print("Single length stitch didn't have leading 0.")
                sys.exit(0)
            print(c)
            # c = c_byte( (c & 0x3F) | (0xc0 if ((c & 0x40) > 0) else 0) ).value
            c = c_byte(((c & 0b01000000) << 1) | c).value
            return c

    @classmethod
    def readBytes(cls, f, num):
        bytes = f.read(num)
        s = ""
        for b in bytes:
            s = s + hex(ord(b))
        print("Read: {}".format(s))
        return bytes

    @classmethod
    def stepRendering(cls, stepBy):

        f = cls.file


        for i in range(0,stepBy):
            x = cls.getCoordinate(f)
            if x is None or isinstance(x, str):
                continue
            y = -cls.getCoordinate(f)
            if y is None or isinstance(y, str):
                continue

            if x is "End" or y is "End":
                break

            print("({},{})".format(x,y))
            cls.addLine(Global.x, Global.y, Global.x + x, Global.y + y,
                        (Global.colorLookup[Global.colors[Global.colorIndex]])[1],
                         (Global.colorLookup[Global.colors[Global.colorIndex]])[2],
                          (Global.colorLookup[Global.colors[Global.colorIndex]])[3])








@window.event
def on_key_press(symbol, modifiers):
    global pauseEmbroidery
    if symbol is pyglet.window.key.P:
        pauseEmbroidery = ~(pauseEmbroidery)

    if symbol is pyglet.window.key.S:
        if modifiers & pyglet.window.key.MOD_SHIFT:
            Global.stepRendering(300)
        else:
            Global.stepRendering(1)

@window.event
def on_key_release(symbol, modifiers):
    None


def updateDisplay(s):
    window.clear()
    pyglet.gl.glLineWidth(1)

    # Stitch a line


    # Draw everything we have so far
    Global.batch.draw()


# Open the PES file and start "stitching"
Global.file = open(filepath, "r")
print("Opened file: {}, {}".format(filepath, Global.file))

# Read the header
Global.readPECHeader()

# Run loop for rendering
pyglet.clock.schedule_interval(updateDisplay, 1/30.0)
pyglet.app.run()













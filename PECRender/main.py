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

filepath = "/Users/imaustyn/Documents/MiamiUniversity/ECE 487/Project/Understanding2/tux.pes"
#filepath = "/Users/imaustyn/Downloads/Circle embroidery designs/Circle.pes"

# Global variables
class Global:
    pauseEmbroidery = False
    batch = pyglet.graphics.Batch()
    x = 0
    y = 0
    file = None
    xScale = 4.0
    yScale = 4.0
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
        f.seek(PECOffset)
        # Skip stuff
        cls.label = f.read(20)
        print("Label: {}".format(cls.label))
        f.read(28)
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
        f.read(8)
        width, height = struct.unpack("<HH", f.read(4))
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
        while True:
            Global.x = Global.getCoordinate(f)
            Global.y = -Global.getCoordinate(f)

            if Global.x != 0 or Global.y != 0:
                break
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

        if peek == 0xFF:
            print("End stitches")
            return "End"

        peekByte = struct.unpack("B", peek)[0]
        if (peekByte & 0x80) > 0:
            # Double length
            c = struct.unpack(">H", Global.readBytes(f, 2))[0]
            print("Beep: {}".format(hex(c)))

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
            if x is None:
                continue
            y = -cls.getCoordinate(f)
            if y is None:
                continue

            if x is "End" or y is "End":
                break

            print("({},{})".format(x,y))
            cls.addLine(Global.x, Global.y, Global.x + x, Global.y + y,
                        (Global.testColors[Global.colorIndex])[0],
                         (Global.testColors[Global.colorIndex])[1],
                          (Global.testColors[Global.colorIndex])[2])








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













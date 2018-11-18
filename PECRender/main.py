import sys
import pyglet
import struct
import random

# Make a new window to render into
window = pyglet.window.Window()
window.set_size(1000,1000)
window.set_location(300, 0)
pyglet.gl.glClearColor(0.4,0.4,0.4,1)

filepath = "/Users/imaustyn/Documents/MiamiUniversity/ECE 487/Project/Understanding2/tux.pes"

# Global variables
class Global:
    pauseEmbroidery = False
    batch = pyglet.graphics.Batch()
    x = 0
    y = 0
    file = None
    scale = 1.0

    @classmethod
    def addLine(cls, x1, y1, x2, y2, r, g, b):
        cls.batch.add(2, pyglet.gl.GL_LINES, None,
                         ('v2f', (x1 / cls.scale, y1 / cls.scale, x2 / cls.scale, y2 / cls.scale)),
                         ('c3B', (r,g,b, r,g,b))
                         )
        print("Stitch from ({}, {}) to ({}, {})".format(x1, y1, x2, y2) )
        cls.x = x2
        cls.y = y2

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


        f.read(462 - cls.numberOfColors)
        # blank = struct.unpack("BB", f.read(2))
        # if blank is not (0,0):
        #     print("nope: {}".format(blank) )
        #     sys.exit(0)
        f.read(20)
        print("Starting stitches at location: {}".format(f.tell()))

        # I'm pretty sure one coordinate can be the long form
        #  and the second one is short or vice versa. I initially
        #  thought they had to come in pairs but that didn't seem
        #  to be working so let's try it this way.
        def getCoordinate():
            peek = f.read(1)
            f.seek(f.tell() - 1)
            if peek is None:
                return "End"

            if peek == 0xFF:
                print("End stitches")
                return "End"

            peekByte = struct.unpack("B", peek)[0]
            if (peekByte & 0x80) > 0:
                # Double length
                c = struct.unpack(">H", f.read(2))[0]
                # Verify
                if (c & 0x8000) == 0:
                    print("Double length stitch didn't have leading 1.")
                    sys.exit(0)
                c = (c & 0x07FF) * (-1 if (c & 0x0800) > 0 else 1)
                return c
            else:
                # Single length coordinate
                c = struct.unpack("B", f.read(1))[0]
                if (c & 0x80) != 0:
                    print("Single length stitch didn't have leading 0.")
                    sys.exit(0)
                c = (c & 0x3F) * (-1 if (c & 0x70) > 0 else 1)
                return c



        while True:
            x = getCoordinate()
            y = getCoordinate()

            if x is "End" or y is "End":
                break

            cls.addLine(Global.x, Global.y, Global.x + x, Global.y + y, int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255)))










@window.event
def on_key_press(symbol, modifiers):
    global pauseEmbroidery
    if symbol is pyglet.window.key.P:
        pauseEmbroidery = ~(pauseEmbroidery)

@window.event
def on_key_release(symbol, modifiers):
    None


def updateDisplay(s):
    window.clear()
    pyglet.gl.glLineWidth(8)

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















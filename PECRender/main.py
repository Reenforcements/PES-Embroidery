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
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    file = None

    @classmethod
    def addLine(cls, x1, y1, x2, y2, r, g, b):
        cls.batch.add(2, pyglet.gl.GL_LINES, None,
                         ('v2i', (x1, y1, x2, y2)),
                         ('c3B', (r,g,b, r,g,b))
                         )

    @classmethod
    def readPECHeader(cls):
        if cls.file is None:
            return

        




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















import pyglet
from svgpathtools import Line, CubicBezier, QuadraticBezier, Path

class GenericRenderer:
    globalRenderer = None

    def __init__(self):
        # Make a new window to render into
        self.window = pyglet.window.Window()
        self.window.set_size(1000, 1000)
        self.window.set_location(300, 0)
        pyglet.gl.glClearColor(0.4, 0.4, 0.4, 1)

        self.lineBatch = pyglet.graphics.Batch()
        self.pointBatch = pyglet.graphics.Batch()

        pyglet.gl.glLineWidth(2)

        self.addLine(Line(start=(0+0j), end=(1000+1000j)), 255, 0, 0)

        GenericRenderer.globalRenderer = self

    def addLine(self, line, r, g, b):
            self.lineBatch.add(2, pyglet.gl.GL_LINES, None,
                             ('v2f', (line.start.real, line.start.imag, line.end.real, line.end.imag)),
                             ('c3B', (r,g,b, r,g,b))
            )
    def addPath(self, path, r, g, b):
        for shape in path:
            for x in range(0, 99):
                x1 = x / 100.0
                x2 = x1 + 0.01
                self.addLine(Line(start=shape.point(x1), end=shape.point(x2)), r, g, b)

    def addPoint(self, point, r, g, b):
        self.pointBatch.add(1, pyglet.gl.GL_POINTS, None,
                           ('v2f', (point.real, point.imag)),
                           ('c3B', (r, g, b))
                           )

    def updateDisplay(self, s):
        self.window.clear()
        self.lineBatch.draw()
        self.pointBatch.draw()

    def runLoop(self):
        pyglet.clock.schedule_interval(self.updateDisplay, 1 / 30.0)
        pyglet.app.run()


from svgpathtools import Line
import math
import numpy
from sys import float_info

# Represents your average y = mx + b line
class InfLine:
    def __init__(self, m, center):
        self.m = m
        self.center = center
        # Calculate b such that the line includes the point `center`
        self.b = center.imag - (center.real * m)

    def x_for_y(self, y):
        return (y - self.b) / self.m;

    def y_for_x(self, x):
        return (self.m * x) + self.b

    def invertSlope(self):
        if self.m is not 0:
            m2 = -1.0 / self.m
            # Find a new b to maintain the center
            b2 = (self.center.imag - (m2 * self.center.real))

            self.m = m2
            self.b = b2
    def matchInfLine(self, infLine):
        self.b = infLine.b
        self.m = infLine.m
        self.center = complex(infLine.center.real, infLine.center.imag)

    def matchLine(self, line):
        dx = line.start.real - line.end.real
        if dx == 0:
            self.m = float_info.max
        else:
            dy = line.start.imag - line.end.imag
            self.m = dy / dx

        self.center = line.point(0.5)
        self.b = self.center.imag - (self.center.real * self.m)

    def moveToIncludePoint(self, point):
        self.b = point.imag - (point.real * self.m)
        self.center = point

    def intersectionPointWithInfLine(self, il):
        if self.m == il.m:
            return None

        x = (il.b - self.b) / (self.m - il.m)
        y = self.y_for_x(x)
        return complex(x, y)

    def to_svg_Line(self, center, length):
        dist = length / 2.0
        # Find the two values of x that are "dist" down each
        #  side of the line.
        # I did this on paper, and its just a quadratic equation that
        #  needs to be solved. Nothing a little numpy can't fix.
        xRoots = numpy.roots([ (1 + math.pow(self.m, 2.0) ),
                               ((-2 * center.real * math.pow(self.m, 2.0)) - (2*center.real)),
                               (math.pow(center.real, 2.0)*math.pow(self.m, 2.0)) + (math.pow(center.real, 2.0)) - (math.pow(dist, 2.0))  ])

        assert(len(xRoots) == 2)
        assert(numpy.isreal(xRoots[0]))
        assert (numpy.isreal(xRoots[1]))

        return Line( start=complex(xRoots[0], self.y_for_x(xRoots[0]) ),
                     end= complex(xRoots[1], self.y_for_x(xRoots[1])) )


        # h = length / 2.0
        # ext1 = complex( (center.real + h), self.y_for_x(center.real + h) )
        # ext2 = complex( ext1.real - length, ext1.imag - length)
        # return Line(start=ext1, end=ext2)

def getBoxDiagonalLength(left, right, top, bottom):
    return math.sqrt( math.pow(left-right, 2) + math.pow(top-bottom, 2) )

def getIntersectionPathFromBox(infLine, left, right, top, bottom):
    # Intersect the line with all the sides of the box and
    #  take the two points inside the box.
    # This will always be on the top and bottom
    # or on the left and right sides.
    p1 = complex(left, infLine.y_for_x(left))
    p2 = complex(right, infLine.y_for_x(right))
    l1 = Line(start=p1,end=p2)

    p3 = complex(infLine.x_for_y(top), top)
    p4 = complex(infLine.x_for_y(bottom), bottom)
    l2 = Line(start=p3, end=p4)

    if l1.length() < l2.length():
        return l2
    else:
        return l1

def invertLine(line, scale=1.0):
    center = line.point(0.5)

    # Shift to origin
    p1 = line.start - center
    p2 = line.end - center

    p1 = complex(p2.imag, p1.real) * scale
    p2 = complex(p1.imag , p2.real) * scale

    # Shift back
    p1 = p1 + center
    p2 = p2 + center

    # "Rotate"
    rotated = Line(start=p1, end=p2)
    return rotated

def projectPointOntoInfLine(point, infLine):
    i = InfLine(1, (0+0j))
    i.matchInfLine(infLine)
    i.invertSlope()
    i.moveToIncludePoint(point)

    return infLine.intersectionPointWithInfLine(i)



def projectLineOntoInfLine(line, infLine):
    return Line(start=projectPointOntoInfLine(line.start, infLine), end=projectPointOntoInfLine(line.end, infLine) )

def getDistanceBetweenPoints(p1, p2):
    return math.sqrt( math.pow(p1.real - p2.real, 2) + math.pow(p1.imag - p2.imag, 2) )

# Creates a line with the given y intercept (b) that covers
#  the given bounding box.
def defineLine(length=1000, m=45.0, b=0, upperLeft=(0+0j), size=(0+0j)):
    None

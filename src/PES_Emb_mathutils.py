from svgpathtools import Line
import math
import numpy

# Represents your average y = mx + b line
class InfLine:
    def __init__(self, m, center):
        self.m = m
        self.b = center.imag - (center.real * m)

    def x_for_y(self, y):
        return (y - self.b) / self.m;

    def y_for_x(self, x):
        return (self.m * x) + self.b

    def invertSlope(self):
        if self.m is not 0:
            self.m = 1 / self.m

    def to_svg_Line(self, center, length):
        # center = 2.0+0j
        # length = 2.0*math.pow(8.0, 0.5)
        # self.m = 1.0
        # self.b = -2

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

        return Line(start=(xRoots[0], self.y_for_x(xRoots[0])),
                    end=(xRoots[1], self.y_for_x(xRoots[1])))


        # h = length / 2.0
        # ext1 = complex( (center.real + h), self.y_for_x(center.real + h) )
        # ext2 = complex( ext1.real - length, ext1.imag - length)
        # return Line(start=ext1, end=ext2)

def getBoxDiagonalLength(left, right, top, bottom):
    return math.sqrt( math.pow(left-right, 2) + math.pow(top-bottom, 2) )

def getStartAndEndPointsOfLineInBox(infLine, left, right, top, bottom):
    # Intersect the line with all the sides of the box and
    #  take the two points inside the box.
    # This will always be on the top and bottom
    # or on the left and right sides.
    p1 = complex(left, infLine.y_for_x(left))
    p2 = complex(right, infLine.y_for_x(right))

    p3 = complex(top, infLine.x_for_y(top))
    p4 = complex(bottom, infLine.x_for_y(bottom))

    if p1.imag <= top and p1.imag >= bottom:
        return p3, p4
    else:
        return p1, p2



# Creates a line with the given y intercept (b) that covers
#  the given bounding box.
def defineLine(length=1000, m=45.0, b=0, upperLeft=(0+0j), size=(0+0j)):
    None

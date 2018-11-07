from svgpathtools import Line
import math

class InfLine:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def x_for_y(self, y):
        return (y - self.b) / m;

    def y_for_x(self, x):
        return (self.m * x) + self.b

    def to_svg_Line(self, center, length):
        h = length / 2.0
        ext1 = complex(  )

def getBoxDiagonalLength(left, right, top, bottom):
    return math.sqrt( math.pow(left-right, 2) + math.pow(top-bottom, 2) )

def getStartAndEndPointsOfLineInBox(m, b, left, right, top, bottom):
    # Intersect the line with all the sides of the box and
    #  take the two points inside the box.
    # This will always be the top and bottom
    # or the left and right sides.
    p1 = complex((top - b) / m, top);
    p2 = complex(left, m*left + b)



# Creates a line with the given y intercept (b) that covers
#  the given bounding box.
def defineLine(length=1000, m=45.0, b=0, upperLeft=(0+0j), size=(0+0j)):
    None

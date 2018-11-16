import svgpathtools
from PES_Emb_mathutils import *
from PES import Stitch
import numpy

def loadVectorGraphic(filename):
    svg = None
    try:
        svg = svgpathtools.svg2paths(filename)
    except:
        print("Couldn't load SVG file. Perhaps it doesn't exist?")

    return svg

def makeStitchLines(shape, threadWidth=0.04, slope=1):
    stitchLines = []

    # Get the bounds of the shape
    left, right, bottom, top = shape.bbox()
    width = right - left
    height = top - bottom
    center = complex( (left + right) / 2, (top + bottom) / 2)

    # Intersect a line with the given angle over and over
    #  to find where stitches should start/end.
    # If the shape isn't convex, the line might intersect
    #  more than once but should always intersect an even
    #  number of times (as long as the shape is closed.)

    # Place the intersection line at various points along
    # a straight path that has the opposite slope.
    # The path should cross through the center of the bounding-
    #  box square.
    intersectionPath = InfLine(m=slope, center=center)
    intersectionPath.invertSlope()
    p1, p2 = getStartAndEndPointsOfLineInBox(intersectionPath, left, right, top, bottom)
    intersectionPath = Line(start=p1, end=p2)
    #intersectionPath = intersectionPath.to_svg_Line(center=center, length=intersectionLineLength)

    # Make sure we cover everything based on the thread width.
    # Line objects can be enumerated from 0 < t < 1
    # Depending on the Line's length, we need to increment t
    # by a value such that we move threadWidth each time.
    intersectionLineInc = (intersectionPath.length() / threadWidth) + 1

    return stitchLines
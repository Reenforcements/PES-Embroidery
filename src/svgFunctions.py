import svgpathtools
from PES_Emb_mathutils import *
from PES import Stitch

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

    # Pick the origin based on whether or not the slope is positive
    if slope > 0:
        origin = complex(left, top)
    else:
        origin = complex(right, top)

    # Place the intersection line at various points along
    # a straight path that has the opposite slope.
    if slope is not 0:
        pSlope = 1 / slope
    else:
        pSlope = 0

    # The path should cross through the center of the bounding-
    #  box square.

    return stitchLines
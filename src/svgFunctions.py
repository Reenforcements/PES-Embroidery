import svgpathtools
from PES_Emb_mathutils import *
from PES_render_utils import *
from PES import Stitch
import re
import numpy

def loadVectorGraphic(filename):
    svg = None
    attributes = None
    try:
        svg, attributes = svgpathtools.svg2paths(filename)
    except:
        print("Couldn't load SVG file. Perhaps it doesn't exist?")

    return svg, attributes

def getColorOfPathAtIndex(attributes, index):
    color = (0, 0, 0)

    if attributes is None:
        return color

    try:
        m = re.search("fill:#(\S{6})", attributes[index]["style"])
        last = m.group(1)
        r = int(last[0:2], 16)
        g = int(last[2:4], 16)
        b = int(last[4:6], 16)
        color = (r, g, b)
    except:
        None

    return color

def makeStitchLines(shape, fillColor=(0,0,0), threadWidth=0.04, slope=1):
    """

    :type shape: svgpathtools.CubicBezier
    """
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

    #print("Start and end points: {}, {}".format(p1,p2))
    #intersectionPath = intersectionPath.to_svg_Line(center=center, length=intersectionLineLength)

    # Make sure we cover everything based on the thread width.
    # Line objects can be enumerated from 0 < t < 1
    # Depending on the Line's length, we need to increment t
    # by a value such that we move threadWidth each time.
    totalIntersections = int((intersectionPath.length() / threadWidth)) + 1
    pathLength = intersectionPath.length()
    tIncrementAmount = pathLength / float(totalIntersections)
    # Get the max length of the intersection lines we'll need
    intersectionLineLength = getBoxDiagonalLength(left, right, top, bottom)

    print("Performing up to {} intersections along path: {}".format(totalIntersections, intersectionPath))
    print("(From {} to {})".format(intersectionPath.point(0), intersectionPath.point(1.0)))

    GenericRenderer.globalRenderer.addPath(shape, 50, 120, 255)

    for x in range(0, totalIntersections):
        # Get a new (infinite) line using the point at the current t value
        #  as the center
        center = intersectionPath.point((tIncrementAmount * x) / pathLength)
        GenericRenderer.globalRenderer.addPoint(center, 255, 255, 0)
        i = InfLine(m=slope, center=center)
        # Convert it to a bezier line
        l = i.to_svg_Line(center=center, length=intersectionLineLength)
        GenericRenderer.globalRenderer.addLine(l, 255, 255, 255)

        # Intersect with the shape
        intersections = shape.intersect(l)
        if len(intersections) % 2 is not 0:
            s = "Number of intersections should always be even (its {} ). Make sure all shapes are closed shapes.".format(len(intersections))
            raise Exception(s)

        # Iterate through the intersections to find where to put stitches
        for i in range(0, len( intersections )/2):
            start = l.point(intersections[i][1][0])
            end = l.point(intersections[i+1][1][0])
            # Create a stitch for the given start and end points
            l = Line(start=start, end=end)
            s = Stitch(line=l)

            stitchLines.append(s)

            # Draw debug lines
            GenericRenderer.globalRenderer.addLine(l, fillColor[0], fillColor[1], fillColor[2])


    return stitchLines

# Take all the stitches we created and actually make
#  a continuous set of commands for the machine to follow.
def createStitchRoutine(basicStitches):
    for shapeStitches in basicStitches:
        for stitch in shapeStitches:
            # Remove lines that are super short
            if stitch.length() < 5.0:
                continue


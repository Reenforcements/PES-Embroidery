import svgpathtools
from PES_Emb_mathutils import *
from PES_render_utils import *
from PES import *
import re
import numpy

class StitchLevel:
    def __init__(self, lines, infLine):
        self.lines = lines
        self.infLine = infLine
        #self.barriers = []

        # Make barriers out of the spaces between the lines
        # numBarriers = len(lines) - 1
        # for x in range(0, numBarriers):
        #     p1 = self.lines[x].end
        #     p2 = self.lines[x+1].start
        #     b = Line(start=p1, end=p2)
        #     #GenericRenderer.globalRenderer.addLine(b, 55, 55, 55)
        #     # Rotate line around center
        #     invertedB = invertLine(b)
        #     self.barriers.append(invertedB)

            #GenericRenderer.globalRenderer.addLine(invertLine(b, scale = 1), 55, 0, 255)

    def lineFallsInValidProjectionOfUngroupedLine(self, line, ungroupedLine):
        # Project the line onto the intersection line
        pLine = projectLineOntoInfLine(line, self.infLine)
        #GenericRenderer.globalRenderer.addLine(pLine, 255, 0, 255)
        ipLine = invertLine(pLine)

        # # Avoid rounding errors by doing this with two
        # #  perpendicular lines at the start and end points.
        # l1 = InfLine(1, (0+0j))
        # l1.matchLine(ipLine)
        # l1.moveToIncludePoint(pLine.start)
        # l1 = l1.to_svg_Line(pLine.start, 1)
        #
        # l2 = InfLine(1, (0+0j))
        # l2.matchLine(ipLine)
        # l2.moveToIncludePoint(pLine.end)
        # l2 = l2.to_svg_Line(pLine.end, 1)
        l = ungroupedLine

        lLength = l.length()
        pLength = pLine.length()
        maxDist = max(lLength, pLength)

        # For a line to be valid with another line,
        #  the two points of one line can't be farther
        #  than maxDist more than once.
        dists = [Line(l.start, pLine.start).length(),
                 Line(l.start, pLine.end).length(),
                 Line(l.end, pLine.start).length(),
                 Line(l.end, pLine.end).length()]

        totalTooFar = 0
        for d in dists:
            if d > maxDist:
                totalTooFar += 1

        if totalTooFar <= 1:
            return True

        return False

def loadVectorGraphic(filename):
    svg = None
    attributes = None
    try:
        svg, attributes = svgpathtools.svg2paths(filename)
    except Exception as e:
        print("Couldn't load SVG file. Perhaps it doesn't exist?")
        print(e.message)

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

def makeStitchLevels(shape, fillColor=(0,0,0), threadWidth=2, slope=1, debug=False):
    """

    :type shape: svgpathtools.CubicBezier
    """
    stitchLevels = []

    # Draw the shape
    GenericRenderer.globalRenderer.addPath(shape, 50, 120, 255)

    # Get the bounds of the shape
    left, right, bottom, top = shape.bbox()
    width = right - left
    height = top - bottom
    center = complex( (left + right) / 2, (top + bottom) / 2)
    # Draw the bounding box
    GenericRenderer.globalRenderer.addLine(Line(  start=complex(left,top)  ,end=complex(right,top) ), 0, 255, 255)
    GenericRenderer.globalRenderer.addLine(Line(start=complex(right, top), end=complex(right, bottom)), 0, 255, 255)
    GenericRenderer.globalRenderer.addLine(Line(start=complex(right, bottom), end=complex(left, bottom)), 0, 255, 255)
    GenericRenderer.globalRenderer.addLine(Line(start=complex(left, bottom), end=complex(left, top)), 0, 255, 255)
    GenericRenderer.globalRenderer.addPoint(center, 0, 255, 255)

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
    GenericRenderer.globalRenderer.addLine(
        Line(start=complex(1000, intersectionPath.y_for_x(1000)),
             end=complex(-1000, intersectionPath.y_for_x(-1000)) ), 0, 255, 0)
    intersectionPath.invertSlope()
    GenericRenderer.globalRenderer.addLine(
        Line(start=complex(1000, intersectionPath.y_for_x(1000)),
             end=complex(-1000, intersectionPath.y_for_x(-1000))), 0, 255, 0)

    intersectionPath = getIntersectionPathFromBox(intersectionPath, left, right, top, bottom)

    GenericRenderer.globalRenderer.addLine(intersectionPath, 255, 255, 0)

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

    for x in range(0, totalIntersections):
        # Get a new (infinite) line using the point at the current t value
        #  as the center
        center = intersectionPath.point((tIncrementAmount * x) / pathLength)
        #GenericRenderer.globalRenderer.addPoint(center, 255, 255, 0)
        infLine = InfLine(m=slope, center=center)
        # Convert it to a bezier line
        l = infLine.to_svg_Line(center=center, length=intersectionLineLength)
        #GenericRenderer.globalRenderer.addLine(l, 255, 255, 255)

        # Intersect with the shape
        intersections = shape.intersect(l)
        if len(intersections) % 2 is not 0:
            s = "Number of intersections should always be even (its {} ). Make sure all shapes are closed shapes.".format(len(intersections))
            if debug:
                print(s)
            else:
                raise Exception(s)

        intersectionPoints = []
        # Get the intersection points and order them by location
        #  on the intersection line.
        for i in range(0, len( intersections )):
            p1 = l.point(intersections[i][1][0])
            intersectionPoints.append(p1)

        def dist1(p):
            return getDistanceBetweenPoints(p, l.start)

        intersectionPoints.sort(key=dist1)

        if debug:
            #print("{} intersection points for this iteration.".format(len(intersectionPoints)))
            for i in intersectionPoints:
                None#GenericRenderer.globalRenderer.addPoint(i, 255, 0, 255)

        genericColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

        currentLines = []

        # Iterate through the intersections to find where to put stitches
        for i in range(0, len( intersectionPoints )/2):
            start = intersectionPoints[i*2]
            end = intersectionPoints[(i*2)+1]

            # Create a stitch for the given start and end points
            stitchLine = Line(start=start, end=end)

            currentLines.append(stitchLine)

            # Draw debug lines
            if debug:
                GenericRenderer.globalRenderer.addLine(stitchLine, genericColors[i%6][0], genericColors[i%6][1], genericColors[i%6][2])
            else:
                GenericRenderer.globalRenderer.addLine(stitchLine, fillColor[0], fillColor[1], fillColor[2])

        stitchLevel = StitchLevel(currentLines, infLine)
        stitchLevels.append(stitchLevel)

    return stitchLevels

def prependShapeTraces(shapePaths, subshapeLineGroups, maxStitchDistance=10.0):
    for i, shape in enumerate(shapePaths):
        lineGroups = subshapeLineGroups[i]

        print("Shape length: {}".format(shape.length()))

        increment = int( round(shape.length() / maxStitchDistance) )
        traceLines = []
        for x in range(0, increment):
            p1 = shape.point(float(x) / increment)
            p2 = shape.point(min(float(x + 1) / increment, 1.0))
            traceLines.append(Line(start=p1, end=p2))
        lineGroups.insert(0, traceLines)

    return subshapeLineGroups




def switchPointsInLine(line):
    return Line(start=line.end, end=line.start)

def pointWithinPoint(p1, p2, dist):
    return math.sqrt( math.pow(p1.real - p2.real, 2) + math.pow(p1.imag - p2.imag, 2) ) <= dist

# Take all the stitches we created and actually make
#  a continuous set of stitches for the machine to follow
#  on a per sub-shape basis.
# This should return a list of sublists, with each sublist
#  containing an array of continuous stitch lines.
def createSubshapeLineGroups(subshapeLevelGroups, mode, fillColors, threadWidth=2, maxStitchDistance=10.0):

    subshapeLineGroups = []
    lastUsedGroups = []
    # For each set of lines corresponding to each SVG shape...
    for subshapeLevels in subshapeLevelGroups:
        # Find an order of lines that works with (relatively) minimum jumping.
        # This requires us to group lines by continuity.
        # Each group is stitchable with no jumps.
        # Jumps will occur between these groups.
        # This holds lists of lines that can be stitched continuously with no jumping.
        lineGroups = []
        # SVG files can have multiple shapes
        # Hold all the line groups in "shapeLineGroups"
        # This contains a list of lineGroups, one for each subshape.
        subshapeLineGroups.append(lineGroups)

        # Each level can contain multiple lines
        for level in subshapeLevels:

            newUsedGroups = []

            # Check each ungrouped line in the level
            level.lines.reverse()
            for ungroupedLine in level.lines:
                # Remove lines that are super short
                # TODO: Find a good value for this.
                #if ungroupedLine.length() < ???:
                #    continue

                # Does the line connect to any of the current groups?
                foundGroup = None
                for lineGroup in lastUsedGroups:
                    lastLine = lineGroup[-1]

                    # Does it cross a barrier?
                    if level.lineFallsInValidProjectionOfUngroupedLine( lastLine, ungroupedLine ):
                        foundGroup = lineGroup
                        break

                # Did we find a group that works?
                if foundGroup is None:
                    # No current group works for this line.
                    # We probably started intersecting a new part of the shape
                    # Start a new group
                    foundGroup = []
                    lineGroups.append(foundGroup)

                foundGroup.append(ungroupedLine)

                newUsedGroups.append(foundGroup)
                # This group found a member. It's off the table
                #  for the rest of this iteration.
                if foundGroup in lastUsedGroups:
                    lastUsedGroups.remove(foundGroup)

            lastUsedGroups = newUsedGroups

        print("Made {} groups for a shape.".format(len(lineGroups)))

    # Break up the lines into intermediate stitches.
    # We don't want giant stitches traversing the whole object.
    # We want little stitches along the way.
    def breakUpBigStitchLine(l):
        # Not less than one segment
        segments = max(1, int( round(l.length() / maxStitchDistance) ) )
        increment = 1.0 / float(segments)
        lines = []
        for x in range(0, segments):
            p1 = l.point( x*increment )
            p2 = l.point( min((x+1)*increment, 1.0) )
            lines.append(Line(start=p1,end=p2))
        return lines

    # Holds groups for every subshape
    shortenedSubshapeLineGroups = []

    if mode == "zigzag":
        for lineGroups in subshapeLineGroups:
            # Holds the groups for a single subshhape
            shortenedLineGroups = []
            shortenedSubshapeLineGroups.append(shortenedLineGroups)
            for lineGroup in lineGroups:
                # Holds shortened lines for a single continuous region
                shortenedLines = []
                shortenedLineGroups.append(shortenedLines)
                lastLine = None
                for line in lineGroup:
                    if lastLine is not None:
                        # Make a line connecting this line and the previous one.
                        l = Line(lastLine.end, line.start)
                        shortenedLines.extend( breakUpBigStitchLine(l) )
                    shortenedLines.extend(breakUpBigStitchLine(line))
                    lastLine = line
    elif mode == "closest":
        for lineGroups in subshapeLineGroups:
            # Holds the groups for a single subshhape
            shortenedLineGroups = []
            shortenedSubshapeLineGroups.append(shortenedLineGroups)
            for lineGroup in lineGroups:
                # Holds shortened lines for a single continuous region
                shortenedLines = []
                shortenedLineGroups.append(shortenedLines)
                lastLine = None
                for line in lineGroup:
                    if lastLine is not None:
                        # Which point on the next line is closest?
                        d1 = Line(lastLine.end, line.start).length()
                        d2 = Line(lastLine.end, line.end).length()
                        # Make a line connecting this line and the previous one.
                        if d2 < d1:
                            # Invert the line
                            line = Line(line.end, line.start)
                            l = Line(lastLine.end, line.start)
                            shortenedLines.extend(breakUpBigStitchLine(l))
                        else:
                            l = Line(lastLine.end, line.start)
                            shortenedLines.extend( breakUpBigStitchLine(l) )
                    else:
                        # The first line.
                        shortenedLines.extend(breakUpBigStitchLine(line))

                    shortenedLines.extend(breakUpBigStitchLine(line))
                    lastLine = line

        # Render the lines
        GenericRenderer.globalRenderer.clearAll()
        curColor = 0
        for lineGroups in shortenedSubshapeLineGroups:
            for lineGroup in lineGroups:
                curColor += 1
                currentColor = PES.colors[curColor % len(PES.colors)]
                for line in lineGroup:
                    # Add slight color variation to be able to see individual stitches.
                    variation = 50
                    c1 = min(255, max(0, currentColor[1] + int(round(random.uniform(-variation, variation))) ))
                    c2 = min(255, max(0, currentColor[2] + int(round(random.uniform(-variation, variation)))))
                    c3 = min(255, max(0, currentColor[3] + int(round(random.uniform(-variation, variation)))))
                    GenericRenderer.globalRenderer.addLine(line, c1, c2, c3)

    return shortenedSubshapeLineGroups

def createPECStitchRoutines(subshapeLineGroups, fillColors, threadWidth, maxStitchDistance):
    # Add color change, convert lines to stitches and add jump commands
    PECCommands = []
    maxDist = math.sqrt(2 * math.pow(threadWidth, 2))

    for i, subshapeLineGroup in enumerate(subshapeLineGroups):
        # Create the color change command.
        fillColor = fillColors[i]
        colorData = PES.getClosestColor(fillColor)

        # First color is automatically set.
        if i != 0:
            colorChange = ColorChange(colorIndex=colorData[0], indexInColorList=i )
            PECCommands.append(colorChange)

        for singleLineGroup in subshapeLineGroup:
            # Was the last command a stitch?
            if len(PECCommands) > 0 and isinstance(PECCommands[-1], Stitch):
                lastStitch = PECCommands[-1]
                # Is the distance greater than the minimum?
                if pointWithinPoint(lastStitch.point, singleLineGroup[0].start, maxDist) is not True:
                    # Jump to the location of this shape.
                    jump = Stitch( singleLineGroup[0].start )
                    jump.type = Stitch.TYPE_JUMP
                    PECCommands.append(jump)

            if len(singleLineGroup) > 0:
                PECCommands.append(Stitch(singleLineGroup[0].start))

            for singleLine in singleLineGroup:
                # s = Stitch(singleLine.start)
                # PECCommands.append(s)
                s = Stitch(singleLine.end)
                PECCommands.append(s)

    print("Created {} PEC commands (most are stitches.)".format(len(PECCommands)))
    return PECCommands

def renderPEC(pec):

    PECCommands = pec.commands
    colors = pec.colors

    GenericRenderer.globalRenderer.clearAll()

    lastPoint = (0+0j)
    currentColor = colors[0][1:]
    jumps = []
    for command in PECCommands:
        if isinstance(command, Stitch):
            if command.type is Stitch.TYPE_JUMP:
                jumps.append(Line(lastPoint, command.point))
            else:
                # Regular stitch
                GenericRenderer.globalRenderer.addLine(Line(lastPoint, command.point), currentColor[1], currentColor[2], currentColor[3])

            lastPoint = command.point

        if isinstance(command, ColorChange):
            currentColor = colors[command.indexInColorList][1:]

    # Render all the jumps on top
    for jump in jumps:
        GenericRenderer.globalRenderer.addLine(jump, 255, 255, 255)
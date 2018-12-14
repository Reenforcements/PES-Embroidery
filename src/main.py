import argparse
import sys
from svgFunctions import *
import pyembroidery
from utilities import *
from PES import *
from PES_render_utils import *

# Argument parsing
parser = argparse.ArgumentParser(description="Converts an SVG file into a PES embroidery file.")

parser.add_argument("-i", dest="inputFile", type=str, action='store', required=True, help="The SVG file to be converted.")
parser.add_argument("-o", dest="outputFile", type=str, action='store', default="output.PES", required=False, help="The output PES file.")
parser.add_argument("-t", dest="threadWidth", type=float, action='store', default=2.5, required=False,
                    help="The thread width to use. This controls how close parallel stitches are to one another.")
parser.add_argument("-m", dest="maxStitchDistance", type=float, action='store', default=10.0, required=False,
                    help="The maximum distance the sewing machine can traverse before it has to make a stitch.")
parser.add_argument("-l", dest="slope", type=float, action='store', default=-1.0, required=False,
                    help="The slope of the line to use when performing intersections.")
parser.add_argument("-s", dest="style", nargs=1, choices=["zigzag", "closest"], default=["closest"], action='store',
                    help="The method uses to attach parallel stitches together.")
parser.add_argument("--noOutline", dest="noOutline", action='store_true', help="Do not add outline stitches to shapes.")

parser.add_argument("-d", dest="debug", action='store_true', help="Print debug info and show a rendering of the PES in a window.")
parser.add_argument("-r", dest="debugRendering", action='store_true', help="Generate a debug image next to the output file.")

args = parser.parse_args()

# Create a generic renderer so we can see what's happening
# (Only actually creates a window if the debug argument is set.)
renderer = GenericRenderer(args.debug)

# Load the SVG file from disk
svg = loadVectorGraphic(args.inputFile)
paths, attributes = svg

if paths is None:
    print("SVG contains no paths.")
    sys.exit(0)

threadWidth = args.threadWidth
maxStitchDistance = args.maxStitchDistance

# Enumerate the shapes in the SVG to find where stitches should go.
subshapeLevelGroups = []
fillColors = []
PECColors = []
for i, shape in enumerate(paths):
    fillColor = getColorOfPathAtIndex(attributes,i)
    fillColors.append(fillColor)
    PECColors.append(PES.getClosestColor(fillColor))

    print("Doing shape {} with fill color {}".format(shape, fillColor))
    print("Closest color: {}".format( PES.getClosestColor(fillColor) ))

    # Fill color here is only for debugging.
    levels = makeStitchLevels(shape, fillColor, debug=args.debug, slope=(-args.slope), threadWidth=threadWidth)
    # Append the stitches as their own array so we can separate by colors
    subshapeLevelGroups.append(levels)

# Make the stitches into continuous groups.
# This also breaks the long stitches up into little ones.
print("Using stitch style: {}".format(args.style[0]))
subshapeLineGroups = createSubshapeLineGroups(subshapeLevelGroups, mode=args.style[0], fillColors=fillColors, threadWidth=threadWidth, maxStitchDistance=maxStitchDistance)

# Creates stitch outlines for each shape
if args.noOutline is not True:
    subshapeLineGroups = prependShapeTraces(paths, subshapeLineGroups, maxStitchDistance=maxStitchDistance)

#DEBUG lines: [[[Line(0+0j, 300+0j), Line(300+0j, 300+300j), Line(300+300j, 0+300j) , Line(0+300j, 0+0j)]]]
PECCommands = createPECStitchRoutines(subshapeLineGroups, fillColors, threadWidth, maxStitchDistance=maxStitchDistance)

left, right, bottom, top = shape.bbox()

pec = PEC(label="simple", colors=PECColors, commands=PECCommands, size=complex(right - left, top - bottom))

# Render the PEC commands
renderPEC(pec)

pes = PES(PEC=pec, shape=shape)
encodedPES = pes.encode()

with open(args.outputFile, "w") as f:
    f.write(encodedPES)

print("Wrote {} to disk.".format(args.outputFile))

if args.debugRendering:
    loadedPES = pyembroidery.read(args.outputFile)
    if loadedPES is not None:
        print("Generating debug image.")
        debugImagePath = replaceFilenameAndExtensionFromPath(args.outputFile, "debugPicture" + getFilenameAndExtensionFromPath(args.outputFile)[0], "png")
        pyembroidery.write_png(loadedPES, debugImagePath)
        print("Image written to disk: {}".format(debugImagePath))
    else:
        print("Couldn't find output file.")

    # Show what the program did in the debug window
    #  until the user quits.
    GenericRenderer.globalRenderer.runLoop()
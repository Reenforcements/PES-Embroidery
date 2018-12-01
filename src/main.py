import argparse
import sys
from svgFunctions import *
import pyembroidery
from utilities import *
from PES import *
from PES_render_utils import *

# Argument parsing
parser = argparse.ArgumentParser(description="Converts an SVG file into a PES embroidery file.")

parser.add_argument("-i", dest="inputFile", type=str, action='store', required=True)
parser.add_argument("-o", dest="outputFile", type=str, action='store', default="output.PES", required=False)
parser.add_argument("-d", dest="debug", action='store_true')

args = parser.parse_args()

if args.debug:
    # Create a generic renderer so we can see what's happening
    renderer = GenericRenderer()

# Load the SVG file from disk
svg = loadVectorGraphic(args.inputFile)
paths, attributes = svg

if paths is None:
    sys.exit(0)

threadWidth = 0.5

# Enumerate the shapes in the SVG to find where stitches should go.
levelGroups = []
fillColors = []
PECColors = []
for i, shape in enumerate(paths):
    fillColor = getColorOfPathAtIndex(attributes,i)
    fillColors.append(fillColor)
    PECColors.append(PES.getClosestColor(fillColor))

    print("Doing shape {} with fill color {}".format(shape, fillColor))
    print("Closest color: {}".format( PES.getClosestColor(fillColor) ))

    # Fill color here is only for debugging.
    levels = makeStitchLevels(shape, fillColor, debug=args.debug, threadWidth=threadWidth)
    # Append the stitches as their own array so we can separate by colors
    levelGroups.append(levels)

# Make the stitches into a continuous set of commands
PECCommands = createStitchRoutine(levelGroups, fillColors=fillColors, threadWidth=threadWidth)

# Render the PEC commands
renderPECCommands(PECCommands)

pec = PEC(label="pec1", colors=PECColors, commands=PECCommands)
pes = PES(PEC=pec)
encodedPES = pes.encode()

with open(args.outputFile, "w") as f:
    f.write(encodedPES)

print("Wrote {} to disk.".format(args.outputFile))

if args.debug:
    loadedPES = pyembroidery.read(args.outputFile)
    if loadedPES is not None:
        print("Generating debug image.")
        pyembroidery.write_png(loadedPES, replaceFilenameAndExtensionFromPath(args.inputFile, "debugPicture", "png"))
        print("Image written to disk.")
    else:
        print("Couldn't find output file.")

    # Show what the program did in the debug window
    #  until the user quits.
    GenericRenderer.globalRenderer.runLoop()
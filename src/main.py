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
if paths is None or attributes is None:
    sys.exit(0)

# Enumerate the shapes in the SVG to find where stitches should go.
for shape in paths:
    print(shape)
    stitchLines = makeStitchLines(shape)

pes = PES()
pes.encode()

if args.debug:
    loadedPES = pyembroidery.read(args.outputFile)
    if loadedPES is not None:
        print("Generating debug image.")
        pyembroidery.write_png(loadedPES, replaceFilenameAndExtensionFromPath(args.inputFile, "debugPicture", "png"))
    else:
        print("Couldn't find output file.")

    # Show what the program did in the debug window
    #  until the user quits.
    GenericRenderer.globalRenderer.runLoop()
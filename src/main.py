import argparse
import sys
from svgFunctions import *


parser = argparse.ArgumentParser(description="Converts an SVG file into a PES embroidery file.")

parser.add_argument("-i", dest="inputFile", type=str, action='store', required=True)

args = parser.parse_args()

# Load the SVG file from disk
svg = loadVectorGraphic(args.inputFile)
paths, attributes = svg
if paths is None or attributes is None:
    sys.exit(0)

# Enumerate the shapes in the SVG to find where stitches should go.
for shape in paths:

    print(shape)

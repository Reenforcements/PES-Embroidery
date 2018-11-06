import svgpathtools

def loadVectorGraphic(filename):
    svg = None
    try:
        svg = svgpathtools.svg2paths(filename)
    except:
        print("Couldn't load SVG file. Perhaps it doesn't exist?")

    return svg

def 
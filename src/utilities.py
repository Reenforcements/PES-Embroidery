
from re import search

def getFilenameAndExtensionFromPath(path):
    return search("(\w+)\.(\w{3})", path).groups()

def replaceFilenameAndExtensionFromPath(path, filename, extension):
    # Get the path without the filename
    oldFilename, oldPath = getFilenameAndExtensionFromPath(path)
    path = path[0:-(len(oldFilename) + len(oldPath) + 1)]
    return path + filename + "." + extension

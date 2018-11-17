# 11/16

I haven't had the chance to work on this in a while. That's ok, this weekend is partially dedicated to coding this project (among other things.)

I added a debug flag to generate an image based on the exported PES. This will be my first and most basic testing. I'm starting to really understand the format.

Man, the PEC stitch coordinate system is weird. 

Okay, it's less weird after finding [this resource](https://edutechwiki.unige.ch/en/Embroidery_format_PEC) which explains it much better. Apparently stitches have a short and long form. I'm going to always use the long form to make things simpler. That way, I won't have to worry about making multiple jumps or not.

I'd like to try to optimize the groups of stitches to minimize jumps and make the jumps optimal if possible.

In version 1 of the .PES format, the PES and PEC sections contain the same data.

I think I'm going to try totally skipping the PES section because it won't be needed for embroidering, which is the purpose of this software.

# 11/6

Trying to make sense of the "d" string in the path object. I need to be able to parse this myself I think to find intersections.

Found svgpathtools Python library. This can load SVG files and even do intersections. I'm going to try it. I don't regret the research I did on Bezier curves though. Its always cool to know more. Prerequisites are numpy and svgwrite.

I think I'll need to sort the stitches so the regular ones go together and the **jump stitches are minimized**. This sounds like a ROUTING PROBLEM!

Stitches can be made from the start to end or from the end to the start. The stitch doesn't care and it will look the same in the end. I should use this to my advantage when filling shapes with stitches and also jumping from one stitch group to another. I might want a renderer that shows all this in detail, like how Simplify3D has a GCode visualizer that shows all lines but also retractions and movements.

# 11/5

It turns out Bezier paths are just interpolations between mutliple points. They're much simpler than I thought.
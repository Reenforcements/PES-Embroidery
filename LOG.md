# 11/6

Trying to make sense of the "d" string in the path object. I need to be able to parse this myself I think to find intersections.

Found svgpathtools Python library. This can load SVG files and even do intersections. I'm going to try it. I don't regret the research I did on Bezier curves though. Its always cool to know more. Prerequisites are numpy and svgwrite.

I think I'll need to sort the stitches so the regular ones go together and the **jump stitches are minimized**. This sounds like a ROUTING PROBLEM!

Stitches can be made from the start to end or from the end to the start. The stitch doesn't care and it will look the same in the end. I should use this to my advantage when filling shapes with stitches and also jumping from one stitch group to another. I might want a renderer that shows all this in detail, like how Simplify3D has a GCode visualizer that shows all lines but also retractions and movements.

# 11/5

It turns out Bezier paths are just interpolations between mutliple points. They're much simpler than I thought.
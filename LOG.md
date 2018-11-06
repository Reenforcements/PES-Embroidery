# 11/6

Trying to make sense of the "d" string in the path object. I need to be able to parse this myself I think to find intersections.

Found svgpathtools Python library. This can load SVG files and even do intersections. I'm going to try it. I don't regret the research I did on Bezier curves though. Its always cool to know more. Prerequisites are numpy and svgwrite.

# 11/5

It turns out Bezier paths are just interpolations between mutliple points. They're much simpler than I thought.
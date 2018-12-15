# What is this?

This project is a program for a CAD tool design class (ECE 487) at Miami University. The tool converts .SVG vector graphics to .PES embroidery files that can be used by machines such as the Brother SE600.

# Examples

![Apple](https://github.com/Reenforcements/PES-Embroidery/blob/master/DATA/Results/apple.JPG?raw=true)
![Tree](https://github.com/Reenforcements/PES-Embroidery/blob/master/DATA/Results/tree.JPG?raw=true)
![Droplet](https://github.com/Reenforcements/PES-Embroidery/blob/master/DATA/Results/droplet.JPG?raw=true)
![Zigzag](https://github.com/Reenforcements/PES-Embroidery/blob/master/DATA/Results/zigzag.JPG?raw=true)

# Installation

Python is required to run the program.

PES-Embroidery also relies on a number of third party libraries:

- numpy
- svgPathTools
- pyEmbroidery
- pyGlet

These libraries can be easily installed using `pip`.

```
sudo pip install numpy svgpathtools pyembroidery pyglet
```

# Usage (Requires Python)

##### Sample command:
`python -i ./myVectorGraphic.svg -o ./myEmbroideryFile.pes -t 2.5 -d 10 -r -d`

##### Parameter details:

For decimal parameters, 10 units are equal to 1mm.

- `-h` Display parameter help.
- `-i [path]` The full path of the input SVG file.
- `-o [path]` The full path of the output PES file.
- `-t [decimal number]` This will be used as the distance between parallel stitches. Default is 1.5.
- `-m [decimal number]` This is the max distance the sewing machine will travel between stitches. Default is 20.
- `-l [decimal number]` This is the mathematical slope that the stitch lines will have. Default is a slope of 1.
- `-s ['closest' or 'zigzag']` This is the stitch style for connecting parallel stitch groups. The default is closest.
- `--noOutline` If this flag is specified, the embroidery design will not contain stitches that outline each shape.
- `-d` Shows a debug rendering of the embroidery design.
- `-r` Generates a debug rendering picture of the design in the same directory as the output PES file.

# Known Issues

- Some SVG shapes do not convert correctly. I believe this to be a bug in the svgPathTools library.
- The outline of embroidered designs don't tend to line up with the fill stitches.

# References

General PES/PEC information from [here.](https://github.com/frno7/libpes/wiki/PES-format)

General PES/PEC information and colors for PES version 1 taken from [here.](https://edutechwiki.unige.ch/en/Embroidery_format_PEC#Stitch)

[svgPathTools](https://pypi.org/project/svgpathtools/)

[numpy](https://pypi.org/project/numpy/)

[pyEmbroidery](https://pypi.org/project/pyembroidery/)

Tux embroidery demo file from [here.](https://github.com/t2b/embroidery)
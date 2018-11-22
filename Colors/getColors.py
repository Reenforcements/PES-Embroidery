import re
import sys

# This file converts the color table for PES version 1 into something I can use in Python
all = """
1	007	Prussian Blue	A	`#1a0a94`
2	000	Blue	A	`#0f75ff`
3	534	Teal Green	A	`#00934c`
4	070	Corn Flower Blue	A	`#babdfe`
5	800	Red	A	`#ec0000`
6	000	Reddish Brown	A	`#e4995a`
7	620	Magenta	A	`#cc48ab`
8	810	Light Lilac	A	`#fdc4fa`
9	000	Lilac	A	`#dd84cd`
10	502	Mint Green	A	`#6bd38a`
11	214	Deep Gold	A	`#e4a945`
12	208	Orange	A	`#ffbd42`
13	000	Yellow	A	`#ffe600`
14	513	Lime Green	A	`#6cd900`
15	328	Brass	A	`#c1a941`
16	005	Silver	A	`#b5ad97`
17	000	Russet Brown	A	`#ba9c5f`
18	000	Cream Brown	A	`#faf59e`
19	704	Pewter	A	`#808080`
20	900	Black	A	`#000000`
21	000	Ultramarine	A	`#001cdf`
22	000	Royal Purple	A	`#df00b8`
23	707	Dark Gray	A	`#626262`
24	058	Dark Brown	A	`#69260d`
25	086	Deep Rose	A	`#ff0060`
26	323	Light Brown	A	`#bf8200`
27	079	Salmon Pink	A	`#f39178`
28	000	Vermilion	A	`#ff6805`
29	001	White	A	`#f0f0f0`
30	000	Violet	A	`#c832cd`
31	000	Seacrest	A	`#b0bf9b`
32	019	Sky Blue	A	`#65bfeb`
33	000	Pumpkin	A	`#ffba04`
34	010	Cream Yellow	A	`#fff06c`
35	000	Khaki	A	`#feca15`
36	000	Clay Brown	A	`#f38101`
37	000	Leaf Green	A	`#37a923`
38	405	Peacock Blue	A	`#23465f`
39	000	Gray	A	`#a6a695`
40	000	Warm Gray	A	`#cebfa6`
41	000	Dark Olive	A	`#96aa02`
42	307	Linen	A	`#ffe3c6`
43	000	Pink	A	`#ff99d7`
44	000	Deep Green	A	`#007004`
45	000	Lavender	A	`#edccfb`
46	000	Wisteria Violet	A	`#c089d8`
47	843	Beige	A	`#e7d9b4`
48	000	Carmine	A	`#e90e86`
49	000	Amber Red	A	`#cf6829`
50	000	Olive Green	A	`#408615`
51	107	Dark Fuchsia	A	`#db1797`
52	209	Tangerine	A	`#ffa704`
53	017	Light Blue	A	`#b9ffff`
54	507	Emerald Green	A	`#228927`
55	614	Purple	A	`#b612cd`
56	515	Moss Green	A	`#00aa00`
57	124	Flesh Pink	A	`#fea9dc`
58	000	Harvest Gold	A	`#fed510`
59	000	Electric Blue	A	`#0097df`
60	205	Lemon Yellow	A	`#ffff84`
61	027	Fresh Green	A	`#cfe774`
62	000	Applique Material	A	`#ffc864`
63	000	Applique Position	A	`#ffc8c8`
64	000	Applique	A	`#ffc8c8`"""


p = "(\\d+)\\t(\\d+)\\t([^\\t]+)\\tA\\t`#(\\S{6})`"
lines = re.findall(p, all)

colors = []

for line in lines:
    last = line[-1]
    print(last)
    r = int(last[0:2], 16)
    g = int(last[2:4], 16)
    b = int(last[4:6], 16)
    color = (line[2], r, g, b)
    colors.append(color)

# Print so it can be pasted into Python source

sys.stdout.write("colors = [")
for color in colors:
    sys.stdout.write("{}".format(color))
    if color is not colors[-1]:
        sys.stdout.write(", \n")

sys.stdout.write("]")






















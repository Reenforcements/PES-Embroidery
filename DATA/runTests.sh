# Generate PES files for the four test shapes
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePath.pes -r -t 1.5 -m 20
python ../src/main.py -i "./TestInput/tree.svg" -o ./TestOutput/tree.pes -r -t 1.5 -m 20
python ../src/main.py -i "./TestInput/ugliestApple.svg" -o ./TestOutput/ugliestApple.pes -r -t 1.5 -m 20
python ../src/main.py -i "./TestInput/zigzag.svg" -o ./TestOutput/zigzag.pes -r -t 1.5 -m 20
# Generate PES files for different stitch widths
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePath_4_5.pes -r -t 4.5 -m 10
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePath_3_5.pes -r -t 3.5 -m 10
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePath_2_5.pes -r -t 2.5 -m 10
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePath_1_5.pes -r -t 1.5 -m 10

# Generate PES files for different minimum stitch distances
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePathD-20.pes -r -t 2.5 -m 20
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePathD-15.pes -r -t 2.5 -m 15
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePathD-10.pes -r -t 2.5 -m 10
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePathD-5.pes -r -t 2.5 -m 5

# Closest vs Zigzag stitch methods
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePathClosest.pes -r -s closest -m 20 -t 2.5
python ../src/main.py -i "./TestInput/simplePath.svg" -o ./TestOutput/simplePathZigzag.pes -r -s zigzag -m 20 -t 2.5



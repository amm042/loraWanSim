rm -f topo.csv
./topology.py 100 sunflower
./topology.py 5 random --show
cat topo.csv

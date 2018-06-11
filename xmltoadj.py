import sys
from gistfile1 import *

G = read_osm(sys.argv[1])
networkx.write_adjlist(G, sys.argv[2])

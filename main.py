import sys
import math
from Tkinter import *
from gistfile1 import *
 
#--------------------------------------------------------------------
# GLOBAL VARIABLES
window_width = 1366
window_height = 700
#--------------------------------------------------------------------
def main():
    f1 = file('map.osm', 'r');
    G = read_osm(f1)
    drawMapGraph(G)
    
    f1.close()
#--------------------------------------------------------------------
def writeNodesOnFile(G):
    file_nodes = open('map.nodes', 'w')
    for n_id in G.nodes():
        string_file = str(G.nodes[n_id]['data'].id) + " " + str(G.nodes[n_id]['data'].lat) + " " + str(G.nodes[n_id]['data'].lon) + "\n"
        file_nodes.write(string_file)
    file_nodes.close()

def writeAdjListOnFile(G):
    file_adjList = file('map.adjlist', 'w');
    networkx.write_adjlist(G, file_adjList)
    file_adjList.close()

#--------------------------------------------------------------------
def drawMapGraph(G):
    master = Tk()

    canvas_width = window_width
    canvas_height = window_height

    w = Canvas(master, width=canvas_width, height=canvas_height)
    w.pack()
    w.configure(background='#ffffff')

    for n_id in G.nodes():
        drawNode(w, G.nodes[n_id]['data'].lat, G.nodes[n_id]['data'].lon)
        drawWay(w, G) 
    mainloop()

def drawWay(w, G):      # G -> DiGRaph e w -> Canvas
    for n_node in G.nodes():
        adj = G.__getitem__(n_node)
        for n_adj in adj:
            (lat1, lon1) = adjustCanvasScale(G.nodes[n_node]['data'].lat, G.nodes[n_node]['data'].lon)
            (lat2, lon2) = adjustCanvasScale(G.nodes[n_adj]['data'].lat, G.nodes[n_adj]['data'].lon)
            if lon1 < lon2 and lat1 < lat2:
                w.create_line(lon1+1, lat1+1, lon2, lat2, fill='red')
            elif lon1 < lon2 and lat1 > lat2:
                w.create_line(lon1+1, lat1, lon2, lat2+1, fill='red')
            elif lon1 > lon2 and lat1 < lat2:
                w.create_line(lon1, lat1+1, lon2+1, lat2, fill='red')
            elif lon1 > lon2 and lat1 > lat2:
                w.create_line(lon1, lat1, lon2+1, lat2+1, fill='red')

def drawNode(w, lat_node, lon_node):
    (lat_node, lon_node) = adjustCanvasScale(lat_node, lon_node)
    w.create_rectangle(lon_node, lat_node, lon_node + 1, lat_node + 1, fill="#000000")

def adjustCanvasScale(lat, lon):
    # FALTA IMPLEMENTAR - PEGAR ESSES DADOS DO ARQUIVO OSM
    MAX_LAT = -28.9338700
    MIN_LAT = -28.9425700
    MAX_LON = -49.4748500
    MIN_LON = -49.4909900

    lat_canvas = lat - MIN_LAT
    lat_canvas = (- window_height / (MAX_LAT-MIN_LAT)) * lat_canvas + window_height

    lon_canvas = lon - MIN_LON
    lon_canvas = (window_width / (MAX_LON-MIN_LON)) * lon_canvas

    return (lat_canvas, lon_canvas)

# --------------------------------------------------

def nodesDistances(lat1, lon1, lat2, lon2):
    # Formula de haversine: calcula distancia entre nos
    # @@@@@@@@@@ TESTAR @@@@@@@@@@@@@@
    R = 6371e3      # Earth radius
    latRad1 = math.radians(lat1)
    latRad2 = math.radians(lat2)
    deltaLatRad = math.radians(lat2 - lat1)
    deltaLonRad = math.radians(lon2 - lon1)

    a = math.sin(deltaLatRad / 2) * math.sin(deltaLatRad / 2) + math.cos(latRad1) * math.cos(latRad2) * math.sin(deltaLonRad / 2) * math.sin(deltaLonRad / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));

    return R * c

def dijkstra(G, ini):    # ini -> no inicial
    # FALTA IMPLEMENTAR
    dist = []
    visited = []
    for i in G.nodes():
        dist[i] = -1
        visited[i] = False
    dist[ini] = 0
    pass
# --------------------------------------------------

if __name__ == "__main__":
    main()

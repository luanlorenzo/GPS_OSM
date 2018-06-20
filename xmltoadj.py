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
    f2 = file('mapAdj.adjlist', 'w');
    G = read_osm(f1)
    networkx.write_adjlist(G, f2)

    drawMapGraph(G)
    
    f1.close()
    f2.close()
#--------------------------------------------------------------------

def drawMapGraph(G):
    f = open('nodesMAP.nodes', 'w') 
    master = Tk()

    canvas_width = window_width
    canvas_height = window_height

    w = Canvas(master, width=canvas_width, height=canvas_height)
    w.pack()
    w.configure(background='#ffffff')

    for n_id in G.nodes():
        drawNode(w, G.nodes[n_id]['data'].lat, G.nodes[n_id]['data'].lon)

    drawWay(w, G)
    string_file = str(G.nodes[n_id]['data'].id) + " " + str(G.nodes[n_id]['data'].lat) + " " + str(G.nodes[n_id]['data'].lon) + "\n"
    f.write(string_file)  
    mainloop()

def drawWay(w, G):      # G -> DiGRaph e w -> Canvas
    # COMO CRIAR LINHA: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_line.html
    for n_node in G.nodes():
        adj = G.__getitem__(n_node)
        for n_adj in adj:
            (x1,y1) = adjustCanvasScale(G.nodes[n_node]['data'].lat, G.nodes[n_node]['data'].lon)
            (x2,y2) = adjustCanvasScale(G.nodes[n_adj]['data'].lat, G.nodes[n_adj]['data'].lon)
            w.create_line(x1, y1, x2, y2, fill='red')

def drawNode(w, lat_node, lon_node):
    (lat_node, lon_node) = adjustCanvasScale(lat_node, lon_node)
    w.create_rectangle(lon_node, lat_node, lon_node + 1, lat_node + 1, fill="#000000")

def adjustCanvasScale(lat, lon):
    # PENSAR EM ALGUM METODO PARA PEGAR ESSES DADOS AUTOMATICAMENTE
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
    dist = []
    visited = []
    for i in G.nodes():
        dist[i] = -1
        visited[i] = False
    dist[ini] = 0

# --------------------------------------------------

if __name__ == "__main__":
    main()
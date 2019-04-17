from math import *
from Tkinter import *
from gistfile1 import *
import heapq
 
window_width = 1366
window_height = 700

def main():
    f1 = file('map.osm', 'r')
    G = read_osm(f1)

    caminho = dijkstra(G, '1942003459', '1942008162')   # id of 2 nodes of the .osm file
    drawMapGraph(G, caminho)

    f1.close()

def writeNodesOnFile(G):
    file_nodes = open('map.nodes', 'w')
    for n_id in G.nodes():
        string_file = str(G.nodes[n_id]['data'].id) + " " + str(G.nodes[n_id]['data'].lat) + " " + str(G.nodes[n_id]['data'].lon) + "\n"
        file_nodes.write(string_file)
    file_nodes.close()

def writeAdjListOnFile(G):
    file_adjList = file('map.adjlist', 'w')
    networkx.write_adjlist(G, file_adjList)
    file_adjList.close()

def drawMapGraph(G, melhor_caminho):
    master = Tk()

    canvas_width = window_width
    canvas_height = window_height

    w = Canvas(master, width=canvas_width, height=canvas_height)
    w.pack()
    w.configure(background='#ffffff')

    for n_id in G.nodes():
        drawNode(w, G.nodes[n_id]['data'].lat, G.nodes[n_id]['data'].lon)
        drawWay(w, G)
    
    flag = 0
    prox_no = 0

    for i in melhor_caminho:
        if flag >= 1:
            no_atual = i
            (lat1, lon1) = adjustCanvasScale(G.nodes[prox_no]['data'].lat, G.nodes[prox_no]['data'].lon)
            (lat2, lon2) = adjustCanvasScale(G.nodes[no_atual]['data'].lat, G.nodes[no_atual]['data'].lon)
            w.create_line(lon1, lat1, lon2, lat2, fill='blue', width=5)
        prox_no = i
        flag = flag + 1 
    mainloop()

def drawWay(w, G):
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
    # missing implementation - uploading data altmatically from OSM file
    MAX_LAT = -28.9338700
    MIN_LAT = -28.9425700
    MAX_LON = -49.4748500
    MIN_LON = -49.4909900

    lat_canvas = lat - MIN_LAT
    lat_canvas = (- window_height / (MAX_LAT-MIN_LAT)) * lat_canvas + window_height

    lon_canvas = lon - MIN_LON
    lon_canvas = (window_width / (MAX_LON-MIN_LON)) * lon_canvas

    return (lat_canvas, lon_canvas)


def nodesDistances(lat1, lon1, lat2, lon2):
    """ Haversine's Formula: calculates distance between nodes """ 
    R = 6371e3      # Earth radius
    latRad1 = radians(lat1)
    latRad2 = radians(lat2)
    deltaLatRad = radians(lat2 - lat1)
    deltaLonRad = radians(lon2 - lon1)

    a = sin(deltaLatRad / 2) * sin(deltaLatRad / 2) + cos(latRad1) * cos(latRad2) * sin(deltaLonRad / 2) * sin(deltaLonRad / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    dist = R * c        # distance in m

    return dist/1000    # distance in km


class PriorityQueue(object):
    def __init__(self):
        self.__heapq = []

    def push(self, item, priority = 0):
        self.__heapq.append((priority, item))
        heapq.heapify(self.__heapq)

    def pop(self):
        return heapq.heappop(self.__heapq)[1]

    def empty(self):
        return len(self.__heapq) == 0

def reconstruct_path(came_from, start, end):
    current = end
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def dijkstra(G, start, end):
    pq = PriorityQueue()
    pq.push(start, priority=0)
    came_from = {}
    cost_so_far = {}
    cost_so_far[start] = 0
    came_from[start] = None

    while not pq.empty():
        current = pq.pop()

        if current == end:
            break

        for neighbor in G.neighbors(current):
            new_cost = cost_so_far[current] + float(nodesDistances(G.nodes[current]['data'].lat, G.nodes[current]['data'].lon, G.nodes[neighbor]['data'].lat, G.nodes[neighbor]['data'].lon))
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                pq.push(neighbor, priority = new_cost)
                came_from[neighbor] = current

    path = reconstruct_path(came_from, start, end)
    return path

# --------------------------------------------------
if __name__ == "__main__":
    main()

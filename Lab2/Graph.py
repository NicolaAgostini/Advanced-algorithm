from Node import Node
from Edge import Edge
from BinaryHeap import BinaryHeap
import sys

class Graph:
    def __init__(self):
        self.id_to_number = {}      #per ciascun id ritorna l'indice corrispondente
        self.nodes_number = 0       #numero dei nodi del grafo
        self.nodes_list = []    #lista dei nodi contenuti nel grafo
        self.edges_number = 0       #contatore degli archi
        self.number_to_id = {}    #associa il count all'id_stazione e al suo nome

    def returnIdToNumber(self):
        return self.id_to_number

    def returnNumberToId(self):
        return self.number_to_id

    def printG(self):   #stampa le informazioni principali del grafo
        print("Grafo con ", self.nodes_number, " nodi e ", self.edges_number, " archi.")

    def addNode(self, id_station, name_station, count):
        """
        :param id_station: id del nodo
        :param name_station: nome della stazione
        :param count: indice calcolato del nodo
        """
        id_station = int(id_station)        #converto in intero
        self.id_to_number[id_station] = count   #aggiungo al dizionario il count con indice id_station
        self.nodes_number += 1          #incremento il numero dei nodi del grafo
        self.nodes_list.append(Node(id_station))        #aggiungo alla lista dei nodi il nodo id_station
        self.number_to_id[count] = id_station       #aggiungo al dizionario l'id_station con indice count

    def addEdge(self, edge):
        """
        :param edge: arco
        """
        self.edges_number += 1      #incremento il numero di archi del grafo
        i = self.id_to_number[edge.id_departure_station]        #assegno ad i l'indice del nodo da cui parte l'arco
        self.nodes_list[i].addEdgeToNode(edge)      #aggiungo al nodo l'arco

    def relax(self, u, v, previous_nodes, distances, edge, timetables, run_id_list, line_id_list, time_departures):  # u e v sono indici dei nodi da rilassare
        """
        :param u: indice del nodo/stazione da rilassare
        :param v: indice del nodo/stazione da rilassare
        :param previous_nodes: nodi già trattati
        :param distances: valori delle distanze dalla sorgente
        :param edge: arco da rilassare
        :param timetables: lista degli orari di arrivo in una certa stazione
        :param run_id_list: lista delle corse
        :param line_id_list: lista delle linee
        :param time_departures: orario di partenza dal nodo
        """
        timetables[v] = edge.arrival_time       #aggiungo l'orario di arrivo alla lista in indice v
        distances[v] = distances[u] + (self.attendanceTime(timetables[u], edge.departure_time) +
                                       (self.time(edge.arrival_time) - self.time(edge.departure_time)))     #aggiorno la distanza del nodo v
        run_id_list[v] = edge.run_id    #aggiungo l'id della corsa alla lista
        line_id_list[v] = edge.id_line      #aggiungo l'id della linea alla lista
        previous_nodes[v] = u       #aggiorno il predecessore del nodo v
        time_departures[v] = edge.departure_time    #aggiorno l'orario di partenza del nodo v
        return distances, previous_nodes, timetables, run_id_list, line_id_list, time_departures

    def dijkstra(self, id_start_node, min_departure_time):
        """
        :param id_start_node: stazione di partenza
        :param min_departure_time: orario minimo in cui si è disposti a partire
        """
        distances = []      #array delle distanze dal nodo sorgente
        heap = BinaryHeap()     #inizializzo una heap binaria
        previous_nodes = []     #inizializzo la lista dei nodi già visitati
        timetables = []         #inizializzo la lista degli orari di arrivo per ciascun nodo
        time_departures = []    #inizializzo la lista degli orari di partenza per ciascun nodo

        run_id_list = []        #inizializzo la lista delle corse per ciascun nodo
        line_id_list = []       #inizializzo la lista delle linee per ciascun nodo

        for i, x in enumerate(self.nodes_list):
            distances.append(sys.maxsize)       #inizializzo diversi valori
            previous_nodes.append(-1)
            timetables.append("-1")
            run_id_list.append("-1")
            line_id_list.append("-1")
            time_departures.append("-1")
            heap.add(x.id, distances[self.id_to_number[x.id]])  #aggiungo alla heap l'id della stazione e la distanza fra il nodo e la sorgente
        distances[self.id_to_number[id_start_node]] = 0     #pongo a 0 la distanza fra lo start_node e la sorgente
        timetables[self.id_to_number[id_start_node]] = min_departure_time       #aggiorno l'orario di arrivo nel nodo sorgente al minimo orario di partenza
        heap.decreaseKey(id_start_node, 0)       #decremento il valore della heap ad indice idToNumber[startNodeId] a 0 in modo da essere la sorgente
        while len(heap.list_vertices) > 0:      #finchè la heap non è vuota
            u = heap.extractMin()       #estraggo il minimo
            if timetables[self.id_to_number[u.id]] != "-1":
                for edge in self.nodes_list[self.id_to_number[u.id]].adj_arr:
                    # poichè la partenza da una stazione deve essere dopo l'orario di arrivo nella stazione precedente
                    if distances[self.id_to_number[u.id]] + (self.attendanceTime(timetables[self.id_to_number[u.id]], edge.departure_time) + (self.time(edge.arrival_time) - self.time(edge.departure_time))) < distances[self.id_to_number[edge.id_arrival_station]]:

                        distances, previous_nodes, timetables, run_id_list, line_id_list, time_departures = self.relax(self.id_to_number[u.id], self.id_to_number[edge.id_arrival_station], previous_nodes, distances, edge, timetables, run_id_list, line_id_list, time_departures)
                        heap.decreaseKey(edge.id_arrival_station, distances[self.id_to_number[edge.id_arrival_station]])

        return distances, previous_nodes, timetables, run_id_list, line_id_list, time_departures

    def extractTime(self, time):    #ritorno l'orario diviso in ore e minuti
        return time[0:2], time[2:]

    def attendanceTime(self, arriving_time, departure_time):     #ritorna il tempo di attesa fra l'orario di arrivo nella stazione e l'orario di partenza della corsa
        arriving_hours, arriving_minutes = self.extractTime(arriving_time[1:])      #elimino il primo carattere dagli orari e li divido in ore e minuti
        departure_hours, departure_minutes = self.extractTime(departure_time[1:])

        arriving_time_minutes = int(arriving_hours) * 60 + int(arriving_minutes)        #trasformo gli orari in minuti
        departure_time_minutes = int(departure_hours) * 60 + int(departure_minutes)

        if arriving_time_minutes >= 24 * 60:        #se sforo le 24 ore
            arriving_time_minutes = abs(24 * 60 - arriving_time_minutes)    #ricalcolo l'orario di arrivo

        if departure_time_minutes >= 24 * 60:       #se sforo le 24 ore
            departure_time_minutes = abs(24 * 60 - departure_time_minutes)      #ricalcolo l'orario di partenza

        if departure_time_minutes - arriving_time_minutes >= 0:     #se l'orario di partenza è maggiore o uguale dell'orario di arrivo
            return departure_time_minutes - arriving_time_minutes
        else:
            return 24*60 + departure_time_minutes - arriving_time_minutes


    def time(self, string):     #ritorna l'orario in minuti
        hours, minutes = self.extractTime(string[1:])
        return int(hours) * 60 + int(minutes)

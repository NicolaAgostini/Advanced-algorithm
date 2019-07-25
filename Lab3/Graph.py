import math
import numpy as np
import sys
import copy
import time
from Tree import Tree
from Node import Node
from Edge import Edge
sys.setrecursionlimit(10000)


class Graph:
    def __init__(self, name, dimension, coord_type, coordinates):
        """
        :param name: nome del grafo che si sta analizzando
        :param dimension: numero dei nodi del grafo
        :param coord_type: tipo di coordinate utilizzate
        :param coordinates: lista di tutte le coordinate
        """
        self.name = name
        self.num_nodes = int(dimension)
        self.coord_type = coord_type
        self.coordinates = coordinates
        self.num_edges = 0          # numero di archi del grafo
        self.matr_adj = np.zeros(shape=(self.num_nodes, self.num_nodes))        # matrice delle adiacenze del grafo

        # aggiungo tutti gli archi al grafo in modo da creare un grafo completo
        for i in range(self.num_nodes-1):       # scorro solo la matrice triangolare superiore essendo gli archi non orientati
            for j in range(i+1, self.num_nodes):
                self.num_edges += 1     # aumento il numero di archi
                self.matr_adj[i][j] = self.calculateWeight(self.coordinates[i], self.coordinates[j])
                self.matr_adj[j][i] = self.matr_adj[i][j]

    def printG(self):
        print("Il grafo", self.name, "ha ", self.num_nodes, "nodi e ", self.num_edges, "archi")
        print(self.matr_adj)

    def calculateWeight(self, coordinates1, coordinates2):
        """
        :param coordinates1: prima coppia di coordinate
        :param coordinates2: seconda coppia di coordinate
        :return: il peso dell'arco fra le due coppie di coordinate
        """
        if self.coord_type != "GEO\n":  # se sono coordinate euclidee
            x = abs(coordinates1[0] - coordinates2[0])
            y = abs(coordinates1[1] - coordinates2[1])
            return round((x**2 + y**2)**0.5)
        else:                           # se sono coordinate geografiche
            RRR = 6378.388

            q1 = math.cos(coordinates1[1] - coordinates2[1])
            q2 = math.cos(coordinates1[0] - coordinates2[0])
            q3 = math.cos(coordinates1[0] + coordinates2[0])
            return int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

    def hkVisit(self, v, subset_nodes, distances, start_time, stop):
        """
        :param v: nodo destinazione
        :param subset_nodes: sottoinsieme di nodi in cui viene calcolato il peso del cammino minimo
        :param distances: struttura dati che rappresenta la migliore distanza trovata fino a quel nodo passando per tutti i vertici di quel preciso subset
        :param start_time: tempo di inizio
        :param stop: tempo di fine del timer
        :return: peso del cammino minimo da 0 a v che visita tutti i vertici in subset_nodes
        """
        g = tuple(subset_nodes) # creo la tupla immutabile che rappresenta il subset corrente

        if len(subset_nodes) == 1 and subset_nodes[0] == v:  # caso base: se il subset contiene solo il nodo corrente da visitare v
            return self.matr_adj[0][v], distances, stop

        elif (v, g) in distances:  # caso base: se esiste già il subset g associato al nodo v
            return distances[v, g], distances, stop
        else:
            min_dist = sys.maxsize
            subset = copy.deepcopy(subset_nodes)  # effettuo una copia profonda del subset per poi eliminarci il nodo v senza avere side effect su subset nodes
            subset.remove(v)
            for vertex in subset_nodes:  # per ogni vertice nel subset
                if stop:  # se è scaduto il tempo
                    break

                if vertex != v:  # per tutti i vertici tranne quello appena rimosso
                    dist, distances, stop = self.hkVisit(vertex, subset, distances, start_time, stop)  # chiamata ricorsiva
                    if dist + self.matr_adj[vertex][v] < min_dist:  # se la distanza trovata più l'arco considerato è minore della distanza trovata fin'ora (al più infinita)
                        min_dist = dist + self.matr_adj[vertex][v]  # aggiorna la minima distanza

            if time.time() - start_time > 20*60:  # se scade il countdown allora ritorno
                stop = True
                return min_dist, distances, stop

            distances.update({(v, g): min_dist})  # aggiorno la struttura dati distances con il vertice v e il subset corrente con la minima distanza trovata fin'ora
            return min_dist, distances, stop

    def hkTsp(self, start_time):
        """
        :param start_time: tempo di avvio della funzione, serve per capire quando fermarmi
        :return: la minima distanza esatta oppure se termina il tempo a disposizione la migliore distanza trovata fin'ora
        """
        distances = {}  # creo la struttura dati delle distanze
        vertices = [x for x in range(self.num_nodes)]  # inizializzo l'array che contiene gli id dei vertici di tutti i nodi del grafo
        return self.hkVisit(0, vertices, distances, start_time, False)

    def nearestNeighbor(self):
        """
        :return: ritorna la distanza del circuito secondo l'euristica nearest neighbor
        """
        circuit = []        # inizializzo il circuito vuoto
        total_circuit_length = 0        # inizializzo la lunghezza del circuito a 0
        visited_nodes = [False for x in range(self.num_nodes)]  # inizializzo un array che per ciascun nodo tiene traccia se è stato aggiunto al circuito o no
        circuit.append(0)       # aggiungo il nodo iniziale al circuito
        visited_nodes[0] = True             # ho aggiunto il nodo iniziale al circuito

        for i in range(1, self.num_nodes):  # per ogni altro nodo
            min_dist = sys.maxsize
            choosen_index = -1          # inizializzo l'indice del nodo scelto

            for index, val in enumerate(self.matr_adj[circuit[-1]]):    # scelgo il nodo che ha minima distanza
                if val < min_dist and not visited_nodes[index]:
                    min_dist = val                  # salvo il peso dell'arco
                    choosen_index = index               # salvo l'indice del nodo

            circuit.append(choosen_index)       # aggiungo il nuovo nodo al circuito
            visited_nodes[choosen_index] = True
            total_circuit_length += min_dist    # aggiorno il valore della lunghezza del circuito

        total_circuit_length += self.matr_adj[0][circuit[-1]]       # aggiungo la distanza fra l'ultimo nodo trovato e il nodo sorgente
        circuit.append(0)               # aggiungo il nodo iniziale anche alla fine del circuito in modo da creare un vero e proprio circuito
        return total_circuit_length

    def createArraysOfEdges(self):
        """
        :return res: un array di due dimensioni in cui ciascuna riga è una tupla di 3 valori ordinata secondo il peso minore
                 del tipo: (peso, indice i, indice j)
        """
        res = [(self.matr_adj[i][j], i, j)
               for i in range(self.num_nodes - 1)
               for j in range(i+1, self.num_nodes)]  # creo una lista di oggetti in cui il primo campo di ogni oggetto è il peso dell'arco, il secondo è in nodo di partenza dell'arco e il terzo è il nodo di arrivo dell'arco

        res = sorted(res, key=lambda t: t[0])  # ordino la lista in base al primo campo di ogni oggetto
        return res

    def Tsp2_approx(self):
        """
        :return: la distanza secondo tsp 2-approssimato
        """
        graphMST = self.kruskalMST()
        already_inserted = [False for x in range(self.num_nodes)]  # struttura dati che serve per la ricerca in profondità per non visitare nuovamente nodi già visitati
        dictionary = {}
        counter = 0
        start_node = graphMST[0]
        counter, graph_enumeration = self.deptFirstSearch(graphMST, counter, dictionary, start_node, already_inserted)  # ricerca in profondità
        graph_enumeration[counter] = graphMST[0].id  # completo il ciclo sapendo che l'ultimo nodo viene collegato con il primo
        dist = self.calculate_distance_MST(graph_enumeration)  # calcola la distanza secondo tsp 2-approssimato
        return dist

    def kruskalMST(self):
        """
        :return: il minimum spanning tree, cioè l'albero di copertura minimo del grafo in questione
        """
        couples = []    # array di nodi
        for i in range(self.num_nodes):
            couples.append(Node(i))     # aggiunge n nodi a couples
        set_tree = Tree(self.num_nodes)     # aggiunge n nodi all'albero
        for i in range(self.num_nodes):
            set_tree.makeSet(i)         #crea n insiemi disgiunti
        edges = self.createArraysOfEdges()  # ordina gli archi in peso crescente
        for val in edges:       # per ogni arco ordinato secondo peso crescente
            if set_tree.findSet(val[1]) != set_tree.findSet(val[2]):    # se i nodi non fanno parte dello stesso albero
                couples[val[1]].addEdgeToNode(Edge(val[1], val[2], val[0]))     # aggiungo un arco fra il primo ed il secondo nodo
                couples[val[2]].addEdgeToNode(Edge(val[2], val[1], val[0]))     # aggiungo un arco fra il secondo ed il primo nodo
                set_tree.union(val[1], val[2])              # faccio l'unione degli alberi

        return couples

    def deptFirstSearch(self, couples, counter, dictionary, start_node, already_inserted):
        """
        :param couples: array di nodi con la lista di adiacenza per ciascun nodo
        :param counter: contatore per la numerazione dei nodi
        :param dictionary: dizionario che associa la numerazione dei nodi all'id del nodo nel grafo originale(self)
        :param start_node: nodo di partenza
        :return dictionary: dizionario finale
        """
        dictionary[counter] = start_node.id
        already_inserted[start_node.id] = True
        counter += 1
        for edge in start_node.adj_arr:
            if not already_inserted[edge.arrival_node]:
                counter, dictionary = self.deptFirstSearch(couples, counter, dictionary, couples[edge.arrival_node],
                                                           already_inserted)

        return counter, dictionary

    def calculate_distance_MST(self, graph_enumeration):
        """
        :param graph_enumeration: dizionario che associa la numerazione all'id del nodo
        :return: la distanza rispetto alla numerazione di graph_enumeration
        """
        dist = 0
        for i in range(self.num_nodes):
            dist += self.matr_adj[graph_enumeration[i]][graph_enumeration[i+1]]
        return dist















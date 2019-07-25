import codecs
from Graph import Graph
import math
import time


def main():
    path_info_array = ["./Files/burma14.tsp", "./Files/d493.tsp", "./Files/dsj1000.tsp", "./Files/eil51.tsp",
                       "./Files/gr229.tsp", "./Files/kroD100.tsp", "./Files/ulysses22.tsp"]
    graph_list = []
    #path_info = ["./Files/burma14.tsp"]

    for i in range(len(path_info_array)):       # per ciascun file
        name = ""       # nome del grafo
        dimension = -1      # numero dei nodi
        coord_type = ""     # tipo di coordinate
        coordinates = []    # lista di tuple della forma (coordinataX, coordinataY)
        next_are_coords = False     # se è True significa che sto parsando le coordinate
        line = ""       # inizializzazione della linea che verrà utilizzata per scorrere il file

        with codecs.open(path_info_array[i]) as f:    # apertura dei file
            line = f.readline()         # lettura della prima riga
            while line != "EOF\n":      # finchè non vi è EOF
                if not next_are_coords:     # se la linea è riferita all'intestazione del file

                    a = line.split(":")     # divido la linea rispetto al carattere :
                    if a[0] == "NAME" or a[0] == "NAME ":
                        name = a[1].replace(" ", "")[:-1]   # salvo il nome del grafo

                    if a[0] == "DIMENSION" or a[0] == "DIMENSION ":
                        dimension = int(a[1].replace(" ", ""))     # salvo la dimensione dei nodi del grafo

                    if a[0] == "EDGE_WEIGHT_TYPE" or a[0] == "EDGE_WEIGHT_TYPE ":
                        coord_type = a[1].replace(" ", "")   # salvo il tipo di coordinate

                    if a[0] == "NODE_COORD_SECTION\n":
                        next_are_coords = True      # le prossime righe del file saranno coordinate

                else:
                    a = line.split(" ")     # divido la linea rispetto agli spazi
                    a = [i for i in a if i != ""]
                    if coord_type == "EUC_2D\n":      # se sono euclidee
                        coordinates.append((float(a[1]), float(a[2][:-1])))      # float gestisce la codifica numerica esponenziale

                    else:
                        deg = int(float(a[1]))      # tronca all'intero
                        min = float(a[1]) - deg
                        rad_x= math.pi * (deg + 5.0 * min / 3.0) / 180.0    # calcolo coordinata x

                        deg = int(float(a[2][:-1]))
                        min = float(a[2][:-1]) - deg
                        rad_y = math.pi * (deg + 5.0 * min / 3.0) / 180.0    # calcolo coordinata y

                        coordinates.append((rad_x, rad_y))    # aggiungo le coordinate alla lista

                line = f.readline()     # leggo la linea successiva
        graph_list.append(Graph(name, dimension, coord_type, coordinates))          # aggiungo alla lista di grafi il grafo creato

    for graph in graph_list:        # per ciascun grafo
        print(graph.name)
        start_time = time.time()        # faccio partire il timer
        min_dist, distances, stop = graph.hkTsp(start_time)   # eseguo Held-Karp
        print("Minima distanza algoritmo esatto = ", min_dist)      # stampo il cammino minimo trovato
        print("tempo algoritmo esatto =", time.time() - start_time)     # stampo il tempo impiegato

        start_time = time.time()        # faccio partire il timer
        min_dist = graph.nearestNeighbor()         # eseguo l'euristica Nearest Neighbor
        print("Minima distanza euristica Nearest Neighbor = ", min_dist)    # stampo il cammino minimo trovato
        print("tempo Nearest Neighbor =", time.time() - start_time)     # stampo il tempo impiegato

        start_time = time.time()        # faccio partire il timer
        dist = graph.Tsp2_approx()       # eseguo l'euristica 2-approssimata
        print("Minima distanza 2 approssimata = ", dist)    # stampo il cammino minimo trovato
        print("tempo euristica 2-approssimata = ", time.time() - start_time)    # stampo il tempo impiegato


if __name__ == '__main__':
    main()

import fileinput
import glob
import errno
import codecs
import sys
from Graph import Graph
from Node import Node
from Edge import Edge
import matplotlib.pyplot as plt

def main():
    # sys.setrecursionlimit(sys.maxsize)
    path_info = "./Files/Info/"
    file_stations = path_info + "bahnhof"       # percorso in cui vi è il file delle stazioni

    id_station = 0          # inizializzazione dell'id e del nome della stazione
    name_station = ""
    graph = Graph()         # creazione del grafo
    with codecs.open(file_stations, encoding='cp1250') as f:    # apertura del file delle stazioni
        f.readline()            # salto la prima riga
        line = f.readline()
        count = 0               # contatore delle stazioni
        while line:    # finchè il file non finisce;
            id_station = line[0:9]      # trovo l'id della stazione
            name_station = line[14:34]  # trovo il nome della stazione
            graph.addNode(id_station, name_station, count)      # aggiungo la stazione al grafo
            line = f.readline()     # passo alla linea successiva
            count += 1              # incremento il contatore delle stazioni che corrisponderà ad un nuovo id

    file_coordinates = path_info + "bfkoord"        # percorso in cui sono descritte le coordinate delle stazioni
    with codecs.open(file_coordinates, encoding='cp1250') as f:     # apertura del file delle coordinate
        f.readline()        # salto le prime 2 righe
        f.readline()
        line = f.readline()     # mi salvo il contenuto della terza linea
        count = 0           # contatore che mi serve per aggiungere le coordinate ai nodi corretti
        while line:         # itero finchè il file non finisce
            id_station = line[0:9]
            latitude = line[12:20]
            longitude = line[22:31]
            graph.nodes_list[count].setCoordinates(float(latitude), float(longitude))   # aggiungo le coordinate al nodo con indice count
            count += 1          # incremento il count per il nodo successivo
            line = f.readline()     # leggo la prossima riga del file

    # for i in graph.nodes_list:     # stampo le coordinate di tutte le stazioni
    #     print(i.id, i.posX, i.posY)



    path_lines = "./Files/Linee/*.LIN"      # mi posiziono sulle linee

    files = glob.glob(path_lines)
    i = 0       # contatore dei files

    for name in files:      # per ciascun file presente nella cartella Linee
        i += 1
        with codecs.open(name, encoding='cp1250') as f:    # FONDAMENTALE la codifica del file
            line = f.readline()     # leggo la prima riga
            run_id = ""     # inizializzo l'id della corsa
            line_id = ""    # inizializzo l'id della linea
            j = 0           # alla prima fermata sarà a 0, poi sarà un contatore
            arrival_time = []       # lista che conterrà tutti gli orari di arrivo in una determinata stazione
            departure_time = []     # lista che conterrà tutti gli orari di partenza da una determinata stazione
            name_station = []       # lista dei nomi di tutte le stazioni
            id_station = []         # lista degli id delle stazioni

            restart = False         # mi serve per capire se creare un arco oppure no

            while line:        # finchè non finisce il file
                if line.startswith("*"):
                    restart = True
                    if line.startswith("*Z"):       # identifica le righe che danno informazioni sulla corsa
                        run_id = line[3:8]        # utile per l'edge
                        line_id = line[9:15]

                else:        # se è una riga che contiene informazioni riguardo alle fermate
                    id_station.append(line[0:9])          # inserisco l'id
                    name_station.append(line[10:30])      # inserisco il nome

                    if not (line[32:].startswith(" ") and line[32:].startswith("-")):   # se è una tratta intermedia della linea
                        arrival_time.append(line[32:37])        # aggiungo l'orario di arrivo a quella fermata

                    departure_time.append(line[39:44])      # aggiungo l'orario di partenza da quella fermata

                    if restart:
                        restart = False
                    elif int(j) >= 1:       # se ho almeno due fermate di una linea posso creare un arco
                        edge = Edge(departure_time[j-1], arrival_time[j], run_id, line_id, int(id_station[j-1]), int(id_station[j]))
                        graph.addEdge(edge)     # aggiungo l'arco al grafo


                    j += 1    #  incremento j

                line = f.readline()     # leggo la prossima riga

    graph.printG()      # stampo le caratteristiche del grafo
    distances = []          # conterrà le distanze di ciascun nodo dalla sorgente e -1 se il nodo è la sorgente stessa
    previous_nodes = []     # conterrà le stazioni visitate per raggiungere il nodo destinazione
    run_id_list = []        # conterrà la lista di tutte le corse
    time_departures = []    # conterrà la lista di tutti gli orari di partenza
    line_id_list = []       # conterrà la lista di tutte le linee
    '''
    for nodo in graph.nodes_list:
        print("Nodo: ", nodo.id)
        for arco in nodo.adj_arr:
            print("arco da ", arco.id_departure_station, " a ", arco.id_arrival_station, "\tOrario partenza: ",
                  arco.departure_time, "\tOrario Arrivo: ", arco.arrival_time)
    '''
    # array = [(500000079, 300000044, "01300")]      # corsa di prova
    # array = [(200415016, 200405005, "00930")]
    # array = [(300000032, 400000122, "00530")]
    # array = [(210602003, 300000030, "00630")]
    # array = [(200417051, 140701016, "01200")]
    #array = [(200417051, 140701016, "02355")]
    #array = [(120904001, 120103002, "01055")]
    array = [(150303001, 130107002, "00755")]
    #array = [(300000032, 150104001, "00320")]


    print("Viaggio da", array[0][0], "a", array[0][1])
    for dep_node, arr_node, time_dep in array:

        distances, previous_nodes, timetables, run_id_list, line_id_list, time_departures = graph.dijkstra(dep_node, time_dep)      # calcolo dijkstra sul grafo
        id_to_number = graph.returnIdToNumber()     # ricavo la mappa fra gli id dei nodi e il contatore associato
        number_to_id = graph.returnNumberToId()     # ricavo la mappa fra il contatore e l'id corrispondente

        # print(distances[id_to_number[arr_node]])   # numero di minuti trascorsi fra la partenza e l'arrivo

        previous_path = []
        previous_path = rebuildPreviousNodes(previous_nodes, id_to_number[arr_node], id_to_number, previous_path, dep_node)     # ricostruisco il cammino eseguito per arrivare al nodo destinazione
        print("Ora di partenza:", timetables[id_to_number[dep_node]][1:3]+":"+timetables[id_to_number[dep_node]][3:])   # adatto l'orario di partenza in forma ore:minuti
        print("Ora di arrivo:", timetables[id_to_number[arr_node]][1:3]+":"+timetables[id_to_number[arr_node]][3:])     # adatto l'orario di arrivo in forma ore:minuti
        j = previous_path[-1]       # nodo sorgente

        id_repeated_dep = ""        # inizializzo id e orario delle corse
        time_repeated_dep = ""
        same_run = False        # boolean che mi serve per capire se il prossimo arco fra due nodi ha lo stesso id del nodo precedente
        previous_path = previous_path[::-1]     # ribalto la lista in modo da avere il percorso in ordine
        num_time = 0            # mi serve per controllare che onlyOneLine non venga chiamata più di una volta
        for i, val in enumerate(previous_path):     # per ciascuna stazione presente
            if i == 0:      # se è la sorgente
                pass
            else:
                if num_time == 1:       # TODO Verificare, probabilmente si può togliere
                    break
                else:
                    # 1 caso: la corsa corrente e la precedente hanno id diverso e non siamo alla fine di archi con lo stesso id della corsa
                    if run_id_list[val] != run_id_list[previous_path[i-1]] and not same_run:
                        if not onlyOneLine(previous_path[i:], run_id_list, num_time):       # se il percorso si articola attraverso più di una linea
                            print(time_departures[val][1:3] + ":" + time_departures[val][3:] +": corsa", run_id_list[val], " ",
                                    line_id_list[val], "da", number_to_id[j], "a", number_to_id[val])
                            j = val     # salvo la stazione in cui è arrivato


                    # 2 caso: la corsa successiva è sulla stessa linea e la precedente è su un'altra corsa
                    if run_id_list[val] == run_id_list[previous_path[i-1]] and not same_run:
                            same_run = True
                            id_repeated_dep = number_to_id[j]           # salvo l'id della stazione
                            time_repeated_dep = time_departures[val]    # salvo l'orario di partenza da quella stazione
                            j = val

                    # Se tutte le prossime stazioni del percorso hanno lo stesso id della corsa
                    if onlyOneLine(previous_path[i:], run_id_list, num_time):

                        if same_run:        # se sono entrato nel caso 2
                            print(time_departures[val][1:3] + ":" + time_departures[val][3:] + ": corsa",
                                  run_id_list[val], " ",
                                  line_id_list[val], "da", id_repeated_dep, "a", number_to_id[previous_path[-1]])
                        else:
                            print(time_departures[val][1:3] + ":" + time_departures[val][3:] + ": corsa",
                                  run_id_list[val], " ",
                                  line_id_list[val], "da", number_to_id[j], "a", number_to_id[previous_path[-1]])
                        num_time += 1       # faccio in modo che non venga più chiamata la funzione onlyOneLine
                        break       # fine del percorso

                    #  3 caso: la corsa successiva non è sulla stessa linea e le precedenti lo erano
                    if run_id_list[val] != run_id_list[previous_path[i-1]] and same_run:
                        same_run = False
                        print(time_repeated_dep[1:3] + ":" + time_repeated_dep[3:] + ": corsa", run_id_list[val],
                                  " ", line_id_list[val], "da", id_repeated_dep, "a", number_to_id[val])
                        j = val

    # for i in previous_path:
    #     print(run_id_list[i])

    plotPath(previous_path, graph)      # plot del grafo

def rebuildPreviousNodes(previous_nodes, node, id_to_number, previous_path, start_node):
    """
    :param previous_nodes: array ritornato dall'algoritmo di Dijkstra
    :param node: nodo destinazione
    :param id_to_number: dizionario originale che associa gli id delle stazioni agli id dei nodi
    :param previous_path: array del cammino minimo
    :param start_node: id del nodo di partenza
    :return previous_path: array del cammino minimo
    """
    if node == id_to_number[start_node]:    # se il nodo corrente è l'ultimo
        previous_path.append(node)      # aggiungo l'ultimo nodo alla lista
        return previous_path
    else:
        previous_path.append(node)      # aggiungo il nodo corrente alla lista
        return rebuildPreviousNodes(previous_nodes, previous_nodes[node], id_to_number, previous_path, start_node)      # chiamata ricorsiva


def plotPath(previous_path, graph):
    """
    :param previous_path: lista dei nodi composto dal percorso: nodo sorgente --> nodo destinazione
    :param graph: il grafo costruito dai file
    """
    latitude = []       # lista delle latitudini
    longitude = []      # lista delle longitudini
    for i in graph.nodes_list:      # per ogni nodo del grafo
        if i.posX != 0 and i.posY != 0:     # se il nodo ha valori di latitudine e longitudine
            latitude.append(i.posX/6)       # normalizzo i valori
            longitude.append(i.posY/49.5)   # normalizzo i valori
    plt.scatter(latitude, longitude, marker='.', c='r', s=0.5)      # stampo nel grafo le posizioni dei nodi
    j = previous_path[-1]       # salvo il valore del nodo sorgente

    for i, val in enumerate(reversed(previous_path)):       # per ciascun nodo presente nel cammino sorgente --> destinazione
        if i != j:
            x1, y1 = graph.nodes_list[val].posX/6, graph.nodes_list[val].posY/49.5
            x2, y2 = graph.nodes_list[j].posX/6, graph.nodes_list[j].posY/49.5
            plt.xticks([x1, x2], "")        # tolgo le etichette agli assi
            plt.yticks([y1, y2], "")
            plt.plot([x1, x2], [y1, y2], 'go-')     # stampo il grafo
            j = val     # aggiorno il valore di j
    plt.show()      # mostro il grafo


def onlyOneLine(previous_path, run_id_list, num_time):
    """
    :param previous_path: nodi ancora da valutare nel percorso sorgente --> destinazione
    :param run_id_list: lista delle corse per ciascun nodo
    :param num_time: numero di volte che è chiamata questa funzione
    :return: True se tutti i nodi in previous_path hanno la stessa run_id
    """
    if num_time > 0:    # SOLO se è la prima volta che viene chiamata potrà ritornare True
        return False
    run_id = 0       # dichiaro la variabile
    for i, value in enumerate(previous_path):
        if i == 0:      # salvo il primo valore di run_id_list
            run_id = run_id_list[value]
        else:
            if run_id != run_id_list[value]:    # controllo che tutti i valori siano uguali a run_id
                return False
    return True


if __name__ == '__main__':
        main()

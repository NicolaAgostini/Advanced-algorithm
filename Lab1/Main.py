from Graph import *
import sys
import copy

def main():
    numNodes = 6474     #numero di nodi del grafo
    numEdges = 12572    #numero di archi del grafo

    sys.setrecursionlimit(10000)    #settaggio del limite superiore di chiamate ricorsive possibili da un algoritmo
    seed = 1        #parametro per la generazione dei numeri casuali
    p = 0.0006      #probabilità utilizzata nella generazione del grafo ER
    m = int(round(numEdges / numNodes))     #grado medio del grafo

    print("ER Graph:")
    graph_er = ERGraph(numNodes, p, seed)       #creazione del grafo tramite l'algoritmo ER
    graph_er.printG()       #stampa del grafo
    graph_er_copy = copy.deepcopy(graph_er)     #creazione di una copia del grafo
    arrResilienceEr = graph_er_copy.resilienceCalculator(seed)      #calcolo della resilienza in seguito ad un attacco casuale
   
    intSelResilienceEr = graph_er.intelligentSelectionResilienceCalculator()    #calcolo della resilienza in seguito ad un attacco con strategia migliorata
    

    print("UPA Graph:")
    graph_UPA = UPAGraph(numNodes, m)   #creazione del grafo tramite l'algoritmo UPA
    graph_UPA.printG()  #stampa del grafo
    graph_UPA_copy = copy.deepcopy(graph_UPA)   #creazione di una copia del grafo
    arrResilienceUPA = graph_UPA_copy.resilienceCalculator(seed)    #calcolo della resilienza in seguito ad un attacco casuale
    
    intSelResilienceUPA = graph_UPA.intelligentSelectionResilienceCalculator()  #calcolo della resilienza in seguito ad un attacco con strategia migliorata
    


    print("DataGraph:")
    data_graph = DATAGraph(numNodes, './as20000102.txt')    #creazione del grafo tramite il file di testo
    data_graph.printG()     #stampa del grafo
    data_graph_copy = copy.deepcopy(data_graph)     #creazione di una copia del grafo
    arrResilienceDATA = data_graph_copy.resilienceCalculator(seed)      #calcolo della resilienza in seguito ad un attacco casuale
    
    intSelResilienceDATA = data_graph.intelligentSelectionResilienceCalculator()    #calcolo della resilienza in seguito ad un attacco casuale con strategia migliorata
    

    # DOMANDA 1
    printPlotRandom(arrResilienceDATA,
                    arrResilienceEr,
                    arrResilienceUPA,
                    numNodes,
                    "Fig1_resilienze_attacchi_casuali")

    # DOMANDA 2
    printPlotRandom_masked(arrResilienceDATA,
                           arrResilienceEr,
                           arrResilienceUPA,
                           numNodes,
                           "Fig2_resilienze_attacchi_casuali_masked")

    # DOMANDA 3
    printPlotRandom(intSelResilienceDATA,
                    intSelResilienceEr,
                    intSelResilienceUPA,
                    numNodes,
                    "Fig3_resilienze_attacchi_intelligenti")

    # DOMANDA 4
    printPlotRandom_masked(intSelResilienceDATA,
                           intSelResilienceEr,
                           intSelResilienceUPA,
                           numNodes,
                           "Fig4_resilienze_attacchi_intelligenti_masked")


if __name__ == '__main__':
        main()

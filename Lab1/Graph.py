from Node import *
import random as random
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import pylab as pylab


class Color(Enum):      #enumerazione per il colore dei nodi
    White = int(0)
    Gray = int(1)
    Black = int(2)


class Graph:
    def __init__(self, n):
        """
        :param n: numero di nodi del grafo
        """
        self.numNodes = n
        self.arrNodes = []  #lista di nodi contenuti nel grafo
        for i in range(n):
            self.arrNodes.append(Node(i))   #aggiungo l'iesimo nodo in modo da averli ordinati
        self.numEdges = 0       #contatore degli archi

    def printG(self):   #stampa le informazioni principali del grafo
        print("Grafo con ", self.numNodes, " nodi e ", self.numEdges, " archi.")

    def DFS_Visited(self, u, visited, idToColor):
        """
        :param u: indice del nodo da visitare
        :param visited: lista dei nodi visitati
        :param idToColor: array che gestisce i colori dei nodi
        :return: lista dei nodi nella componente connessa
        """
        idToColor[u] = Color.Gray   #rendo grigio il nodo da che sto visitando
        visited.append(u)           #aggiungo il nodo u alla lista dei nodi visitati

        for i in self.arrNodes[u].adjArr:   #per ciascun nodo presente nella lista di adiacenza di u
            if idToColor[i] == Color.White:     #se il nodo non è ancora stato raggiunto
                self.DFS_Visited(i, visited, idToColor)     #richiamo la funzione di visita sul nodo non ancora visitato

        idToColor[u] = Color.Black      #aggiorno il colore del nodo di cui ho completato la visita
        return visited

    def connectedComponents(self):
        """
        :return CC: array di componenti connesse
        """
        idToColor = [Color.White]*self.numNodes     #assegno il colore bianco a ciascun nodo del grafo
        CC = []     #inizializzo la lista delle componenti connesse

        for v in range(self.numNodes):  #itero da 0 al numero dei nodi - 1 presenti nel grafo
            if idToColor[v] == Color.White:     #se il nodo non è ancora stato scoperto
                visited = []        #inizializzo la lista di nodi visitati al grafo
                comp = self.DFS_Visited(v, visited, idToColor)  #richiamo DFS_Visited sul nodo che sto trattando
                CC.append(comp)     #aggiungo la componente connessa
        return CC

    def removeNode(self, index_node):
        """
        :param index_node: indice del nodo che si vuole rimuovere
        :return none
        """
        for vertex in range(len(self.arrNodes)):    #itero da 0 al numero di nodi contenuti nel grafo
            num1 = len(self.arrNodes[vertex].adjArr)    #salvo la lunghezza della lista di adiacenza del vertice con indice vertex
            self.arrNodes[vertex].adjArr = [x for x in self.arrNodes[vertex].adjArr if x != index_node]     #elimino l'index_node se è presente nella lista di adiacenza di vertex
            num2 = len(self.arrNodes[vertex].adjArr)    #salvo la "nuova" lunghezza della lista di adiacenza del vertice con indice vertex
            if num2 < num1:     #se è stato eliminato un nodo
                self.numEdges -= 1  #diminuisco il numero di archi

        del self.arrNodes[index_node]   #elimino il nodo dal grafo
        self.numNodes -= 1      #diminuisco il contatore dei nodi del grafo

        for i in range(len(self.arrNodes)):     #eseguo una procedura di compattazione del grafo
            for j in range(len(self.arrNodes[i].adjArr)):
                if self.arrNodes[i].adjArr[j] > index_node:
                    self.arrNodes[i].adjArr[j] -= 1
            if self.arrNodes[i].id > index_node:
                self.arrNodes[i].id -= 1

    def getResilience(self):
        """
        :return max: dimensione della componente connessa più grande
        """
        CC = self.connectedComponents()     #ricavo la lista delle componenti connesse del grafo
        max = 0
        for index in CC:    #per ciascuna componente connessa
            if len(index) > max:    #se è più grande di max
                max = len(index)    #aggiorno max con la dimensione della componente connessa più grande
        return max

    def resilienceCalculator(self, seed):       #calcolo della resilienza in seguito alla disattivazione di nodi casuale
        """
        :param seed: seme del generatore di numeri casuali utilizzato
        :return: lista contenente le massime dimensioni delle componenti connesse del grafo
        """
        random.seed(seed)
        resilience = []     #inizializzo la lista delle resilienze
        while self.numNodes != 0:       #finchè non sono stati disattivati tutti i nodi
            index_node = random.randint(0, self.numNodes-1)     #scelgo l'indice del nodo da disattivare
            self.removeNode(index_node)     #rimuovo il nodo
            resilience.append(self.getResilience())     #aggiungo la dimensione della componente connessa maggiore presente attualmente nel grafo
        return resilience

    def intelligentSelectionResilienceCalculator(self):     #calcolo della resilienza in seguito alla disattivazione di nodi che presentano grado massimo
        """
        :return resilience: lista contenente le massime dimensioni delle componenti connesse del grafo
        """
        resilience = []     #inizializzo la lista delle resilienze
        while self.numNodes != 0:   #finche non sono stati disattivati tutti i nodi
            max_deg = 0     #grado massimo
            index_max = 0   #indice del nodo con grado massimo
            for i in range(len(self.arrNodes)):     #itero da 0 al numero di nodi presenti nel grafo - 1
                if max_deg < len(self.arrNodes[i].adjArr):  #se il grado massimo è minore della lunghezza della lista di adiacenza del nodo che sto analizzando
                    max_deg = len(self.arrNodes[i].adjArr)      #aggiorno il grado massimo
                    index_max = i       #aggiorno l'indice del grado massimo

            self.removeNode(index_max)  #rimuovo l'indice del nodo che presenta grado massimo
            resilience.append(self.getResilience())     #aggiungo la dimensione della componente connessa maggiore presente attualmente nel grafo
        return resilience


class ERGraph(Graph):

    def __init__(self, n, p, seed):
        """
            :param n: numero di nodi
            :param p: probabilità di generazione di un nodo
            :param seed: seme del generatore di numeri casuali utilizzato
            """
        super().__init__(n)     #utilizzo il costruttore di Graph per creare un grafo con n nodi
        random.seed(seed)       #setto il seed del generatore di numeri random

        for i in range(self.numNodes):  #itero i sul numero di nodi
            for j in range(self.numNodes):  #itero j sul numero di nodi
                a = random.uniform(0, 1)    #genero un numero casuale tra 0 e 1
                if a < p and i != j and j>i:    #se a è minore di p, l'arco che sto considerando di generare non rappresenta un cappio e non sto valutando di generare archi già valutati
                    self.arrNodes[i].addNodeToAdj(j)    #aggiungo i nodi da i a j
                    self.arrNodes[j].addNodeToAdj(i)    #e da j ad i al grafo
                    self.numEdges += 1          #aggiungo un arco al grafo


class UPAGraph(Graph):
    def __init__(self, n, m):
        """
        :param n: numero di nodi
        :param m: numero di nodi già presenti nell'urna
        """
        super().__init__(n)     #creo un grafo usando il costruttore di Graph
        self.numNodes = m

        jar = []    #inizializzo l'urna

        for i in range(m):  #da 0 ad m-1
            for j in range(i+1, m): #ottimizzato per i grafi non orientati
                self.arrNodes[i].addNodeToAdj(j)    #aggiungo il nodo j alla lista di adiacenza del nodo i
                self.arrNodes[j].addNodeToAdj(i)    #aggiungo il nodo i alla lista di adiacenza del nodo j
                self.numEdges += 1      #aggiorno il numero di archi

        #UPATrial
        for i in range(self.numNodes):
            for j in range(self.numNodes):
                jar.append(i)

        for u in range(m, n):
            jar, extraction = self.RunTrial(m, u, jar)
            for num in extraction:
                self.arrNodes[u].addNodeToAdj(num)   #aggiungo i nodi alle rispettive liste di adiacenza
                self.arrNodes[num].addNodeToAdj(u)
                self.numEdges += 1  #aggiorno il numero di archi

    def RunTrial(self, m, num_node, jar):
        """
        :param m: grado medio del grafo diviso 2
        :param num_node: numero di nodi già presenti nel grafo
        :param jar: lista che contiene i nodi presenti nel grafo
        :return jar, extraction: urna e estrazioni effettuate
        """
        extraction = []     #inizializzo la lista dei nodi estratti
        for i in range(m):      #eseguo m estrazioni di nodi
            u = random.randint(0, len(jar) - 1)     #effettuo un estrazione dall'urna
            extraction.append(jar[u])   #aggiungo il numero estratto all'urna
        jar.append(num_node)    #aggiungo un nuovo nodo all'urna
        jar.extend(extraction)  #aggiungo all'urna i nodi che sono stati estratti
        self.numNodes += 1      #aggiungo un nodo al grafo
        return jar, extraction


class DATAGraph(Graph):
    def __init__(self, n, file):
        """
        :param n: numero di nodi
        :param file: percorso in cui si trova il file da leggere
        """
        super().__init__(n)
        data = np.loadtxt(file, delimiter='\t', dtype=int)  #carico il file di testo
        startingNode = data[:, 0]   #salvo i nodi di "partenza"
        endingNode = data[:, 1]     #salvo i nodi di "arrivo"

        IdToNumberArr = list(set(startingNode))     #creo una lista ordinata dei nodi di partenza
        IdToNumberArr.sort()

        IdDictionary = {}       #corrispondenza ID_posizione nella lista

        for i in range(n):  #per ciascun nodo
            IdDictionary[IdToNumberArr[i]] = i  #assegno un ordinamento dei nodi che mi trovo in filename
        for i in range(len(startingNode)):
            #se l'arco non rappresenta un cappio, non è già presente e non è già stato inserito
            if startingNode[i] != endingNode[i] and not self.arrNodes[IdDictionary[endingNode[i]]].adjArr.__contains__(IdDictionary[startingNode[i]]) and not self.arrNodes[IdDictionary[startingNode[i]]].adjArr.__contains__(IdDictionary[endingNode[i]]):
                self.arrNodes[IdDictionary[startingNode[i]]].addNodeToAdj(IdDictionary[endingNode[i]])      #aggiorno la lista di adiacenza del nodo di partenza
                self.arrNodes[IdDictionary[endingNode[i]]].addNodeToAdj(IdDictionary[startingNode[i]])      #aggiorno la lista di adiacenza del nodo di arrivo
                self.numEdges += 1      #aggiorno il numero di archi


def printPlotRandom(ArrResilD, ArrResilER, ArrResilUPA, numNodes, fileName):
    t = np.arange(numNodes)     #creo un array di dimensione numNodes
    fig, ax = plt.subplots()
    #setto i parametri per la stampa dei grafici
    ax.set(xlabel="Nr. nodi disattivati",
           ylabel="Dimensione componente connessa più grande",
           title=fileName)

    ax.plot(t, ArrResilD, "r", label="Grafo dati reali")    #plot dei differenti tipi di grafi
    ax.plot(t, ArrResilER, "b", label="Grafo ER")
    ax.plot(t, ArrResilUPA, "g", label="Grafo UPA")


    ax.legend(loc="upper right", shadow=True, fontsize="medium")    #impostazioni della legenda
   

    plt.show()      #visualizzazione del grafico


def printPlotRandom_masked(ArrResilD, ArrResilER, ArrResilUPA, numNodes, fileName):
    t = np.arange(numNodes)     #creo un array di dimensione numNodes
    fig, ax = plt.subplots()
    # setto i parametri per la stampa dei grafici
    ax.set(xlabel="Nr. nodi disattivati",
           ylabel="Dimensione componente connessa più grande",
           title=fileName)

    ax.plot(t, ArrResilD, "#ff6666", label="Grafo dati reali", linewidth=0.75)  #plot dei differenti tipi di grafi
    ax.plot(t, ArrResilER, "#8080ff", label="Grafo ER", linewidth=0.75)
    ax.plot(t, ArrResilUPA, "#66ff66", label="Grafo UPA", linewidth=0.75)

    #creazione dell'andamento resiliente
    y_threshold = []
    for i in range(numNodes):
        y_threshold.append((numNodes - i) * 0.75)

    x_threshold = numNodes * 0.2    #individuazione del punto in cui sono stati disattivati il 20% dei nodi

    #stampe
    ax.plot(y_threshold, linewidth=0.5, color="k",label="Andamento resiliente")
    ax.axvline(x=x_threshold, linewidth=0.5, color="k", label="20% nodi disattivati")

    ax.legend(loc="upper right", shadow=True, fontsize="medium")    #stampa della legenda



    plt.show()      #visualizzazione del grafico

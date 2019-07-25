from Node import Node
from Edge import Edge
import sys

class Tuple:
    def __init__(self, id, value):
        self.id = id  #  id della stazione a cui corrisponde il nodo
        self.value = value  # valore del nodo nella heap che corrisponde alla distanza dall origine

class BinaryHeap:
    def __init__(self):
        self.list_vertices = []  # lista di nodi contenuti nella heap binaria ogni elemento è una Tupla (valore, id stazione)

    def add(self, id, value):
        """
        :param id: id nodo
        :param value: valore del nodo che corrisponde alla distanza
        :return: aggiunge alla heap il nodo
        """
        self.list_vertices.append(Tuple(id, value))
        n = len(self.list_vertices)
        self.bubbleUp(n-1)

    def left(self, i):
        """
        :param i: indice nodo
        :return: ritorna il nodo a sinistra del nodo di indice i
        """
        return (2*i)+1

    def right(self, i):
        """
        :param i: indice nodo
        :return: ritorna il nodo a destra del nodo di indice i
        """
        return (2*i)+2

    def parent(self, i):
        """
        :param i: indice del nodo
        :return: ritorna il padre del nodo di indice i
        """
        return int((i-1)/2)

    def bubbleUp(self, i):  # modifica la heap facendo salire nella posizione corretta il nodo di indice i
        """
        :param i: indice del nodo
        """
        p = self.parent(i)
        while i > 0 and self.list_vertices[i].value < self.list_vertices[p].value:
            temp = self.list_vertices[p]
            self.list_vertices[p] = self.list_vertices[i]
            self.list_vertices[i] = temp  #  scambio A[i] con A[p]
            i = p
            p = self.parent(i)

    def decreaseKey(self, nodeId, value):  # diminuisce il valore del nodo al valore value
        """
        :param nodeId: id del nodo
        :param value: è la distanza dallo starting node al nodo con id = nodeId
        """
        for i, x in enumerate(self.list_vertices):
            if x.id == nodeId and self.list_vertices[i].value > value:
                self.list_vertices[i].value = value
                self.bubbleUp(i)
                return True
        return False

    def trickleDown(self, i):  # fa scendere un nodo nella heap
        """
        :param i: id del nodo
        """
        l = self.left(i)
        r = self.right(i)
        n = len(self.list_vertices)
        smallest = i
        if l < n and self.list_vertices[l].value < self.list_vertices[i].value:
            smallest = l
        if r < n and self.list_vertices[r].value < self.list_vertices[smallest].value:
            smallest = r
        if smallest != i:
            temp = self.list_vertices[smallest]
            self.list_vertices[smallest] = self.list_vertices[i]
            self.list_vertices[i] = temp
            self.trickleDown(smallest)

    def extractMin(self):
        """
        :return: ritorna il primo nodo nella heap che sarà quello con valore (distanza) minore
        """
        minimum = self.list_vertices[0]
        n = len(self.list_vertices)
        self.list_vertices[0] = self.list_vertices[n - 1]
        self.list_vertices.pop(n - 1)  #  elimina l'elemento copiato in cima (duplicato)
        self.trickleDown(0)
        return minimum

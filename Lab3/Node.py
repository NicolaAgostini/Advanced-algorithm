class Node:
    def __init__(self, id):
        self.id = id         # id della stazione
        self.adj_arr = []    # lista degli archi che partono dal nodo

    def addEdgeToNode(self, arco):
        self.adj_arr.append(arco)   # aggiungo un arco alla lista di adiacenza del nodo



class Tree:
    leader = []     # lista di leader, leader[i] punta all'indice del nodo che è leader del set a cui appartiene i
    next = []       # lista di next, next[i] punta al prossimo nodo presente all'interno del set a cui appartiene i

    def __init__(self, num_nodes):
        """
        :param num_nodes: numero di nodi del grafo
        """
        for i in range(num_nodes):      # per ciascun nodo
            self.leader.append(-1)      # inizializzo a null il leader
            self.next.append(-1)        # inizializzo a null i puntatori al prossimo nodo

    def makeSet(self, x):
        """
        :param x: indice del nodo di cui si vuole creare l'insieme
        """
        self.leader[x] = x      # il leader del nodo ad indice x è sè stesso

    def findSet(self, x):
        """
        :param x: indice del nodo di cui si vuole il leader
        :return: il leader del nodo x
        """
        return self.leader[x]

    def union(self, x, y):
        lead_x = self.findSet(x)        # cerco il leader degli insiemi
        lead_y = self.findSet(y)
        y = lead_y
        self.leader[y] = lead_x     # pongo il leader di x come il nuovo leader di y
        while self.next[y] != -1:   # finchè esistono nodi successivi ad y
            y = self.next[y]
            self.leader[y] = lead_x     # aggiorno il leader di y con il leader di x

        self.next[y] = self.next[lead_x]
        self.next[lead_x] = lead_y


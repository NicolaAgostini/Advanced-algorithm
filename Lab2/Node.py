class Node:
    def __init__(self, id):
        self.id = id         #id della stazione
        self.adj_arr = []    # lista degli archi che partono dal nodo
        self.posX = 0       #latitudine
        self.posY = 0       #longitudine

    def addEdgeToNode(self, arco):
        self.adj_arr.append(arco)   #aggiungo un arco alla lista di adiacenza del nodo

    def setPosX(self, posX):    #aggiorno la latitudine del nodo
        self.posX = posX

    def setPosY(self, posY):    #aggiorno la longitudine del nodo
        self.posY = posY

    def setCoordinates(self, posX, posY):   #aggiorno le coordinate del nodo
        self.setPosX(posX)
        self.setPosY(posY)



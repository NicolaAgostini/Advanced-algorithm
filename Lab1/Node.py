class Node:

    def __init__(self, id):
        self.id = id
        self.adjArr = []
    def getID(self):
        return self.id
    def addNodeToAdj(self, IdNode):
        self.adjArr.append(IdNode)
    def print(self):
        print("Nodo:", self.id, "Adj:", self.adjArr)
    def getAdjArr(self):
        return self.adjArr

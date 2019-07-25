from Shire import Shire


class Cluster:

    def __init__(self, i, j, id):
        """
        :param centroid: tuple of 2 coordinates(x,y)
        """
        self.id = id
        self.pos_x = i
        self.pos_y = j
        self.elements = []
        self.addElementToCluster([self.pos_x, self.pos_y, self.id])


    def printCluster(self):
        print("Cluster in posizione " + str(self.pos_x) + " " + str(self.pos_y) + " con elementi:")
        for el in self.elements:
            print(el.id)

    def addElementToCluster(self, el):
        self.elements.append(el)     # todo da togliere gli elementi dal cluster shire

    def unionCluster(self, cluster):
        # Inserisce le contee del cluster da unire in questo
        for el in cluster.elements:
            self.addElementToCluster(el)

        # Calcolo la nuova x e y come baricentro tra tutti i nodi
        self.updateCentroids()
        return self

    def distanceBetweenCluster(self, cluster_2):
        """
        :param cluster_2:  cluster da confrontare
        :return: calcola la distanza euclidea fra il centroide del cluster stesso e il centroide del cluster2
        """
        return float(float(float(float(self.pos_x) - float(cluster_2.pos_x))**2 +
                           float(float(self.pos_y) - float(cluster_2.pos_y))**2) ** 0.5)

    def updateCentroids(self):
        sum_x = 0
        sum_y = 0
        for el in self.elements:
            sum_x += el[0]
            sum_y += el[1]
        self.pos_x = sum_x / len(self.elements)
        self.pos_y = sum_y / len(self.elements)



from Cluster import Cluster
from Shire import Shire

import numpy as np
import sys
import copy
import time


class Graph:

    def __init__(self, number_of_shires, shires):
        self.number_of_shires = number_of_shires
        self.shires = shires
        # for i in range(number_of_shires):
        #    self.shires.append(Shire(shires[i].id, shires[i].posX, shires[i].posY, shires[i].population, shires[i].cancer_risk))

    def hierarchicalClustering(self, points, k, shire_dict):
        """
        :param k: numero di cluster richiesti
        :return: un insieme di k cluster che partizionano le contee
        """

        P = points[points[:, 1].argsort()]
        S = points[points[:, 2].argsort()]
        #print(P)
        clusters = [Cluster(i[1], i[2], i[0]) for k, i in enumerate(P)]
        #print(clusters)
        idToCluster = {}
        for cl in clusters:
            idToCluster[cl.id] = cl

        distortion = []

        while len(idToCluster) > k:
            print(len(idToCluster))

            minimum = self.fastClosestPair(P, S, idToCluster)


            newCluster = minimum[1]
            delCluster = minimum[2]     # l'indice corrisponde all'id del cluster



            idToCluster[newCluster] = idToCluster[newCluster].unionCluster(idToCluster[delCluster])     # unisco i due cluster mettendo tutti gli elementi di clusters[delCluster] in clusters[newCluster]

            del idToCluster[delCluster]
            P = np.empty([len(idToCluster), 3])
            i = 0
            for key in idToCluster:
                P[i] = [key, idToCluster[key].pos_x, idToCluster[key].pos_y]
                i += 1
            P = P[P[:, 1].argsort()]
            S = P[P[:, 2].argsort()]


            if len(idToCluster) <= 20:
                distortion.append(self.calculateErrorHierarchical(shire_dict, idToCluster))






        return distortion, idToCluster      # ritorno la lista dei cluster

    def fastClosestPair(self, P, S, idToCluster):
        '''
        :param P: lista di n cluster in cui ogni cluster ha un id e una coppia x,y ordinati per x crescente
        :param S: lista di indici dei punti P ordinati per y crescente
        :return: tripla minima
        '''
        n = len(P)
        tripla_minima = [sys.maxsize, -1, -1]
        if n <= 3:
            return self.slowClosestPair(P)
        else:
            m = int(n/2)
            P_l = P[0:m]    # filtro i valori di P con la condizione che ogni elemento sia in range(m)
            P_r = P[m:]    #     filtro i valori di P con la condizione che ogni elemento sia in range(m, n)
            S_l, S_r = self.split(S, P_l, P_r)
            tripla_minima_l = self.fastClosestPair(P_l, S_l, idToCluster)
            tripla_minima_r = self.fastClosestPair(P_r, S_r, idToCluster)
            if tripla_minima_l[0] <= tripla_minima_r[0]:
                tripla_minima = tripla_minima_l
            else:
                tripla_minima = tripla_minima_r
            mid = 0.5 * (P[m-1][1] + P[m][1])

            to_return = self.closestPairStrip(S, mid, tripla_minima[0], P, idToCluster)

            if tripla_minima[0] <= to_return[0]:
                return tripla_minima
            else:
                return to_return


    def closestPairStrip(self, S, mid, d, P, idToCluster):
        '''
        :param S: lista di n indici di punti ordinati per y crescente
        :param mid: valore reale
        :param d: valore reale positivo
        :param P: lista di cluster
        :return:
        '''
        n = len(S)
        S_ = []
        k = 0

        for i in range(n):
            if abs(S[i][1] - mid) < d:
                S_.append(S[i][0])
                k += 1
        tripla_minima = [sys.maxsize, -1, -1]



        for u in range(k-1):         #TODO: CONTROLLAMI L'intervallo

            for v in range(u+1, min(u + 5, n - 1) + 1):
                #print(S_)
                if v < len(S_):
                    temp = self.distanceBetweenPoints([idToCluster[S_[u]].pos_x, idToCluster[S_[u]].pos_y], [idToCluster[S_[v]].pos_x, idToCluster[S_[v]].pos_y])
                    if v < len(S_) and tripla_minima[0] > temp:
                        tripla_minima = [temp, S_[u], S_[v]]
        return tripla_minima

    def slowClosestPair(self, clusters):
        '''
        :param clusters: una lista di clusters dove sono importanti gli id dei cluster e le coordinate X e Y
        :return:
        '''
        tripla_minima = [sys.maxsize, -1, -1]
        for i, p_u in enumerate(clusters):
            for j, p_v in enumerate(clusters):
                if j > i:    # cioè considero la matrice triangolare superiore
                    min_dist = tripla_minima[0]
                    if self.distanceBetweenPoints(p_u[1:], p_v[1:]) < min_dist:
                        tripla_minima = [self.distanceBetweenPoints(p_u[1:], p_v[1:]), p_u[0], p_v[0]]
        return tripla_minima


    def split(self, S, P_l, P_r):
        '''
        :param S: lista contenente gli indici da 0 a n-1 ordinati per y crescente
        :param P_l: lista di cluster contentente partizione dell'inisieme dei centroidi
        :param P_r: lista di cluster contenente partizione dell'inisieme dei centroidi
        :return: due vettori ordinati che contengono gli elementi in P_l e P_r
        '''
        n = len(S)
        S_l, S_r = [], []
        j, k = 0, 0
        for i in range(n):
            if S[i] in P_l:
                S_l.append(S[i])
                j += 1
            else:
                S_r.append(S[i])
                k += 1
        return S_l, S_r




    def kMeansClustering(self, k, iter, points):
        """
        :param k: numero di cluster richiesti
        :param iter: numero di iterazioni da effettuare
        :param points: lista di contee
        :return: un insieme di k cluster che partizionano le contee
        """

        n = self.number_of_shires

        ordered_shire = sorted(self.shires, reverse=True, key=self.sortSecond)
        top_shires = ordered_shire[0:k]  # k contee con popolazione più elevata
        centroids = []
        for i in range(k):          # creo i k centroidi iniziali
            centroids.append([top_shires[i].posX, top_shires[i].posY])


        for i in range(iter):   # aggiungo k cluster, ciascuno con una delle k contee con più popolazione
            clusters = []          # lista di cluster in del tipo (id_cluster: cluster) TODO LASCIAMOLO DENTRO
            for i in range(k):
                clusters.append(-1)
            #cluster = Cluster(top_shires[i].posX, top_shires[i].posY, top_shires[i].id)  # creo l'istanza di cluster corrente
            #clusters[cluster.id] = cluster      #     TODO Forse non servono
            for j in range(n):
                minimum = sys.maxsize

                for f in range(k):
                    if minimum > self.distanceBetweenPoints(centroids[f], [points[j].posX, points[j].posY]):
                        minimum = self.distanceBetweenPoints(centroids[f], [points[j].posX, points[j].posY])
                        l = f       # assegno l'indice del centroide avente distanza minima dal punto

                if clusters[l] == -1:

                    clusters[l] = Cluster(points[j].posX, points[j].posY, points[j].id)
                else:

                    clusters[l].addElementToCluster([points[j].posX, points[j].posY, points[j].id])        # aggiungo al cluster con indice l il punto j

            for index in range(k):
                clusters[index].updateCentroids()
                centroids[index] = [clusters[index].pos_x, clusters[index].pos_y]
                #print(centroids[index])


        return clusters


    def sortSecond(self, val):
        return int(val.population)

    def distanceBetweenPoints(self, centroid, point):
        """
        :param centroid: punto di partenza iniziale nella forma [posX, posY]
        :param point: punto di arrivo nella forma [posX, posY]
        :return :
        """
        return float(((centroid[0] - point[0])**2 + (centroid[1] - point[1])**2)**0.5)

    def calculateErrorHierarchical(self, shire_dict, clusters):
        """
        :param shire_dict:
        :param clusters: elenco dei cluster creati dall'algoritmo
        :return:
        """
        distortion = 0
        for cl in clusters:
            centroid = [clusters[cl].pos_x, clusters[cl].pos_y]
            total_sum = 0
            for el in clusters[cl].elements:
                element = [el[0], el[1]]
                delta = self.calculateDistance(centroid, element)
                population = float(shire_dict[el[2]].population)
                total_sum += population * (delta ** 2)
            distortion += total_sum

        return distortion

    def calculateDistance(self, centroid, point):
        return float(((centroid[0] - point[0]) ** 2 + (centroid[1] - point[1]) ** 2) ** 0.5)


from Shire import Shire
from Graph import Graph
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
from sklearn.cluster import AgglomerativeClustering

def main():
    path_file = ["./unifiedCancerData_212.csv", "./unifiedCancerData_562.csv", "./unifiedCancerData_1041.csv",
                 "./unifiedCancerData_3108.csv"]
    #path_file = ["./unifiedCancerData_3108.csv"]
    #path_file = ["./unifiedCancerData_562.csv"]
    #path_file = ["./piccolo_esempietto.csv"]

    for file in path_file:
        points = np.loadtxt(file, delimiter=",", usecols=(0, 1, 2))
        shire_list = []  # contiene tutte le contee presenti nel file
        shire_dict = {}  # contiene l'id della contea associata alla shire
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                line_count += 1
                shire = Shire(int(row[0]), float(row[1]), float(row[2]), row[3], row[4])
                shire_list.append(shire)
                shire_dict[int(row[0])] = shire

        graph = Graph(len(shire_list), shire_list)

        clustersH = -1
        clustersK = -1

        distH = []
        distK = []

        distH, clustersH = graph.hierarchicalClustering(points, 6, shire_dict)
        distH.reverse()
        for i in range(6, 21):
            clustersK = graph.kMeansClustering(i, 5, shire_list)
            distK.append(calculateErrorKMeans(shire_dict, clustersK))
        x = np.arange(6, 21)
        fig, ax = plt.subplots()
        ax.plot(x, distH, color='r', label="Hierarchical")
        ax.plot(x, distK, color='g', label="K_Means")
        ax.set(xlabel="Number of clusters", ylabel="Distortion", title=str(len(points))+" nodes")
        plt.legend()
        plt.savefig(str(len(points))+" nodes.png")
        plt.show()
        print("DISTORTION HIERARCHICAL:", distH)
        print("DISTORTION K_MEANS:", distK)
        """
        if clustersH != -1:

            distortion = calculateErrorHierarchical(shire_dict, clustersH)
            print("Distorsione = ", distortion)
            colors = matplotlib.cm.rainbow(np.linspace(0, 1, 30))
            i = 0
            img = plt.imread("./USA_Counties.png")
            fig, ax = plt.subplots()
            for cl in clustersH:
                shires_x = [x[0] for x in clustersH[cl].elements]
                shires_y = [x[1] for x in clustersH[cl].elements]


                ax.plot(clustersH[cl].pos_x, clustersH[cl].pos_y, 'o', markersize=4, c=colors[i])
                for el in clustersH[cl].elements:
                    ax.plot([clustersH[cl].pos_x, el[0]], [clustersH[cl].pos_y, el[1]], 'o-', c=colors[i], lw=0.2, markersize=2)
                i += 1
            ax.invert_yaxis()
            ax.imshow(img)
            plt.show()
        
        
        clustersK = graph.kMeansClustering(30, 5, shire_list)
        
        if clustersK != -1:
            distortion = calculateErrorKMeans(shire_dict, clustersK)
            print("Distorsione = ", distortion)
            colors = matplotlib.cm.rainbow(np.linspace(0, 1, 30))
            i = 0
            img = plt.imread("./USA_Counties.png")
            fig, ax = plt.subplots()
            for cl in clustersK:
                ax.plot(cl.pos_x, cl.pos_y, 'o', markersize=4, c=colors[i])
                for k in cl.elements:
                    ax.plot([cl.pos_x, k[0]], [cl.pos_y, k[1]], 'o-', c=colors[i], lw=0.2, markersize=2)
                i += 1
            ax.invert_yaxis()
            ax.imshow(img)
            plt.show()
        """

def calculateErrorHierarchical(shire_dict, clusters):
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
            delta = calculateDistance(centroid, element)
            population = float(shire_dict[el[2]].population)
            total_sum += population*(delta**2)
        distortion += total_sum

    return distortion

def calculateErrorKMeans(shire_dict, clusters):
    """
    :param shire_list:
    :param clusters:
    :return:
    """
    distortion = 0
    for cl in clusters:
        centroid = [cl.pos_x, cl.pos_y]
        total_sum = 0
        for el in cl.elements:
            element = [el[0], el[1]]
            delta = calculateDistance(centroid, element)
            population = float(shire_dict[el[2]].population)
            total_sum += population*(delta**2)
        distortion += total_sum

    return distortion

def calculateDistance(centroid, point):
    return float(((centroid[0] - point[0]) ** 2 + (centroid[1] - point[1]) ** 2) ** 0.5)


if __name__ == '__main__':
    main()

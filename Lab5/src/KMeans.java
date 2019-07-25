import java.sql.Array;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;

class KMeans{

    public Map<Integer, Cluster> serialKMeans(List<City> cities, int k, int num_it){
        int n = cities.size();

        List<City> firstFifty = cities.subList(0, k);

        // Creo la lista dei centroidi
        Map<Integer, Point> centroids = new HashMap<Integer, Point>();
        for (int i = 0; i < k; i++) {
            centroids.put(i, firstFifty.get(i).coordinates);
        }

        Map<Integer, Cluster> clusters = new HashMap<Integer, Cluster>();
        for (int i=0; i<num_it; i++) {
            clusters = new HashMap<Integer, Cluster>();

            // Creo n cluster vuoti (solo con i centroidi)
            for(Map.Entry<Integer, Point> c : centroids.entrySet()) {
                clusters.put(c.getKey(), new Cluster(c.getValue(), new LinkedList<>()));
            }

            // Trovo per ogni città il centroide più vicino
            for(int j = 0; j < n; j++) {
                int nearestCentroidIndex = findNearestIndexOfCentroid(cities.get(j), centroids);
                clusters.get(nearestCentroidIndex).addElementToCluster(cities.get(j));
            }

            // Aggiorno tutti i centroidi dopo l'aggiunta degli elementi ai cluster
            for (int j = 0; j < k ; j++){
                Point newCentroid = clusters.get(j).updateCentroid();
                centroids.put(j, newCentroid);
            }
        }
        return clusters;
    }

    private int findNearestIndexOfCentroid(City nodo, Map<Integer, Point> centroids) {
        double minDistFound = 1000000000;
        int indexMinCentroid = -1;

        for(Map.Entry<Integer, Point> a : centroids.entrySet()) {
            double distance = a.getValue().getDistance(nodo.coordinates);
            if (distance < minDistFound) {
                minDistFound = distance;
                indexMinCentroid = a.getKey();
            }
        }
        return indexMinCentroid;
    }


    public ConcurrentHashMap<Integer, Cluster> parallelKMeans(List<City> cities, int k, int num_it, int cutoff) {
        ForkJoinPool pool = new ForkJoinPool();

        int n = cities.size();

        List<City> firstFifty = cities.subList(0, k);

        // Creo la lista dei centroidi
        ConcurrentHashMap<Integer, Point> centroids = new ConcurrentHashMap<Integer, Point>();

        AtomicInteger a = new AtomicInteger(k);
        pool.invoke(new ParallelFor1(centroids, firstFifty, 0, k, a, cutoff));
        while( a.get() > 0 ) {
            Thread.yield();
        }

        ConcurrentHashMap<Integer, Cluster> clusters = new ConcurrentHashMap<Integer, Cluster>();
        for (int i=0; i<num_it; i++) {
            clusters = new ConcurrentHashMap<Integer, Cluster>();

            AtomicInteger b = new AtomicInteger(k);
            pool.invoke(new ParallelFor2(clusters, centroids, 0, k, b, cutoff));
            while (b.get() > 0) {
                Thread.yield();
            }


            AtomicInteger c = new AtomicInteger(n);
            pool.invoke(new ParallelFor3(clusters, centroids, cities, 0, n, c, cutoff));
            while (c.get() > 0) {
                Thread.yield();
            }

            // Aggiorno tutti i centroidi dopo l'aggiunta degli elementi ai cluster
            for (int j = 0; j < k; j++) {
                Point newCentroid = clusters.get(j).updateCentroid();
                centroids.put(j, newCentroid);
            }
        }
        return clusters;
    }
}

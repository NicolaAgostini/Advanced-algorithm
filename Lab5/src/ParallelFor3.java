import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.RecursiveAction;
import java.util.concurrent.atomic.AtomicInteger;

class ParallelFor3 extends RecursiveAction {

    private ConcurrentHashMap<Integer, Cluster> arrayConteniore;
    private ConcurrentHashMap<Integer, Point> arrayDaAggiungere;
    private List<City> arrayCity;
    private int from;
    private int to;
    private AtomicInteger a;
    private int cutoff ;

    public ParallelFor3(ConcurrentHashMap<Integer, Cluster> arrayConteniore, ConcurrentHashMap<Integer, Point> arrayDaAggiungere, List<City> arrayCity, int from, int to, AtomicInteger a, int cutoff) {
        this.arrayConteniore = arrayConteniore;
        this.arrayDaAggiungere = arrayDaAggiungere;
        this.arrayCity = arrayCity;
        this.from = from;
        this.to = to;
        this.a = a;
        this.cutoff = cutoff;
    }

    @Override
    protected void compute() {
        int len = to - from;
        if (len < cutoff) {
            work(arrayConteniore, arrayDaAggiungere, arrayCity, from, to);
        } else {
            int mid = (from + to) / 2;
            invokeAll(new ParallelFor3(arrayConteniore, arrayDaAggiungere, arrayCity, from, mid, a, cutoff),
                    new ParallelFor3(arrayConteniore, arrayDaAggiungere, arrayCity, mid, to, a, cutoff));
        }

    }

    private void work(ConcurrentHashMap<Integer, Cluster> arrayConteniore, ConcurrentHashMap<Integer, Point> arrayDaAggiungere, List<City> arrayCity, int from, int to) {
        for (int j = from; j < to; j++) {
            int nearestCentroidIndex = findNearestIndexOfCentroid(arrayCity.get(j), arrayDaAggiungere);
            arrayConteniore.get(nearestCentroidIndex).addElementToCluster(arrayCity.get(j));
            a.decrementAndGet();
        }
    }

    private int findNearestIndexOfCentroid(City nodo, ConcurrentHashMap<Integer, Point> centroids) {
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
}


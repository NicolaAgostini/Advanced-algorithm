import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.RecursiveAction;
import java.util.concurrent.atomic.AtomicInteger;

class ParallelFor2 extends RecursiveAction {

    private Map<Integer, Cluster> arrayConteniore;
    private Map<Integer, Point> arrayDaAggiungere;
    private int from;
    private int to;
    private AtomicInteger a;
    private int cutoff ;

    public ParallelFor2(Map<Integer, Cluster> arrayConteniore, Map<Integer, Point> arrayDaAggiungere, int from, int to, AtomicInteger a, int cutoff) {
        this.arrayConteniore = arrayConteniore;
        this.arrayDaAggiungere = arrayDaAggiungere;
        this.from = from;
        this.to = to;
        this.a = a;
        this.cutoff = cutoff;
    }

    @Override
    protected void compute() {
        int len = to - from;
        if (len < cutoff) {
            work(arrayConteniore, arrayDaAggiungere, from, to);
        } else {
            int mid = (from + to) / 2;
           invokeAll(new ParallelFor2(arrayConteniore, arrayDaAggiungere, from, mid, a, cutoff),
            new ParallelFor2(arrayConteniore, arrayDaAggiungere, mid, to, a, cutoff));
        }

    }

    private void work(Map<Integer, Cluster> arrayConteniore, Map<Integer, Point> arrayDaAggiungere, int from, int to) {
        for (int j = from; j < to; j++) {
            arrayConteniore.put(j, new Cluster(arrayDaAggiungere.get(j), new CopyOnWriteArrayList<City>()));
            a.decrementAndGet();
        }
    }
}
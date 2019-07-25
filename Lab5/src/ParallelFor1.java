import java.util.List;
import java.util.Map;
import java.util.concurrent.RecursiveAction;
import java.util.concurrent.atomic.AtomicInteger;

class ParallelFor1 extends RecursiveAction {

    private Map<Integer, Point> arrayConteniore;
    private List<City> arrayDaAggiungere;
    private int from;
    private int to;
    private AtomicInteger a;
    private int cutoff;

    public ParallelFor1(Map<Integer, Point> arrayConteniore, List<City> arrayDaAggiungere, int from, int to, AtomicInteger a, int cutoff) {
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
            invokeAll(new ParallelFor1(arrayConteniore, arrayDaAggiungere, from, mid, a, cutoff),
            new ParallelFor1(arrayConteniore, arrayDaAggiungere, mid, to, a, cutoff));
        }
    }

    private void work(Map<Integer, Point>arrayConteniore, List<City> arrayDaAggiungere, int from, int to) {
        for (int j = from; j < to; j++) {
            arrayConteniore.put(j, arrayDaAggiungere.get(j).coordinates);
            a.decrementAndGet();
        }
    }
}
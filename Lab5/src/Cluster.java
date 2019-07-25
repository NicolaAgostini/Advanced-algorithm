import java.util.List;

public class Cluster {
    private Point centroid;
    private List<City> elements;
    public Cluster(Point centroid, List<City> elements){
        this.centroid = centroid;
        this.elements = elements;
    }
    public void addElementToCluster(City element){
        this.elements.add(element);
    }

    public Point updateCentroid(){
        double sumX = 0;
        double sumY = 0;
        for (City nodo: this.elements){
            sumX += nodo.coordinates.x;
            sumY += nodo.coordinates.y;
        }
        this.centroid = new Point(sumX / this.elements.size(), sumY / this.elements.size());

        return this.centroid;
    }

    public String toString() {
        return "[" + this.centroid + "," + this.elements.size() + "]";
    }


}

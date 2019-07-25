import java.util.List;
public class Point{
    public double x;
    public double y;
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double getDistance(Point other) {
        return Math.sqrt(Math.pow(this.x - other.x, 2)
                + Math.pow(this.y - other.y, 2));
    }

    public int getNearestPointIndex(List<Point> points) {
        int index = -1;
        double minDist = Double.MAX_VALUE;
        for (int i = 0; i < points.size(); i++) {
            double dist = this.getDistance(points.get(i));
            if (dist < minDist) {
                minDist = dist;
                index = i;
            }
        }
        return index;
    }

    public static Point getMean(List<Point> points) {
        float accumX = 0;
        float accumY = 0;
        if (points.size() == 0) return new Point(accumX, accumY);
        for (Point point : points) {
            accumX += point.x;
            accumY += point.y;
        }
        return new Point(accumX / points.size(), accumY / points.size());
    }

    public String toString() {
        return "[" + this.x + "," + this.y + "]";
    }

    public boolean equals(Object obj) {
        if (obj == null || !(obj.getClass() != Point.class)) {
            return false;
        }
        Point other = (Point) obj;
        return this.x == other.x && this.y == other.y;
    }
}
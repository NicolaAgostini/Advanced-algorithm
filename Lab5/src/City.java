public class City {
    private int id;
    private String name;
    private int population;
    Point coordinates;

    public City(String[] values) {
        this.id = Integer.parseInt(values[0]);
        this.name = values[1];
        this.population = Integer.parseInt(values[2]);
        double latitude = Double.parseDouble(values[3]);
        double longitude = Double.parseDouble(values[4]);
        this.coordinates = new Point(latitude, longitude);
    }

    public int getPopulation() {
        return population;
    }

    @Override
    public String toString() {
        return "[" + this.id + ", " + this.name + ", " + this.population + ", " + this.coordinates.x + ", " + this.coordinates.y +"]";
    }
}

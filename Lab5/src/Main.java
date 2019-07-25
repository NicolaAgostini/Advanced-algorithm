import org.knowm.xchart.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.lang.Math;
import java.util.concurrent.ConcurrentHashMap;


public class Main {

    private static final String SAMPLE_CSV_FILE_PATH = "./src/cities-and-towns-of-usa.csv";


    private static void stampaTerminale(String domanda, ArrayList<Double> arraySeriale, ArrayList<Double> arrayParallelo){
        System.out.println("\n\n~~~~ " + domanda);
        System.out.print("KMeans seriale: \n\t");
        for (double time: arraySeriale) {
            System.out.print(time + " ");
        }
        System.out.print("\nKMeans parallelo: \n\t");
        for (double time: arrayParallelo) {
            System.out.print(time + " ");
        }
    }

    private static void stampaGrafico(String titolo, String asseX, ArrayList<Double> arraySeriale, ArrayList<Double> arrayParallelo, ArrayList<Double> arrayX){

        double[] yDataS=new double[arraySeriale.size()];
        for(int i=0; i< arraySeriale.size(); i++) {
            yDataS[i] = arraySeriale.get(i);
        }
        double[] yDataD=new double[arrayParallelo.size()];
        for(int i=0; i< arrayParallelo.size(); i++) {
            yDataD[i] = arrayParallelo.get(i);
        }
        double[] xData=new double[arrayX.size()];
        for(int i=0; i< arrayX.size(); i++) {
            xData[i] = arrayX.get(i);
        }

        // Create Chart
        XYChart chart = new XYChartBuilder().width(800).height(600).title(titolo).xAxisTitle(asseX).yAxisTitle("Tempo di esecuzione in ms").build();
        chart.addSeries("Seriale", xData, yDataS);
        chart.addSeries("Parallelo", xData, yDataD);
        // Show it
        new SwingWrapper(chart).displayChart();

        // Save it
        try {
            BitmapEncoder.saveBitmap(chart, "./"+titolo, BitmapEncoder.BitmapFormat.PNG);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        List<City> citiesList = new ArrayList<City>();

        // Lettura file
        try (BufferedReader br = new BufferedReader(new FileReader(SAMPLE_CSV_FILE_PATH))) {
            String line;
            br.readLine();
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                int deg = (int)(Double.parseDouble(values[3]));      // tronca all'intero
                double min = Float.parseFloat(values[3]) - deg;
                double rad_x= Math.PI * (deg + 5.0 * min / 3.0) / 180.0;    //calcolo coordinata x
                values[3] = ""+rad_x;
                deg = (int)(Double.parseDouble(values[4]));
                min = Float.parseFloat(values[4]) - deg;
                double rad_y = Math.PI * (deg + 5.0 * min / 3.0) / 180.0;    // calcolo coordinata y
                values[4] = ""+rad_y;
                City city = new City(values);
                citiesList.add(city);
            }
            citiesList.sort((a, b)-> a.getPopulation() - b.getPopulation());
            Collections.reverse(citiesList);

            // Parametri
            ArrayList<Integer> threshold = new ArrayList<Integer>();
            threshold.add(-1);
            threshold.add(250);
            threshold.add(2000);
            threshold.add(5000);
            threshold.add(15000);
            threshold.add(50000);
            threshold.add(100000);

            int k = 50; // numero di cluster

            int iter = 100; // iterazioni

            int cutoff = 20;

            KMeans kmeans = new KMeans();

            // TEST
//            double startS = System.currentTimeMillis();
//            Map<Integer, Cluster> S = kmeans.serialKMeans(citiesList, k, iter);
//            double timeS = System.currentTimeMillis() - startS;
//            System.out.println(timeS);
//
//            double startP = System.currentTimeMillis();
//            ConcurrentHashMap<Integer, Cluster> P = kmeans.parallelKMeans(citiesList, k, iter, cutoff);
//            double timeP = System.currentTimeMillis() - startP;
//            System.out.println(timeP);


            // DOMANDA 1

            ArrayList<Double> serialTimeD1 = new ArrayList<Double>();
            ArrayList<Double> parallelTimeD1 = new ArrayList<Double>();

            // Ordinamento città
            int index_threshold = citiesList.size();

            List<City> cities = new ArrayList<>(citiesList);
            ArrayList<Double> numero_citta = new ArrayList<Double>();

            for (int tr: threshold) {

                // Creo sottoinsieme di città in base al limite di popolazione
                if(tr != -1) {
                    for (int i = 0; i < citiesList.size(); i++) {
                        if ((tr != -1) && citiesList.get(i).getPopulation() < tr) {
                            index_threshold = i;
                            break;
                        }
                    }
                    cities = citiesList.subList(0, index_threshold);
                }
                numero_citta.add((double)cities.size());

                // Seriale
                double startD1S = System.currentTimeMillis();
                Map<Integer, Cluster> D1S = kmeans.serialKMeans(cities, k, iter);
                double timeD1S = System.currentTimeMillis() - startD1S;
                serialTimeD1.add(timeD1S);

                // Parallelo
                double startD1P = System.currentTimeMillis();
                ConcurrentHashMap<Integer, Cluster> D1P = kmeans.parallelKMeans(cities, k, iter, cutoff);
                double timeD1P = System.currentTimeMillis() - startD1P;
                parallelTimeD1.add(timeD1P);
            }
            double sum = 0;
            for(int i=0; i<serialTimeD1.size(); i++){
                sum = sum + (serialTimeD1.get(i) / parallelTimeD1.get(i));
                System.out.println("Speed up: "+numero_citta.get(i)+"\t"+serialTimeD1.get(i)/parallelTimeD1.get(i));
            }
            double speedUp = sum/serialTimeD1.size();
            System.out.println("SpeedUp: " + speedUp);

            stampaTerminale("Domanda 1: variare del numero di città", serialTimeD1, parallelTimeD1);
            stampaGrafico("Domanda 1", "Numero di città", serialTimeD1, parallelTimeD1, numero_citta);


            // DOMANDA 2
            ArrayList<Double> serialTimeD2 = new ArrayList<Double>();
            ArrayList<Double> parallelTimeD2 = new ArrayList<Double>();

            ArrayList<Double> numero_cluster = new ArrayList<Double>();

            for (int kappa=10; kappa <101; kappa++) {
                numero_cluster.add((double)kappa);
                // Seriale
                double startD2S = System.currentTimeMillis();
                Map<Integer, Cluster> D2S = kmeans.serialKMeans(citiesList, kappa, iter);
                double timeD2S = System.currentTimeMillis() - startD2S;
                serialTimeD2.add(timeD2S);

                // Parallelo
                double startD2P = System.currentTimeMillis();
                ConcurrentHashMap<Integer, Cluster> D2P = kmeans.parallelKMeans(citiesList, kappa, iter, cutoff);
                double timeD2P = System.currentTimeMillis() - startD2P;
                parallelTimeD2.add(timeD2P);
            }
            sum=0;
            for(int i=0; i<serialTimeD2.size(); i++){
                sum = sum + (serialTimeD2.get(i) / parallelTimeD2.get(i));
                System.out.println("Speed up: "+numero_cluster.get(i)+"\t"+serialTimeD2.get(i)/parallelTimeD2.get(i));
            }
            speedUp = sum/serialTimeD2.size();
            System.out.println("SpeedUp: " + speedUp);

            stampaTerminale("Domanda 2: variare del numero di cluster", serialTimeD2, parallelTimeD2);
            stampaGrafico("Domanda 2", "Numero di cluster", serialTimeD2, parallelTimeD2, numero_cluster);


            // DOMANDA 3
            ArrayList<Double> serialTimeD3 = new ArrayList<Double>();
            ArrayList<Double> parallelTimeD3 = new ArrayList<Double>();
            ArrayList<Double> numero_iterazioni = new ArrayList<Double>();

            for (int iterazioni=10;  iterazioni<1000; iterazioni+=10) {
                numero_iterazioni.add((double)iterazioni);

                // Seriale
                double startD3S = System.currentTimeMillis();
                Map<Integer, Cluster> D3S = kmeans.serialKMeans(citiesList, k, iterazioni);
                double timeD3S = System.currentTimeMillis() - startD3S;
                serialTimeD3.add(timeD3S);

                // Parallelo
                double startD3P = System.currentTimeMillis();
                ConcurrentHashMap<Integer, Cluster> D3P = kmeans.parallelKMeans(citiesList, k, iterazioni, cutoff);
                double timeD3P = System.currentTimeMillis() - startD3P;
                parallelTimeD3.add(timeD3P);
            }

            sum=0;
            for(int i=0; i<serialTimeD3.size(); i++){
                sum = sum + (serialTimeD3.get(i) / parallelTimeD3.get(i));
                System.out.println("Speed up: "+(int)((i*10)+10) +"\t"+serialTimeD3.get(i)/parallelTimeD3.get(i));
            }
            speedUp = sum/serialTimeD3.size();
            System.out.println("SpeedUp: " + speedUp);
            stampaTerminale("Domanda 3: variare del numero di iterazioni", serialTimeD3, parallelTimeD3);
            stampaGrafico("Domanda 3", "Numero di iterazioni", serialTimeD3, parallelTimeD3, numero_iterazioni);


            // DOMANDA 4
            ArrayList<Integer> arrayCutoff = new ArrayList<Integer>();
            arrayCutoff.add(2);
            arrayCutoff.add(5);
            arrayCutoff.add(10);
            arrayCutoff.add(20);
            arrayCutoff.add(30);
            arrayCutoff.add(40);
            arrayCutoff.add(50);
            arrayCutoff.add(60);
            arrayCutoff.add(70);
            arrayCutoff.add(80);
            arrayCutoff.add(90);
            arrayCutoff.add(100);
            arrayCutoff.add(150);
            arrayCutoff.add(200);
            arrayCutoff.add(250);
            arrayCutoff.add(300);

            ArrayList<Double> parallelTimeD4 = new ArrayList<Double>();
            ArrayList<Double> numero_cutoff = new ArrayList<Double>();

            for (int co=0;  co<arrayCutoff.size(); co++) {
                numero_cutoff.add((double)cutoff);

                // Parallelo
                double startD4P = System.currentTimeMillis();
                ConcurrentHashMap<Integer, Cluster> D3P = kmeans.parallelKMeans(citiesList, k, iter, arrayCutoff.get(co));
                double timeD4P = System.currentTimeMillis() - startD4P;
                parallelTimeD4.add(timeD4P);
            }

            System.out.println("\n\n~~~~ Domanda 4: variare del cutoff");
            System.out.print("KMeans parallelo: \n\t");
            for (double time: parallelTimeD4) {
                System.out.print(time + " ");
            }

            double[] yDataD=new double[parallelTimeD4.size()];
            for(int i=0; i< parallelTimeD4.size(); i++) {
                yDataD[i] = parallelTimeD4.get(i);
            }
            double[] xData=new double[arrayCutoff.size()];
            for(int i=0; i< arrayCutoff.size(); i++) {
                xData[i] = arrayCutoff.get(i);
            }

            // Create Chart
            XYChart chart = new XYChartBuilder().width(800).height(600).title("Doamnda 4").xAxisTitle("Cutoff").yAxisTitle("Tempo di esecuzione in ms").build();
            chart.addSeries("Parallelo", xData, yDataD);
            // Show it
            new SwingWrapper(chart).displayChart();

            // Save it
            try {
                BitmapEncoder.saveBitmap(chart, "./Domanda 4", BitmapEncoder.BitmapFormat.PNG);
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
        catch(Exception e) {
            System.out.println(e);
        }

    }
}

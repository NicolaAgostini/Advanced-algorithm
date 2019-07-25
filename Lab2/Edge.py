class Edge:
    def __init__(self, departure_time, arrival_time, run_id, id_line, id_departure_station, id_arrival_station):
        """
        :param departure_time: quando parte la corsa
        :param arrival_time: quando arriva la corsa
        :param run_id: identificativo della corsa
        :param id_line: identificativo della linea
        :param id_departure_station: identificativo della stazione di partenza
        :param id_arrival_station: identificativo della stazione di arrivo
        """
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.run_id = run_id
        self.id_line = id_line
        self.id_departure_station = id_departure_station
        self.id_arrival_station = id_arrival_station

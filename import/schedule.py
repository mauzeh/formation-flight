import os
import csv
from airports import get_airports

class Flight(object):
    """Represents a flight.

    @todo merge with geo lib"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))
        
    def csv(self):
        return [
            self.departure_time,
            '%s%s' % (self.airline,self.flight_number),
            '%s-%s' % (self.origin, self.destination),
            self.equipment
        ]

airports = get_airports()

if __name__ == "__main__":
    
    fn = os.path.join(os.path.dirname(__file__), 'data/flights.tsv')
    reader = csv.reader(open(fn), delimiter = "\t")
    fn = os.path.join(os.path.dirname(__file__), '../data/flights.tsv')
    writer = csv.writer(open(fn, 'wb'), delimiter = '\t',
                        quotechar = '"')
    flights = []
    airports_used = []
    for row in reader:

        # Discard dummy rows
        if len(row) < 15: continue

        flight = Flight(
            origin         = row[3],
            destination    = row[4],
            airline        = row[2],
            flight_number  = row[6],
            equipment      = row[8],
            departure_time = row[12], # LT, to be converted to z
            operating_days = row[15]
        )

        try:
            flight.origin = airports[flight.origin]
            flight.destination = airports[flight.destination]
        except KeyError:
            continue

        # Discard flights not operating on Thursday
        if flight.operating_days[3] != '4':
            continue

        # Discard flights not going to North America
        if flight.destination.continent != 'North America':
            continue

        # Temp to verify filter
        #if flight.origin.code != 'AMS' or flight.destination.code != 'JFK':
            #continue

        # Assemble all airports used in this selection of flights to minimize
        # redundant waypoints in the database
        if flight.origin not in airports_used:
            airports_used.append(flight.origin)
        if flight.destination not in airports_used:
            airports_used.append(flight.destination)

        # Calibrate departure time to UTC
        flight.departure_time = int(flight.departure_time[0:2])*60 + int(flight.departure_time[2:4])
        flight.departure_time = flight.departure_time - int(flight.origin.gmt_offset) * 60

        flights.append(flight)

        writer.writerow(flight.csv())

    fn = os.path.join(os.path.dirname(__file__), '../data/airports.tsv')
    writer = csv.writer(open(fn, 'wb'), delimiter = '\t',
                        quotechar = '"')
    for airport in airports_used:
        writer.writerow(airport.csv())

    #print flights
    print 'done... %d flights found!' % len(flights)
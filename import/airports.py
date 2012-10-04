import os
import csv

class Airport(object):
    """Represents an airport.

    @todo merge with geo lib"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def csv(self):
        return [self.code, self.lat, self.lon]

    def __repr__(self):
        return self.code
        #keys = sorted(self.__dict__)
        #items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        #return "{}({})".format(type(self).__name__, ", ".join(items))

def get_airports():

    # First populate a list with GMT offsets and merge it later
    fn = os.path.join(os.path.dirname(__file__), 'data/gmt_offsets.csv')
    reader = csv.reader(open(fn))
    gmt_offsets = {}
    for row in reader:
        if len(row[0].strip()) == 0:
            continue
        gmt_offsets[row[0]] = row[1]

    # Then get all the airports
    fn = os.path.join(os.path.dirname(__file__), 'data/airports.csv')
    reader = csv.reader(open(fn))
    airports = {}
    for row in reader:

        try:
            gmt_offset = gmt_offsets[row[0]]
        except KeyError:
            continue

        airport = Airport(
            code = row[0],
            name = row[1],
            lat = row[5],
            lon = row[6],
            gmt_offset = gmt_offset,
            continent = row[9]
        )

        airports[airport.code] = airport

    return airports
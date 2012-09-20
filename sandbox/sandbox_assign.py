"""
Tests the assignment algorithm.

Assignment algorithm: find all flights that arrive at the virtual hub within a 
certain time window of each other and group them by maximizing the available 
slack.
"""
from lib.intervals import Interval,group

if __name__ == '__main__':

    print group([
        Interval('G', 0, 2),
        Interval('B', 2, 4),
        Interval('C', 1, 3),
        Interval('D', 3, 5),
        Interval('A', 1, 3),
        Interval('E', 4, 6),
        Interval('F', 2, 4),
    ])
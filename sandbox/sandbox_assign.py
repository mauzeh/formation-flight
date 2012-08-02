"""
Tests the assignment algorithm.

Assignment algorithm: find all flights that arrive at the virtual hub within a certain time window of each other and
group them by maximizing the available slack.
"""

import copy

class Interval:
    """
    An interval that needs to be grouped
    """
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def is_within(self, interval):
        """
        Determine if the interval overlaps with the current one.
        """
        if(self.start >= interval.start) & (self.start <= interval.end):
        #            print 'Yes because start is within interval'
            return True
        if(self.end >= interval.start) & (self.end <= interval.end):
        #            print 'Yes because end is within interval (end: %s, interval: %s)' % (self.end, interval)
            return True

        return False

    def __repr__(self):
        #return '%s (%s ~ %s)' % (self.name, self.start, self.end)
        return self.name

class Group:
    """
    A group of intervals
    """
    def __init__(self):
        self.intervals = []

    def contains(self, interval):
        for candidate in self.intervals:
            if interval == candidate: return True
        return False

    def __len__(self):
        return len(self.intervals)

    def __repr__(self):
        return self.intervals.__repr__() + '\n'

def filter(intervals):
    """Filter out any intervals that do not overlap with the first one in the list"""

    test_interval = intervals[0]
    candidates_by_start = []
    candidates_by_end = []

    for interval in intervals:
        # exact match: add to lower bound
        if (interval.start == test_interval.start) & (interval.end == test_interval.end):
            candidates_by_start.append(interval)
            continue
            # lower bound match
        if (interval.start > test_interval.start) & (interval.start < test_interval.end):
            candidates_by_start.append(interval)
            continue
            # upper bound match
        if (interval.end < test_interval.end) & (interval.end > test_interval.start):
            candidates_by_end.append(interval)
            continue

    return candidates_by_start + candidates_by_end

def group_intervals(intervals):

    grouped_intervals = []

    for i in range(0, len(intervals)):

        candidates = copy.deepcopy(intervals)

        # Put this interval at the beginning of the list
        candidates.pop(i)
        candidates.insert(0, intervals[i])

        group = Group()

        while len(candidates) > 0:
            filtered_intervals = filter(candidates)
            group.intervals.append(filtered_intervals)
            candidates = list(set(candidates) - set(filtered_intervals))

        grouped_intervals.append(group)

    return grouped_intervals

if __name__ == '__main__':

#    print filter([
#        Interval('G', 0, 2),
#        Interval('A', 1, 3),
#        Interval('B', 2, 4),
#        Interval('C', 1, 3),
#        Interval('D', 3, 5),
#        Interval('E', 4, 6),
#        Interval('F', 2, 4),
#    ])
#
#    print filter([
#        Interval('B', 2, 4),
#        Interval('D', 3, 5),
#        Interval('E', 4, 6),
#        Interval('F', 2, 4),
#    ])

    print group_intervals([
       Interval('A', 1, 3),
       Interval('B', 2, 4),
       Interval('C', 1, 3),
       Interval('D', 3, 5),
       Interval('E', 4, 6),
       Interval('F', 2, 4),
       Interval('G', 0, 2),
    ])

    print group_intervals([
        Interval('D', 3, 5),
        Interval('C', 1, 3),
        Interval('A', 1, 3),
        Interval('G', 0, 2),
        Interval('B', 2, 4),
        Interval('E', 4, 6),
        Interval('F', 2, 4),
    ])
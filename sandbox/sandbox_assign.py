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

    def get_slack(self):
        """
        Return an interval containing the overlap of all member intervals.
        """
        # This is the main interval
        first_interval = self.intervals[0]

        # The biggest slack would equal the first interval
        slack = Interval('Slack', first_interval.start, first_interval.end)

        # first do the intervals whose lower bound falls in the main interval
        for interval in self.intervals:
            print interval
            if interval.start > slack.start:
                slack.start = max(slack.start, interval.start)
                print slack

        # first do the intervals whose upper bound falls in the main interval
        for interval in self.intervals:
            print interval
            if interval.end < slack.end:
                slack.end = min(slack.end, interval.end)
                print slack

        assert slack.start <= slack.end, 'Invalid slack: start should be lower than end'

        return slack


    def __repr__(self):
        return self.intervals.__repr__()

def generate_sets(intervals, sets):

    print 'Received intervals: %s' % intervals
    print 'Received sets: %s' % sets

    for interval in intervals:

        print 'working on interval %s'%interval

        for set in sets:

            # Skip if already contains
            if(set.contains(interval)):
                continue

            copy_set = copy.deepcopy(set)
            slack = copy_set.get_slack()

            if interval.is_within(slack):
                print 'Yes, we can add %s to set %s' % (interval, set)
                copy_set.intervals.append(interval)
                sets.append(copy_set)
    return sets

if __name__ == '__main__':

    intervals = []
    intervals.append(Interval('A', 0, 4))
    intervals.append(Interval('B', 1, 5))
    intervals.append(Interval('C', 2, 6))
    intervals.append(Interval('D', -1, 3))
    intervals.append(Interval('E', -2, 1))
    intervals.append(Interval('F', -2, 0))

    interval = intervals[0]
    candidates_by_start = []
    candidates_by_end = []

    # Filter out any intervals that do not overlap at all
    for other_interval in intervals:
        if (other_interval.start >= interval.start) & (other_interval.start <= interval.end):
            print 'lower bound match: %s fits within %s' % (other_interval, interval)
            candidates_by_start.append(other_interval)
            continue
        if (other_interval.end <= interval.end) & (other_interval.end >= interval.start):
            print 'upper bound match: %s fits within %s' % (other_interval, interval)
            candidates_by_end.append(other_interval)
            continue

    candidates = Group()
    candidates.intervals = sorted(candidates_by_start, key = lambda interval: interval.start) +\
                           sorted(candidates_by_end,   key = lambda interval: interval.end, reverse = True)

    print 'candidates are %s' % candidates

    # Create sets of intervals where all intervals overlap each other as well, not just
    # our primary interval
    first_set = Group()
    first_set.intervals.append(intervals[0])

    print generate_sets(candidates.intervals, [first_set])


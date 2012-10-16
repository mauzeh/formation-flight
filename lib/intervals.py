"""Contains mechanisms to group intervals if they overlap."""

class Interval:
    """
    A time window that is used to group flights arriving at about the same time.
    """
    def __init__(self, obj, start, end):
        assert start <= end
        self.obj = obj
        self.start = start
        self.end = end

    def __repr__(self):
        return '%s (%s ~ %s)' % (self.obj, self.start, self.end)
        #return self.name

def group(intervals):
    """
    Groups intervals according to their overlap. Does not yield an optimum yet.
    """
    intervals = sorted(intervals, key = lambda interval: interval.start)
    if(len(intervals) == 0): return []
    solution = []
    candidates = intervals
    for i in range(0, len(candidates)):
        if candidates[i].start <= candidates[0].end:
            solution.append(candidates[i])
    return [solution] + group(list(set(candidates) - set(solution)))

if __name__ == "__main__":
    print group([
        Interval('G', 0, 2),
        Interval('B', 4, 4),
        Interval('C', 1, 3),
        Interval('D', 3, 5),
        Interval('A', 1, 3),
        Interval('E', 4, 6),
        Interval('F', 2, 4),
    ])

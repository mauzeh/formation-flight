import copy

class Interval:
    """
    An interval that needs to be grouped
    """
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def __repr__(self):
        return '%s (%s ~ %s)' % (self.name, self.start, self.end)
        #return self.name

def group(intervals):
    """
    Groups intervals according to their overlap. Does not yield an optimum yet,
    try it out with:
    print group([
        Interval('G', 0, 2),
        Interval('B', 2, 4),
        Interval('C', 1, 3),
        Interval('D', 3, 5),
        Interval('A', 1, 3),
        Interval('E', 4, 6),
        Interval('F', 2, 4),
    ])
    """
    intervals = sorted(intervals, key = lambda interval: interval.start)
    if(len(intervals) == 0): return []
    solution = []
    candidates = copy.deepcopy(intervals)
    for i in range(0, len(candidates)):
        if candidates[i].start < candidates[0].end:
            solution.append(candidates[i])
    return [solution] + group(list(set(candidates) - set(solution)))
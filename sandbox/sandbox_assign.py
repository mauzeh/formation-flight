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

def get_winning_combination(candidate_sets):

    candidate_sets = generate_combinations(candidate_sets)

    solutions = []

    for candidates in candidate_sets:
        results = filter(candidates)
        remaining = list(set(candidates) - set(results))
        solutions.append([results, remaining])

    # Challenge: which one is the "best"? For now, let's take the
    # one with the least elements in remaining as best. If there are multiple
    # winners, we take the first winner in the list as best.
    best_solution = solutions[0]
    for solution in solutions:
        if len(solution[1]) > len(best_solution[1]):
            best_solution = solution

    return best_solution

def generate_combinations(intervals):

    combinations = []

    for i in range(0, len(intervals)):

        combination = copy.deepcopy(intervals)
        combination.insert(0, combination.pop(i))
        combinations.append(combination)

    return combinations


def group(intervals):
    winner, left = get_winning_combination(intervals)
    if len(left) == 0:
        return winner
    else :
        return [winner] + [group(left)]

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

    print group([
        Interval('G', 0, 2),
        Interval('C', 1, 3),
        Interval('A', 1, 3),
        Interval('B', 2, 4),
        Interval('E', 4, 6),
        Interval('D', 3, 5),
        Interval('F', 2, 4),
    ])

    print group([
        Interval('A', 1, 3),
        Interval('B', 2, 4),
        Interval('C', 1, 3),
        Interval('D', 3, 5),
        Interval('E', 4, 6),
        Interval('F', 2, 4),
        Interval('G', 0, 2),
    ])

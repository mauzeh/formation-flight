"""From a list of objects, finds the object having the lowest value"""

class Getal(object):
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return str(self.val)

items = [Getal(2), Getal(3), Getal(1), Getal(7)]

def lowest(winner, item): 
    return item if item.val < winner.val else winner

print reduce(lowest, items)
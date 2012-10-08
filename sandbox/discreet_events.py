import random

time = 0
events = []

class SimObject(object):
    def __init__(self, label):
        self.label = label
    def __repr__(self):
        return self.label

class Customer(SimObject):

    def __init__(self, label):
        self.label = label

    def arrive(self, event):
        self.arrival_time = event.time
        print 'time = %d. %s just arrived' % (event.time, self)

    def start(self, event):
        print 'time = %d. %s waited %d to get service' %\
              (event.time, self, event.time - self.arrival_time)
    def end(self, event):
        print 'time = %d. %s left' % (event.time, event.sender)

class Server(SimObject):

    def __init__(self, label):
        self.label = label
        self.busy = False

    def start(self):
        self.busy = True

    def end(self):
        self.busy = False

    def get_service_time(self):
        return random.choice([2,5,6])

class Assigner(object):
    
    def __init__(self):
        self.server = Server('Anita')
        self.locked = False
        self.customers = []
        
    def handle_arrival(self, event):

        customer = event.sender
        self.customers.append(customer)

        if self.server.busy or self.locked:
            return

        # If we have one assignment done, lock the assigner to prevent
        # simultaneous arrivals to generate multiple "start" events.
        self.locked = True
        
        global time
        events.append(Event('customer-start-service', customer, time))

    def handle_start(self, event):

        customer = event.sender 
        
        assert not self.server.busy
        self.server.start()
        global time
        end_time = time + self.server.get_service_time()
        events.append(Event('customer-end-service', customer, end_time))

    def handle_end(self, event):

        # We are free to start assigning again!
        self.locked = False
        
        customer = event.sender
        self.server.end()
        index = self.customers.index(customer)
        del self.customers[index]

        if len(self.customers) == 0:
            print 'time = %d. Done with queue' % event.time
            return

        global time
        next_customer = self.customers[0]
        events.append(Event('customer-start-service', next_customer, time)) 

class Event(object):
    
    def __init__(self, label, sender, bubble_time = 0):

        global time
        assert bubble_time >= time
        
        self.label = label
        self.sender = sender
        self.time = bubble_time
        
    def __repr__(self):
        return self.label
        
    def __cmp__(self, other):
        """Allows for easy retrieval of earliest elements (having min(time))"""
        return cmp(self.time, other.time)

class Dispatcher(object):

    def __init__(self):
        self.listeners = {}

    def register(self, event_label, listener):
        if event_label not in self.listeners:
            self.listeners[event_label] = []
        self.listeners[event_label].append(listener)

    def bubble(self, event):
        if event.label not in self.listeners:
            return
        for listener in self.listeners[event.label]:
            listener(event)
            
class CustomerHandler(object):
    
    def handle_arrival(self, event):
        customer = event.sender
        customer.arrive(event)
        
    def handle_start(self, event):
        customer = event.sender
        customer.start(event)
        
    def handle_end(self, event):
        customer = event.sender
        customer.end(event)
            
customers = [
    Customer('Maurits'),
    Customer('Joep'),
    Customer('Nick'),
    Customer('Bart')
]

events.append(Event('customer-arrive', customers[0], 0))
events.append(Event('customer-arrive', customers[1], 2))
events.append(Event('customer-arrive', customers[1], 9))
events.append(Event('customer-arrive', customers[3], 9))

customer_handler = CustomerHandler()
assigner         = Assigner()

dispatcher = Dispatcher()
dispatcher.register('customer-arrive', customer_handler.handle_arrival)
dispatcher.register('customer-arrive', assigner.handle_arrival)
dispatcher.register('customer-start-service', customer_handler.handle_start)
dispatcher.register('customer-start-service', assigner.handle_start)
dispatcher.register('customer-end-service', customer_handler.handle_end)
dispatcher.register('customer-end-service', assigner.handle_end)

while len(events) > 0:
    event = min(events)
    key = events.index(event)
    del events[key]
    time = event.time
    dispatcher.bubble(event)

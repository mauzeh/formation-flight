import config
from lib.geo.segment import Segment
from lib import sim, debug
from lib.debug import print_line as p

vars = {}
runs = 0.
aircraft_success = []

def init():
    
    global runs, aircraft_success

    sim.dispatcher.register('aircraft-depart', handle_depart)
    sim.dispatcher.register('formation-alive', handle_alive)
    sim.dispatcher.register('aircraft-arrive', handle_arrive)
    
    runs = runs + 1.
    aircraft_success = []

def handle_depart(event):
    
    aircraft = event.sender
    
    if aircraft.label not in vars:
        vars[aircraft.label] = 0

def handle_alive(event):
    
    global vars, runs

    formation = event.sender
    
    for aircraft in formation:
        aircraft_success.append(aircraft)
        
def handle_arrive(event):
    
    aircraft = event.sender
    
    global planes, runs, aircraft_success
    
    if aircraft in aircraft_success:
        # Increment amount of times in formation and update with new runs
        vars[aircraft.label] = ((runs - 1) * vars[aircraft.label] + 1.) / runs
    else:
        # Only adjust average to new amount of runs
        vars[aircraft.label] = ((runs - 1) * vars[aircraft.label]) / runs


import config
from lib.geo.segment import Segment
from lib import sim, debug
from lib.debug import print_line as p
from lib.geo.util import get_fuel_burned_during_cruise

vars = {}
hubs = []

def init():
    global vars, hubs
    vars = {}
    hubs = []
    sim.dispatcher.register('sim-start',       handle_start)
    sim.dispatcher.register('aircraft-depart', handle_depart)
    sim.dispatcher.register('formation-alive', handle_alive)
    sim.dispatcher.register('aircraft-arrive', handle_arrive)
    sim.dispatcher.register('sim-finish',      handle_finish)

def handle_start(event):
    global vars
    vars['sim_start'] = int(event.time)

def handle_depart(event):
    global vars, hubs

    aircraft = event.sender

    if 'aircraft_count' not in vars:
        vars['aircraft_count'] = 0
    vars['aircraft_count'] += 1
    
    # If a hub was planned
    hub = aircraft.route.waypoints[0]
    if True:
        if hub not in hubs:
            hubs.append(hub)

def handle_alive(event):
    global vars

    formation = event.sender
    
    # We should have a hookoff point for each participant, and it should be
    # the current segment
    for aircraft in formation:
        assert aircraft.hookoff_point
        # The remaining segment should be hookoff-destination
        #debug.print_object(aircraft)
        assert len(aircraft.route.segments) > 0

        # Let the aircraft know in which formation it belongs
        aircraft.formation = formation

        #assert aircraft.route.segments[0].end.coincides(
        #    aircraft.hookoff_point
        #)
    
    if "formation_count" not in vars:
        vars["formation_count"] = 0
    vars["formation_count"] += 1

    if 'formation_aircraft_count' not in vars:
        vars['formation_aircraft_count'] = 0
    vars['formation_aircraft_count'] += len(formation)
        
    for aircraft in formation:
        if 'Q_sum' not in vars:
            vars['Q_sum'] = 0
        vars['Q_sum']   = vars['Q_sum'] + aircraft.Q

    #hub_key = 'formation_count_%s' % formation.hub
    #if hub_key not in vars:
    #    vars[hub_key] = 0
    #vars[hub_key] += 1
    
def handle_arrive(event):
    global vars, hubs

    aircraft = event.sender
    hub = aircraft.hub
    
    assert hub in hubs

    aircraft = event.sender
    hub = aircraft.hub
    p('Flight %s arrives at hub %s' % (
        aircraft, hub
    ))
    assert hub in hubs
    #key = 'flight_count_%s' % hub
    #if key not in vars:
    #    vars[key] = 0
    #vars[key] = vars[key] + 1

    if 'distance_formation' not in vars:
        vars['distance_formation'] = 0
    if 'distance_solo' not in vars:
        vars['distance_solo'] = 0
    if 'distance_direct' not in vars:
        vars['distance_direct'] = 0
    if 'fuel_actual' not in vars:
        vars['fuel_actual'] = 0
    if 'fuel_direct' not in vars:
        vars['fuel_direct'] = 0

    # Aircraft always fly solo to the hub
    segment = Segment(aircraft.origin, hub)
    origin_to_hub = segment.get_length()
    p('Distance origin_to_hub for %s is %dNM' % (
        aircraft,
        origin_to_hub
    ))
    vars['distance_solo'] += origin_to_hub

    # If in formation
    if hasattr(aircraft, 'formation'):

        segment = Segment(hub, aircraft.hookoff_point)
        hub_to_hookoff = segment.get_length()
        p('Distance hub_to_hookoff for %s is %dNM' % (
            aircraft,
            hub_to_hookoff
        ))
        vars['distance_formation'] += hub_to_hookoff

        segment = Segment(aircraft.hookoff_point, aircraft.destination)
        hookoff_to_destination = segment.get_length()
        p('Distance hookoff_to_destination for %s is %dNM' % (
            aircraft,
            hookoff_to_destination
        ))
        vars['distance_solo'] += hookoff_to_destination

        # Collect all hub delays
        # The calibration aircraft was never delayed
        if hasattr(aircraft, 'hub_delay'):
            if 'hub_delay_sum' not in vars:
                vars['hub_delay_sum'] = 0
            vars['hub_delay_sum'] = vars['hub_delay_sum'] +\
                aircraft.hub_delay

        # @todo first aircraft has no discount
        discount = 1 - config.alpha
        vars['fuel_actual'] = vars['fuel_actual'] +\
            get_fuel_burned_during_cruise(
                origin_to_hub +\
                discount * hub_to_hookoff +\
                hookoff_to_destination
            )

    # If fully solo
    else:
        
        segment = Segment(hub, aircraft.destination)
        hub_to_destination = segment.get_length()
        p('Distance hub_to_destination for %s is %dNM' % (
            aircraft,
            hub_to_destination
        ))
        vars['distance_solo'] += hub_to_destination
        
        vars['fuel_actual'] = vars['fuel_actual'] +\
            get_fuel_burned_during_cruise(
                origin_to_hub + hub_to_destination
            )
        
    # Also calculate the direct distance
    segment = Segment(aircraft.origin, aircraft.destination)
    direct = segment.get_length()
    p('Distance direct for %s is %dNM' % (
        aircraft,
        direct
    ))
    vars['distance_direct'] = vars['distance_direct'] + direct
    vars['fuel_direct'] = vars['fuel_direct'] +\
        get_fuel_burned_during_cruise(
            direct
        )

def handle_finish(event):

    global vars

    vars['sim_finish'] = int(event.time)
    if 'Q_sum' in vars:
        vars['Q_avg'] = vars['Q_sum'] / vars['formation_aircraft_count']
    if 'formation_aircraft_count' in vars:
        vars['formation_success_rate'] = \
            vars['formation_aircraft_count'] /\
            float(vars['aircraft_count'])
        vars['avg_formation_size'] = \
            vars['formation_aircraft_count'] /\
            float(vars['formation_count'])
        vars['distance_total'] = \
            vars['distance_formation'] + vars['distance_solo']
        vars['distance_success_rate'] = \
            vars['distance_formation'] / vars['distance_total']
        vars['distance_penalty'] = -1 + \
            vars['distance_total'] / vars['distance_direct']
        vars['alpha_effective'] =\
            config.alpha *\
            vars['distance_success_rate'] -\
            vars['distance_penalty']
        vars['hub_delay_avg'] = vars['hub_delay_sum'] /\
            vars['formation_aircraft_count']
        
        # estimate hub delay fuel
        fuel_per_minute = 150
        
        vars['fuel_delay'] = vars['hub_delay_avg'] * 152 * (
            vars['formation_aircraft_count'] - vars['formation_count']
        )
        vars['fuel_saved'] = 1 -\
            (vars['fuel_actual'] + vars['fuel_delay']) / vars['fuel_direct']
        vars['fuel_saved_disregard_delay'] = 1 -\
            (vars['fuel_actual']) / vars['fuel_direct']

    vars['config_alpha']      = config.alpha
    vars['config_etah_slack'] = config.etah_slack
    vars['config_lock_time']  = config.lock_time
    vars['config_phi_max']    = config.phi_max
    vars['config_count_hubs'] = config.count_hubs
    vars['config_Z']          = config.Z
    vars['config_dt']         = config.dt

    #debug.print_dictionary(vars)

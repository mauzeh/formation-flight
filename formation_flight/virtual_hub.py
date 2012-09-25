from pydispatch import dispatcher

def register():
    dispatcher.connect(handle)

def handle(signal, sender, data = None, time = 0):

    #if not hasattr(handle, "assigner"):
        #handle.assigner = Assigner()

    #if signal is 'fly':
        #print 'flyyyyyyyyyyyy!'
        #handle.assigner.lock_formations(signal, sender, data, time)
    if signal is 'takeoff':
        print 'taaaaaaaaaake off'
        #handle.assigner.register_takeoff(signal, sender, data, time)
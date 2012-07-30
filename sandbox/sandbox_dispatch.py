from pydispatch import dispatcher

class EventBootstrapper:

    def handle(self, signal, sender, message = None):
        print '+----------------------------------------------+'
        print '| %s :: %s' % (sender.__class__.__name__, signal)
        print '| Attached message: %s' % message
        print '+----------------------------------------------+'

class BeanGrinder(object):

    def grind(self):
        dispatcher.send('start', sender = self, message = {'yeah': 'uhuh'})
        pass

class CoffeeMaker(object):

    def brew_coffee(self):
        grinder = BeanGrinder()
        grinder.grind()
        dispatcher.send('start', sender = self, message = [])

if __name__ == "__main__":

    handler = EventBootstrapper()
    dispatcher.connect(handler.handle)

    maker = CoffeeMaker()
    maker.brew_coffee()

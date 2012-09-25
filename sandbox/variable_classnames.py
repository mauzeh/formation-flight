class A(object):
	def __init__(self, param):
		print 'This is A with param %d' % param
	def foo(self):
		print "foo"

class B(object):
	def __init__(self, param):
		print 'This is B'
	def foo(self):
		print "bar"

def getObject(classname):
	obj = globals()[classname]
	return obj(65)

myobject = getObject('A')
myobject.foo()

print '-'*80

a = A(55)
a.foo()

print '-'*80

myobject = getObject('B')
myobject.foo()

print '-'*80

b = B(44)
b.foo()

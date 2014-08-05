from ImplementedClass import ImplementedClass

def implemented_instance():
	return ImplementedClass(
		visible = 'visible',
		virtual = 'virtual',
		list = [],
		read_only = 'read_only',
		not_implemented = 'not_implemented',
		is_dirty = 'True'
	)

def test_bad_init():
	try:
		ImplementedClass(
			__cache__ = {}
		)
		success = False
	except AttributeError:
		success = True
	assert success == True

def test_bad_dirty():
	a = implemented_instance()
	try:
		a.__cache__ = {}
		success = False
	except AttributeError:
		success = True
	try:
		a.__cache__
		success = False
	except AttributeError:
		success = True
	assert success == True

def test_init():
	a = implemented_instance()
	assert a.visible == 'visible'
	assert a.virtual == 'virtual'
	assert a.list == []
	assert a.is_dirty == False

def test_dirty():
	a = implemented_instance()
	assert a.is_dirty == False
	a.new_variable = None
	assert a.is_dirty == True
	a.save()
	assert a.is_dirty == False

	a.visible = 'new_visible'
	assert a.is_dirty == True
	a.save()
	a.virtual = 'new_virtual'
	assert a.is_dirty == True
	a.save()
	a.list.append(0)
	assert a.is_dirty == True
	assert a.visible == 'new_visible'
	assert a.virtual == 'new_virtual'
	assert a.list == [0]

# test caching behavior -- this is NOT guaranteed to be the same behavior over different releases
# this also demonstrates INCORRECT USAGE of the package,
#	but is necessary to test for the expected behavior of the CURRENT release
def test_cache():
	a = implemented_instance()
	set(a.__dict__['__cache__'].keys()) == set([])
	a.list
	a.virtual
	# virtual fields will set both the __dict__ name AND the associated @property name
	assert set(a.__dict__['__cache__'].keys()) == set(['list', 'virtual', '_virtual_'])
	a.save()
	assert set(a.__dict__['__cache__'].keys()) == set([])
	a.list
	a.visible
	a.new_variable = None
	a.virtual
	# cache keys will be added ONLY if __is_dirty__ is not yet set
	assert set(a.__dict__['__cache__'].keys()) == set(['list', 'visible'])

if __name__ == '__main__':
	test_init()
	test_bad_init()
	test_dirty()
	test_bad_dirty()
	test_cache()

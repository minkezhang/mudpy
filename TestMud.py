from BakedPie import BakedPie

def implemented_instance():
	return BakedPie(
		# these fields will set upon initialization
		visible = 'visible',
		virtual = 'virtual',
		list = [],
		# these following fields will be ignored completely
		read_only = 'read_only',
		not_implemented = 'not_implemented',
		is_dirty = True
	)

# attempting to alter reserved keyword upon init results in a thrown exception
def test_bad_init():
	try:
		BakedPie(
			__cache__ = {}
		)
		success = False
	except AttributeError:
		success = True
	assert success == True

# attemptig to get or set reserved keywords results in a thrown exception
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
	# the object is obviously clean upon initialization
	assert a.is_dirty == False
	assert a.visible == 'visible'
	assert a.virtual == 'virtual'
	assert a.list == []
	# the object has not changed, but has been read
	assert a.is_dirty == False

def test_dirty():
	a = implemented_instance()
	# added new variable to the object -- is_dirty should return True now
	a.new_variable = None
	assert a.is_dirty == True
	# saving all changes -- object should now be clean again
	a.save()
	assert a.is_dirty == False

	a.visible = 'new_visible'
	assert a.is_dirty == True
	a.save()
	a.virtual = 'new_virtual'
	assert a.is_dirty == True
	a.save()
	# the variable was READ from the object, but was change EXTERNALLY -- we should be able to detect this change
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
	# the cache itself should be empty immediately after initialization
	assert a.__dict__['__is_dirty__'] == False
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

from ApplicationClass import ApplicationClass

def application_instance():
	return ApplicationClass(
		visible = 'visible',
		virtual = 'virtual',
		list = [],
		read_only = 'read_only',
		not_implemented = 'not_implemented',
		is_dirty = 'True'
	)


def test_init():
	a = application_instance()
	assert a.visible == 'visible'
	assert a.virtual == 'virtual'
	assert a.list == []
	assert a.is_dirty == False

def test_dirty():
	a = application_instance()
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

if __name__ == '__main__':
	test_init()
	test_dirty()

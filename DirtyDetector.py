from copy import deepcopy

class DirtyDetector(object):
	def __init__(self, **kwargs):
		property_keys = [ k for k, v in self.__class__.__dict__.items() if type(v) is property ]
		for key in kwargs.keys():
			if key == '__cache__':
				raise AttributeError('__cache__ is a reserved variable')
			# only update the appropriate class var if
			#	a.) var in self.__dict__
			#	b.) var is an @property (var in self.__class__.__dict__)
			#	if var is @property, the appropriate @var.setter is called to
			#	update the object instance appropriately (if property.fset exists)
			# cf. http://bit.ly/1qO35ig
			if key in property_keys:
				# ensure the property is not read only -- there exists an X.setter for this property
				# cf. http://bit.ly/1spbmLm
				if self.__class__.__dict__[key].fset != None:
					try:
						setattr(self, key, kwargs.pop(key))
					# catch all calls which may be deprecated, unsupported, etc.
					except NotImplementedError:
						pass
			elif key in self.__dict__:
				setattr(self, key, kwargs.pop(key))
		self.__dict__['__cache__'] = deepcopy(self.__dict__)

	def __setattr__(self, k, v):
		if k == '__cache__':
			raise AttributeError('__cache__ is a reserved variable')
		super(DirtyDetector, self).__setattr__(k, v)

	@property
	def is_dirty(self):
		for k in self.__dict__:
			if k != '__cache__':
				if (k not in self.__cache__) or (self.__dict__[k] != self.__cache__[k]):
					return True
		return False

	def save(self):
		self.__dict__['__cache__'] = deepcopy(self.__dict__)

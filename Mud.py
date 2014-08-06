from copy import deepcopy

class Mud(object):
	def __init__(self, **kwargs):
		property_keys = [ k for k, v in self.__class__.__dict__.items() if type(v) is property ]
		for k in list(kwargs.keys()):
			if k in ('__cache__', '__is_dirty__'):
				raise AttributeError('%s is a reserved variable' % k)
			# only update the appropriate class var if
			#	a.) var in self.__dict__
			#	b.) var is an @property (var in self.__class__.__dict__)
			#	if var is @property, the appropriate @var.setter is called to
			#	update the object instance appropriately (if property.fset exists)
			# cf. http://bit.ly/1qO35ig
			if k in property_keys:
				# ensure the property is not read only -- there exists an X.setter for this property
				# cf. http://bit.ly/1spbmLm
				if self.__class__.__dict__[k].fset != None:
					try:
						setattr(self, k, kwargs.pop(k))
					# catch all calls which may be deprecated, unsupported, etc.
					except NotImplementedError:
						pass
			elif k in self.__dict__:
				setattr(self, k, kwargs.pop(k))

		self.__dict__['__is_dirty__'] = False
		self.__dict__['__cache__'] = {}

	def __setattr__(self, k, v):
		if k in ('__cache__', '__is_dirty__'):
			raise AttributeError('%s is a reserved variable' % k)

		# calling Derived.var = val before calling Mud.__init__
		if '__is_dirty__' not in self.__dict__:
			self.__dict__['__is_dirty__'] = False
		if '__cache__' not in self.__dict__:
			self.__dict__['__cache__'] = {}

		# adding to the cache only if __is_dirty__ is not yet set
		if not self.__dict__['__is_dirty__']:
			# new variables
			if (k not in self.__dict__) and (k not in [ key for key, val in self.__class__.__dict__.items() if type(val) is property ]):
				self.__dict__['__is_dirty__'] = True
			# only add an entry to the cache if the property already exists
			elif k not in self.__dict__['__cache__']:
				self.__dict__['__cache__'][k] = deepcopy(getattr(self, k, None))
		super(Mud, self).__setattr__(k, v)

	def __getattribute__(self, k):
		if k in ('__cache__', '__is_dirty__'):
			raise AttributeError('%s is a reserved variable' % k)

		# reserved, read-only attributes
		# backwards-compatible and auto-escapes loop when k in ('__methods__', '__members__')
		# cf. http://bit.ly/UUml3F
		if k in ('__dict__', '__methods__', '__members__', '__class__', '__bases__', '__name__', '__mro__'):
			return super(Mud, self).__getattribute__(k)

		# calling Derived.var before calling Mud.__init__
		if '__is_dirty__' not in self.__dict__:
			self.__dict__['__is_dirty__'] = False
		if '__cache__' not in self.__dict__:
			self.__dict__['__cache__'] = {}

		if not self.__dict__['__is_dirty__'] and k != 'is_dirty':
			if k not in self.__dict__['__cache__']:
				# saves a copy of the field at time of access
				self.__dict__['__cache__'][k] = deepcopy(super(Mud, self).__getattribute__(k))

		return super(Mud, self).__getattribute__(k)

	@property
	def is_dirty(self):
		# shortcut
		if self.__dict__['__is_dirty__']:
			return True

		# test current values against the values when set / get
		for k in self.__dict__:
			if k not in ('__cache__', '__is_dirty__'):
				if (k in self.__dict__['__cache__']) and (self.__dict__[k] != self.__dict__['__cache__'][k]):
					self.__dict__['__is_dirty__'] = True
					break

		return self.__dict__['__is_dirty__']

	def save(self):
		self.__dict__['__is_dirty__'] = False
		self.__dict__['__cache__'] = {}

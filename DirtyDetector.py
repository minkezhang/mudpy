from copy import deepcopy

class DirtyDetector(object):
	def __init__(self, **kwargs):
		property_keys = [ k for k, v in self.__class__.__dict__.items() if type(v) is property ]
		for key in kwargs.keys():
			if key in property_keys:
				if self.__class__.__dict__[key].fset != None:
					try:
						setattr(self, key, kwargs.pop(key))
					except NotImplementedError:
						pass
			elif key in self.__dict__:
				setattr(self, key, kwargs.pop(key))
		self.__cache__ = deepcopy(self.__dict__)

	@property
	def is_dirty(self):
		for k in self.__dict__:
			if k != '__cache__':
				if (k not in self.__cache__) or (self.__dict__[k] != self.__cache__[k]):
					return True
		return False

	def save(self):
		self.__cache__ = deepcopy(self.__dict__)

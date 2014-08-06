from Mud import Mud

# example usage
# append Mud to end of the inheritance chain:
#	class A(B, C, D, ..., Mud)
# this preserves expected super(...) behavior
class BakedPie(Mud):
	class_var = 'class_var'
	def __init__(self, **kwargs):
		self.visible = None
		self._virtual_ = None
		self.list = []
		# sets self.visible if 'visible' exist in **kwargs
		# sets self._virtual_ if '_virtual_' OR 'virtual' exists in **kwargs
		Mud.__init__(self, **kwargs)

	@property
	def virtual(self):
		return self._virtual_

	@virtual.setter
	def virtual(self, v):
		self._virtual_ = v

	# does NOT attempt to set self.read_only if 'read_only' exists in **kwargs
	@property
	def read_only(self):
		return None

	# catches the NotImplementedError and passes on
	@property
	def not_implemented(self):
		raise NotImplementedError

	@not_implemented.setter
	def not_implemented(self, v):
		raise NotImplementedError

	# write to file or other handler
	def save(self):
		# saving hook
		if self.is_dirty:
			# put other parent class saves here
			# ...

			# this line must be included to reset the cache
			Mud.save(self)

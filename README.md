MudPy
====
introspection on crack

Overview
----
One of the key aspects of programming is to write data onto the disk -- however, we do not wish to uselessly write data if it has not changed. Commonly, a `is_dirty` 
variable is employed as part of the data abstraction to mark when said data has been altered. Upon saving the data, a program can skip the disk-write portion of code if 
the `is_dirty` bit is not set.

Usage
----
Objects that inherit the `Mud` class will be able to reference a field `Mud.is_dirty` to query if the object has been changed since 
initialization.

Calling `Mud.save` will reset the `is_dirty` field to `False`.

An example usage case can be found in `BakedPie.py` (a ''cooked'' mud pie), but a barebones wrapper class is as follows:

```
from mudpy.Mud import Mud

# we're taking the joke and beating it to the ground
# note that Mud comes last in the inheritance chain to preserve expected super(...) behavior
class RawPie(..., Mud):
	# class attribute
	cook_time = None
	def __init__(self, *args, **kwargs):
		# set some instance variables
		self.filling = None

		# will attempt to set 'filling' and 'is_cooked', but not 'chef'
		Mud.__init__(self, **kwargs)

	# read-write property
	@property
	def is_cooked(self):
		# ...
		return None

	@is_cooked.setter
	def is_cooked(self, v):
		# ...
		pass

	# read-only property
	@property
	def chef(self):
		# ...
		return None

	def save(self):
		if not self.is_dirty:
			return

		# save the pie as a recipe
		# ...

		# reset self.is_dirty
		Mud.save(self)
```

**NB** Strictly speaking, `Pie.cook_time` is a class attribute and cannot be modified; `p.cook_time = ...` will simply create a new instance variable to override the 
class attribute, which is detected by `Mud.is_dirty`. See [StackOverflow](http://stackoverflow.com/questions/6475321/global-variable-python-classes) for more 
information.

Features
----
The `Mud` class will check for dirty fields as a result of @property setters, instance variables, **as well as** method changes.

Furthermore, `Mud` can be inherited by Django models (appending to the end of the list of inherited classes) and function as an (almost) drop-in conditional save 
guard, thus replacing the more conventional, but less flexible, [django-dirtyfields](https://github.com/smn/django-dirtyfields) package:

```
from django.db import models
from mudpy.Mud import Mud

class DjangoPie(models.Model, Mud):
	def __init__(self, *args, **kwargs):
		# all instance-related fields are handled by Django
		super(DjangoPie, self).__init__(*args, **kwargs)

		# for the side-effect of setting is_dirty and initializing the cache
		Mud.__init__(self)

	def save(self, *args, **kwargs):
		# self.id evaluates to False upon a new request (and so needs to be saved)
		if not self.is_dirty and self.id:
			return
		# ...
		Mud.save(self)
```

Caveats
----
The `Mud` class employs reserved variables `__cache__` and `__is_dirty__` -- undefined behavior will result if the user attempts to alter these fields manually. 
`Mud.__getattribute__` and `Mud.__setattr__` employs guards to ensure these fields are not accessed via a call such as `instance.__is_dirty__`, but does **not** guard 
against direct dictionary manipulation (e.g. `instance.__dict__['__is_dirty__']`) of these two fields; indeed, direct dictionary manipulation of **any** instance 
variable is not recommended, as it bypasses the checking system in place:

```
p = BakedPie()

###
# Good
###

# this is okay
p.visible = 'new_visible'

assert p.is_dirty == True

# save changes and set is_dirty to False
p.save()

###
# Bad
###

# this is NOT recommended
p.__dict__['visible'] = 'another_new_visible'

# previous op bypassed checking system
assert p.is_dirty == False

# does NOT save changes
p.save()
```

Moreover, as per [Python2](https://docs.python.org/2/library/stdtypes.html#special-attributes) and 
[Python3](https://docs.python.org/3/library/stdtypes.html#special-attributes) documentation, there are several read-only variables which cannot be set directly. `Mud` 
guards these variables specifically by throwing an `AttributeError` when user attempts to set these variables:

```
p = BakedPie()

# this is okay
p.__dict__

# throws an error because the user is a bad, bad person who doesn't deserve pies
try:
	p.__dict__ = 3.14
except AttributeError:
	pass

assert p.is_dirty == False
```

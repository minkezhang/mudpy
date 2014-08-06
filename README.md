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

An example usage case can be found in `BakedPie.py` (a ``cooked'' mud pie).

Features
----
The `Mud` class will work for property setters as well as instance variables.

Caveats
----
The `Mud` class employs reserved variables `__cache__` and `__is_dirty__` -- undefined behavior will result if the user attempts to alter these fields 
manually. `Mud.__getattribute__` and `Mud.__setattr__` employs guards to ensure these fields are not accessed via a call such as 
`instance.__is_dirty__`, but does **not** guard against direct dictionary manipulation (e.g. `instance.__dict__['__is_dirty__']`) of these two fields, or indeed **any** 
instance field in this manner.

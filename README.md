DirtyPy
====

Overview
----
One of the key aspects of programming is to write data onto the disk -- however, we do not wish to uselessly write data if it has not changed. Commonly, a `is_dirty` 
variable is employed as part of the data abstraction to mark when said data has been altered. Upon saving the data, a program can skip the disk-write portion of code if 
the `is_dirty` bit is not set.

Usage
----
Objects that inherit the `DirtyDetector` class will be able to reference a field `DirtyDetector.is_dirty` to query if the object has been changed since 
initialization.

Calling `DirtyDetector.save` will reset the `is_dirty` field to `False`.

An example usage case can be found in `ApplicationClass.py`.

Features
----
The `DirtyDetector` class will work for property setters as well as instance variables.

Caveats
----
The `DirtyDetector` class employs the use of overwriting `__setattr__` to detect changes -- modifying the class `__dict__` instance will bypass this and 
thus is **highly discouraged**. (It's also bad programming practice to alter hidden variables directly, so you shouldn't be doing that anyways.)

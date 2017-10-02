# This imports the old Python API 1.0
# This API is a direct wrapper around the C++ API
from maya import OpenMaya as om1

# This imports the Python API 2.0
# This uses a new Python based API that is much cleaner.
# Notice we get it from maya.api and not just maya
from maya.api import OpenMaya as om

# We can use the regular Python print statements
print("Hello, World! I am writing this using the standard Python print statement")

# But we can also use the Maya API to write directly to where Maya wants us to write to.
# This has several advantages because Maya can be configured to send it to different places
#       and we will automatically comply with it.
om.MGlobal.displayInfo("Hello, World! I am writing this using the OpenMaya API")

# We can also do the same using the old API
# For the most part they are structured the same to us, the users, but internally are quite different.
om1.MGlobal.displayInfo("Hello, World! This is using the old API")

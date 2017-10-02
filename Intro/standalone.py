# The Python API can be used outside of plugins as well inside of standalone scripts
# This is a unique feature to Python and it lets us use the API without having to make a plugin for everything
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma
from maya import cmds

import time


# Download animation from http://www.autodesk.com/maya-creativemarket-samples

def commands():
    """This function will use the Maya commands API to query keyframes in a scene"""
    # Get the start time so we can calculate how long this took
    start = time.time()

    # Ask Maya to fetch all the animCurves for the joints
    curves = cmds.ls(type='animCurveTA')
    # Then query all the keyframes
    keyframes = set(cmds.keyframe(curves, q=True))

    # Finally calculate how long those two lines took
    delta = time.time() - start
    # And then return it so we tally it up
    return delta


def api():
    """This function instead uses the OpenMaya api to query the keyframes"""
    # Get the start time
    start = time.time()
    # Get an iterator with all the anim curves in the scene
    # The argument provided is the type to search for
    it = om.MItDependencyNodes(om.MFn.kAnimCurveTimeToAngular)

    # This set will store all our keyframes
    keyframes = set()

    # We iterate through the iterator till it's done
    while not it.isDone():
        # We get the Function sets for the anim curves so we can interact with the curve
        curveFn = oma.MFnAnimCurve(it.thisNode())
        # We'll check how many keys it has
        for x in range(curveFn.numKeys):
            # Then query what time it happens on
            # The input method gives us back an MTime object
            # The value of the MTime is the frame number
            frame = curveFn.input(x).value

            # Then lets add it to the set
            keyframes.add(frame)

        # Finally go on to the next item in the iterator
        it.next()

    # Calculate how long this took and then return it
    delta = time.time() - start
    return delta


# Run our code in a loop so we can calculate the time it took
# It's important to run it multiple times because many factors can affect the speed of how a function runs
cmdTotal = 0
apiTotal = 0
for x in range(1000):
    apiTotal += api()
    cmdTotal += commands()

# On my machine, the API version takes almost half the time to run compared to the commands version
print "Commands took: %ss and API took %ss" % (cmdTotal, apiTotal)
print "Commands took %s times longer" % (cmdTotal / apiTotal)

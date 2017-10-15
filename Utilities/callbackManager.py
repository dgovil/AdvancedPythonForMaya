import inspect
import logging
import weakref
from functools import partial

from maya import cmds
from maya.api import OpenMaya as om

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class SceneCallbackManager(object):
    """
    The Callback Manager is in charge of keeping track of all callbacks registered in the scene
    and acting as a go between for all scene messages and any callbacks registered.

    This can help prevent bad callbacks from stalling operations or killing Maya.
    Base on PySignal: https://github.com/dgovil/PySignal
    """

    # The instance variable holds on to the instance of this manager
    _instance = None

    # We have an instance class that prevents us creating multiple of this same class
    @classmethod
    def instance(cls):
        cls._instance = cls._instance or cls()
        return cls._instance

    def __init__(self):
        super(SceneCallbackManager, self).__init__()

        # Our two dictionaries will store the callbacks and also the ids of our internal handlers
        self.__callbacks = {}
        self.__callbackIDs = {}

        # For each signal in the MSceneMessage callback, create a register and deregister method
        for signalName in dir(om.MSceneMessage):
            # All the signal names start with k
            if not signalName.startswith('k'):
                continue

            # To get the actual variable, we use getattr and we should only get back ints
            signal = getattr(om.MSceneMessage, signalName)
            if not isinstance(signal, int):
                continue

            # We make a nice name by removing the k from the start
            niceName = signalName[1:]

            # Then we create the registration and deregistration functions for each signal
            # These will internally just call the same functions but with the signal as a provided attribute
            setattr(
                self,
                'register%s' % niceName,
                partial(self.__register, signal=signal)
            )

            setattr(
                self,
                'deregister%s' % niceName,
                partial(self.__deregister, signal=signal)
            )

    def __register(self, callback, signal):
        # When we're passed a callback to register, lets first check if its a callable function or class
        # If we can't call it, don't allow it to be registered
        if not callable(callback):
            raise ValueError('Cannot register non-callable object')

        # Next we get the list of already registered callbacks to this signal
        # If it doesn't have any we'll assign it an empty list
        callbackList = self.__callbacks.setdefault(signal, [])

        # If the list is empty, it means we haven't registered it
        # So lets register the signal with our handler
        if not callbackList:
            # We'll create a handler for this signal
            # It will just call our own handler function internally
            handler = partial(self.__handler, signal=signal)
            # We'll register this handler
            # It will give us back an ID
            id = om.MSceneMessage.addCallback(signal, handler)
            # We'll store this id in our dict
            self.__callbackIDs[signal] = id

        # Now we can store our callback in the list
        # We only support functions and methods
        # Two other types of callables are lambdas and partials
        # Check out the implementation in PySignal : https://github.com/dgovil/PySignal/
        # Try implementing those yourself here

        # First we check if its a method on a class
        if inspect.ismethod(callback):
            # If it is a method, we store its self, which tells us the instance it belongs to
            callbackSelf = callback.__self__
            # We create a WeakKeyDictionary
            # This is a dictionary that allows its keys to stop existing even if it refers to them
            # In a regular dictionary, if we hold onto the value, it prevents Python cleaning up the data if its unused
            # Weakrefs let us refer to things but also let them be cleaned up
            callbackDict = weakref.WeakKeyDictionary()
            # In this dictionary we'll store the instance as the key, and the method function as the value
            callbackDict[callbackSelf] = callback.__func__

            # We then add this to the callback list
            if callbackDict not in callbackList:
                callbackList.append(callbackDict)
        else:
            # The other case is if its just a function
            # In this case we store it as a weakref reference
            # This also lets the object stop existing if needed
            callbackRef = weakref.ref(callback)
            # We'll store this in the list as well
            if callbackRef not in callbackList:
                callbackList.append(callbackRef)

    def __deregister(self, callback, signal=None):
        # To deregister, we do most of the same work as registering
        # We get the list
        callbackList = self.__callbacks.setdefault(signal, [])

        # Then we check if its a method
        if inspect.ismethod(callback):
            callbackSelf = callback.__self__
            for callbackDict in callbackList:
                # We then go through every callback to see if its the same callback
                if not isinstance(callbackDict, weakref.WeakKeyDictionary):
                    continue

                if not callbackSelf in callbackDict:
                    continue
                if not callbackDict[callbackSelf] == callback.__func__:
                    continue

                # Finally once we'fe figured that out, we remove it
                callbackList.remove(callbackDict)
                break
        else:
            try:
                # In the case of a function we just create a new weakref and try and remove it.
                callbackList.remove(weakref.ref(callback))
            except ValueError:
                pass

        # If the callback list is now empty, then we will also deregister the handler
        # This prevents it being called if its not really in use
        if not callbackList:
            # So first we remove it from the MSceneMessage callback list
            om.MSceneMessage.removeCallback(self.__callbackIDs[signal])
            # Then we delete it from both our internal dictionaries
            self.__callbacks.pop(signal)
            self.__callbackIDs.pop(signal)

    def __handler(self, *args, **kwargs):
        # For the handler, we handle it in much the same way again
        # First we get the signal from the kwargs. We'll also remove it from the kwargs using pop
        signal = kwargs.pop('signal')

        # We get the callback list
        callbackList = self.__callbacks[signal]
        # Then loop through it
        for callback in callbackList:
            # If it's a WeakKeyDictionary, we know its a class method
            if isinstance(callback, weakref.WeakKeyDictionary):
                # We then reconstitute the class method using the instance and function
                for obj, method in callback.items():
                    # If it fails to run, we put it inside a try/except to prevent it breaking other tools
                    try:
                        method(obj, *args, **kwargs)
                    except:
                        # However we should also always report the error back so its known
                        logger.exception('Failed to run method callback')

            else:
                # For functions, we convert the reference from a weakref ref, to a ref by calling it
                # This gives us back the function if it still exists or None if it doesn't
                callback = callback()
                # If it's None, it means it no longer exists so ignore it
                if callback is None:
                    continue

                # Then we can simply call it report any errors
                try:
                    callback(*args, **kwargs)
                except:
                    logger.exception('Failed to run function callback')

    def testMethod(self, *args):
        """This is just a test method for our test functions below"""
        print "Test Method"


def testFunction(*args):
    """This is just a simple test function to test our runTests function below"""
    print "testFunction", args


def runTests():
    # We'll get our manager instance
    manager = SceneCallbackManager.instance()

    # Then lets register both a function and a testMethod to afterNew
    # This will fire whenever we create a new file in Maya
    manager.registerAfterNew(testFunction)
    manager.registerAfterNew(manager.testMethod)
    # Lets make a new file. This should call both our functions
    print("Creating new file to test functions were registered")
    cmds.file(new=True, force=True)
    # Then lets deregister them
    manager.deregisterAfterNew(testFunction)
    manager.deregisterAfterNew(manager.testMethod)
    # If we make a new file now, we shouldn't be calling either
    print("Creating new file to test functions were deregistered")
    cmds.file(new=True, force=True)

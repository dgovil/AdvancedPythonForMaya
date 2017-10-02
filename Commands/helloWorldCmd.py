# First we import the OpenMaya API that we need to access Maya's internals
# It's important to import it from maya.api so we get the Python API 2.0
from maya.api import OpenMaya as om


# Just having a function of this name inside our plugin, tells Maya that it's being built using the Python 2 API.
# This is important so that Maya knows how to interact with it internally.
def maya_useNewAPI():
    # It doesn't need to do anything so we'll just pass inside it
    pass


# We need to build out our command and we do this by inheriting from the base MPxCommand that defines commands
# MPx prefixes denote classes we are meant to inherit from
class HelloWorldCmd(om.MPxCommand):
    # This is an attribute on the class that tells Maya what the plugin command will be called
    # It is always required, so don't forget to define it
    # This name must also be unique
    kPluginCmdName = "hello"

    # Lets add the flag names for the name flag
    kNameFlag = '-n'
    kNameLongFlag = '-name'

    # Finally this is the function that performs the action for the command
    def doIt(self, args):
        # To parse the arguments, we pass them to the MArgDatabase and use the MPxCommands built in syntax method to resolve it
        argData = om.MArgDatabase(self.syntax(), args)

        # First we need to check if a flag has been provided
        if argData.isFlagSet(HelloWorldCmd.kNameFlag):
            # Then we get its value.
            # THe 0 tells us which index to get in the event that multiples of the flag have been provided.
            # Since we only have one, just bother with the first one
            name = argData.flagArgumentString(HelloWorldCmd.kNameFlag, 0)
        else:
            # If nothing is provided default to world
            name = 'World'

        om.MGlobal.displayInfo("Hello, %s!" % name)


# This is the function that will create our command.
# Since our command is simple, it just needs to return an instance of the class
def cmdCreator():
    return HelloWorldCmd()


# This function lets our command take arguments
def syntaxCreator():
    # Make the syntax object that will handle all the parameters given to the command
    syntax = om.MSyntax()

    # Now lets add a flag to the syntax object
    syntax.addFlag(
        HelloWorldCmd.kNameFlag,  # First give the short name
        HelloWorldCmd.kNameLongFlag,  # Then the long name of the flag
        om.MSyntax.kString  # Then we define the type of the flag
    )

    return syntax


# We need to tell Maya how to initialize the plugin when it loads it.
# Some plugins require more complex initializations, but this one is very simple
def initializePlugin(plugin):
    # We convert our plugin to a type MfnPlugin so we can interact with it
    pluginFn = om.MFnPlugin(plugin)
    try:
        # Maya will then attempt to load and register the plugin to its internal memory
        pluginFn.registerCommand(
            # We give it the plugin name
            HelloWorldCmd.kPluginCmdName,
            # And give it the function to create it with
            cmdCreator,
            # Finally register the syntax creator
            syntaxCreator
        )
    except:
        # If it fails for whatever reason, we then error out and tell our user.
        om.MGlobal.displayError('Failed to register command: %s\n' % HelloWorldCmd.kPluginCmdName)
        # Then just let the exception be raised after we print the message above
        raise


# Finally we need to tell Maya how to unload the plug-in when requested.
# Some plugins can have a lot of actions required before unloading, but ours is again very simple
def uninitializePlugin(plugin):
    # Again we convert it to a MfnPlugin type so we can interact with it
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterCommand(HelloWorldCmd.kPluginCmdName)
    except:
        om.MGlobal.displayError('Failed to deregister command: %s\n' % HelloWorldCmd.kPluginCmdName)
        raise


"""
To call this

from Commands import helloWorldCmd

try:
    mc.unloadPlugin('helloWorldCmd')
finally:
    mc.loadPlugin(helloWorldCmd.__file__)
    
mc.hello(n="David")
"""
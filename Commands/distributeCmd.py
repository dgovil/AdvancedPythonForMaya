# Import the OpenMaya api 2
from maya.api import OpenMaya as om


# Let maya know we're using it by declaring this function
def maya_useNewAPI():
    pass


class DistributeCmd(om.MPxCommand):
    kPluginCmdName = 'distribute'

    def doIt(self, args):
        pass

    # A class method takes the class instead of the instance
    # It then gives us back an instance of the class.
    # This is useful if you want to call something before its instantiated
    @classmethod
    def cmdCreator(cls):
        return cls()

    # A static method has no knowledge of what class it belongs to
    # It's purely useful for organization purposes
    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()

        return syntax


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        plugin.registerCommand(
            DistributeCmd.kPluginCmdName,
            DistributeCmd.cmdCreator,
            DistributeCmd.syntaxCreator
        )
    except:
        om.MGlobal.displayError('Failed to register command: %s' % DistributeCmd.kPluginCmdName)
        raise


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(DistributeCmd.kPluginCmdName)
    except:
        om.MGlobal.displayError('Failed to deregister command: %s' % DistributeCmd.kPluginCmdName)
        raise


"""
To call this

from Commands import distributeCmd

try:
    mc.unloadPlugin('distrubeCmd')
finally:
    mc.loadPlugin(distributeCmd.__file__)

mc.distribute()
"""

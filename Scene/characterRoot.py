# Again, the node we're defining isn't available under the new api, so we must use the old one
import os
from maya import OpenMaya as om
from maya import OpenMayaMPx as ompx


# A custom transform must inherit from the MPxTransform node
class CharacterRoot(ompx.MPxTransform):
    kNodeName = 'characterRoot'
    kNodeID = om.MTypeId(0x01013)

    # A transform can also implement a custom transformation matrix
    # This isn't necessary for our example so we'll just use the base class for it
    kMatrix = ompx.MPxTransformationMatrix
    # The matrix must also have an ID
    kMatrixID = om.MTypeId(0x01014)

    # Now lets create some place holder attributes
    version = om.MObject()
    author = om.MObject()

    @classmethod
    def creator(cls):
        return ompx.asMPxPtr(cls())

    @staticmethod
    def initialize():
        # First lets add the version number attribute so we can easily query the rig version number
        nAttr = om.MFnNumericAttribute()
        CharacterRoot.version = nAttr.create('version', 'ver', om.MFnNumericData.kInt, 0)
        nAttr.setStorable(True)

        # Then lets store the author of the rig as meta data as well.
        # Strings are a generic typed attribute
        tAttr = om.MFnTypedAttribute()
        # To create the default value we must create it from MFnStringData
        sData = om.MFnStringData()
        defaultValue = sData.create('Dhruv Govil')
        # Finally we make our attirbute
        CharacterRoot.author = tAttr.create('author', 'a', om.MFnData.kString, defaultValue)

        # Then lets add them to our node
        CharacterRoot.addAttribute(CharacterRoot.version)
        CharacterRoot.addAttribute(CharacterRoot.author)


def initializePlugin(plugin):
    # Add the current directory to the script path so it can find the template we wrote
    dirName = 'E:\Projects\AdvancedPythonForMaya\Scene'
    # Maya will look for the environment vairable, MAYA_SCRIPT_PATH to look for scripts
    MAYA_SCRIPT_PATH = os.getenv('MAYA_SCRIPT_PATH')
    if dirName not in MAYA_SCRIPT_PATH:
        # os.pathsep gives us the character that separates paths on your specific operating system
        MAYA_SCRIPT_PATH += (os.pathsep + dirName)
        os.environ['MAYA_SCRIPT_PATH'] = MAYA_SCRIPT_PATH

    pluginFn = ompx.MFnPlugin(plugin)
    try:
        pluginFn.registerTransform(
            CharacterRoot.kNodeName,  # Name of the node
            CharacterRoot.kNodeID,  # ID for the node
            CharacterRoot.creator,  # Creator function
            CharacterRoot.initialize,  # Initialize function
            CharacterRoot.kMatrix,  # Matrix object
            CharacterRoot.kMatrixID  # Matrix ID
        )
    except:
        om.MGlobal.displayError("Failed to register node: %s" % CharacterRoot.kNodeName)
        raise


def uninitializePlugin(plugin):
    pluginFn = ompx.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(CharacterRoot.kNodeID)
    except:
        om.MGlobal.displayError('Failed to unregister node: %s' % CharacterRoot.kNodeName)
        raise


"""
To load
import maya.cmds as mc
from Scene import characterRoot
try:
    mc.delete(mc.ls(type='characterRoot'))
    # Force is important 
    mc.unloadPlugin('characterRoot', force=True)
finally:
    mc.loadPlugin(characterRoot.__file__)

mc.createNode('characterRoot', name='dhruv')
"""

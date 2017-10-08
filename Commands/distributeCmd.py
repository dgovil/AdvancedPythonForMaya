from __future__ import division
# Import the OpenMaya api 2
from maya.api import OpenMaya as om


# Let maya know we're using it by declaring this function
def maya_useNewAPI():
    pass


class DistributeCmd(om.MPxCommand):
    kPluginCmdName = 'distribute'

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

    def __init__(self, *args, **kwargs):
        super(DistributeCmd, self).__init__(*args, **kwargs)
        self.__undoStack = []

    # Our command now implements the redo method
    # This allows users to rerun our command inside of Maya.
    # To facilitate this, we move all our logic to the redoit function instead
    def doIt(self, args):
        self.redoIt()

    # The redoit function is what handles all our logic now
    def redoIt(self):
        # Because we need to know what to undo later, lets make an empty dictionary first
        undo = {}

        # Now lets start making our logic
        # First we get everything we have selected in the scene
        selection = om.MGlobal.getActiveSelectionList()

        # We need atleast 3 objects selected to do a distribution
        if selection.length() < 3:
            om.MGlobal.displayWarning('Atleast 3 objects must be selected')
            # Even though undo is empty here, lets append it so we have undo support
            self.__undoStack.append(undo)
            # Finally return so we don't both with this logic
            return

        # Now similar to undo, we need to store our transforms in a dictionary to process them
        translations = {}

        # We'll convert our selection list into an iterator of Transforms
        it = om.MItSelectionList(selection, om.MFn.kTransform)

        # Now we loop through the iterator
        while not it.isDone():
            # We get the nodes dagPath object, which tells us the transform etc...
            node = it.getDagPath()
            # Then we create an MFnTransform from it to interact with it
            tranFn = om.MFnTransform(node)

            # From this we get the partial name
            # This is longer than the short name and is unique
            # But is shorter than the full path, so is more memory efficient
            name = node.partialPathName()
            # We then get the transform values and add them to two separate dictionaries
            # One to modify and one to store for later undoing
            # Remember that dictionaries are mutable which means even if we have two references
            # to a dictionary, they share the same data
            translations[name] = tranFn.translation(om.MSpace.kWorld)
            undo[name] = tranFn.translation(om.MSpace.kWorld)

            # Finally we move on to the next object
            it.next()

        # Now lets store our current transforms so we can undo later
        self.__undoStack.append(undo)

        # Now is the good part, where we calculate the stuff we need to do
        # First lets loop through the axes
        # The enumerate function gives us a counter through the loop
        for i, axis in enumerate('xyz'):
            # We'll use the enumerate counter to filter our MVectors to just the axis we care about
            axes = [t[i] for t in translations.values()]

            # Then we use this to get the min and max
            minVal = min(axes)
            maxVal = max(axes)

            # Lets also sort the node list by their position in the given axis.
            nodes = sorted(translations.keys(),
                           key=lambda x: translations[x][i])

            # We then need to calculate the steps for our distributions.
            # If we've got four items, we'll be dividing it into three steps
            # So we use the length of the node list and subtract 1
            steps = (maxVal - minVal) / (len(nodes) - 1)

            # Finally lets loop through each node,
            # We get its transform value for the axis
            # And set it to a distance from the min value
            for x, node in enumerate(nodes):
                translations[node][i] = (minVal + (x * steps))

        # Finally we need to reloop through our selection and set the transforms we've calculated
        it.reset()
        while not it.isDone():
            # Again we get the MFnTransform for the node we want
            node = it.getDagPath()
            tranFn = om.MFnTransform(node)
            # Then we look up its position in our dictionary using its partial name
            translation = translations[node.partialPathName()]
            # Finally we set its transforms in world space to the location we calculated
            tranFn.setTranslation(translation, om.MSpace.kWorld)
            # And always remember to go on to the next item
            it.next()

    # To tell Maya that our function can undo, we must define this method
    # It can return different values depending on different conditions
    # But for our case, it's always True
    def isUndoable(self):
        return True

    # With all that done, we can start making our undo method
    def undoIt(self):
        # If we have nothing to undo, lets skip our logic
        if not self.__undoStack:
            return

        # Then we pop the last item, which is the most recent, off the end of our undoStack
        translations = self.__undoStack.pop()

        # If this was empty, then don't do anything
        if not translations:
            return

        # Finally we need to reconstruct our selection and set the transforms back
        # We make an empty selection list
        slist = om.MSelectionList()
        # Then lets loop through our data
        for i, node in enumerate(translations):
            # We'll add the item to our selection list
            slist.add(node)
            # And then get back its dagPath
            node = slist.getDagPath(i)
            # We use that to construct an MFnTransform
            tranFn = om.MFnTransform(node)
            # And use that to set its translation back to our cached value
            tranFn.setTranslation(translations[node.partialPathName()], om.MSpace.kWorld)


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
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

import maya.cmds as mc
try:
    # Force is important because of the undo stack
    mc.unloadPlugin('distributeCmd', force=True)
finally:
    mc.loadPlugin(distributeCmd.__file__)

mc.distribute()
"""

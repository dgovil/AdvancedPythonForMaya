# import the api
from maya.api import OpenMaya as om


# Let maya know we're using it by declaring this function
def maya_useNewAPI():
    pass


# We'll be making our node by deriving from MPxNode, a base class for all nodes
class minMaxNode(om.MPxNode):
    # Define the name of the node
    kNodeName = 'minMax'

    # We also need to define the ID of this node so that Maya has a unique way to identify nodes
    # This ID has to be unique and if it changes, your nodes will no longer associate with this plugin
    # The ID is a hexadecimal number
    # For developing your own nodes, that you won't release, you are free to use any number between
    # 0x00000 to 0x7ffff
    # If you plan to release nodes to the public, you need to request a set of ID's from Autodesk
    kNodeID = om.MTypeId(0x01010)

    # We'll also create placeholders for our attributes
    inputA = None
    inputB = None
    mode = None
    output = None

    # Similar to the other plugins we need a creator
    @classmethod
    def creator(cls):
        return cls()

    # We also need an initialize method that will set up the plugs and attributes on our nodes
    @staticmethod
    def initialize():
        # We need to create an instance of the Numeric Attribute Function set
        # This lets us in turn create numeric attributes
        nAttr = om.MFnNumericAttribute()

        # Lets start b defining our two input attributes
        # We assign this to an attribute on the class
        # The arguments in order are:
        # long name, short name, attribute type, default value
        minMaxNode.inputA = nAttr.create('inputA', 'ia', om.MFnNumericData.kFloat, 0.0)

        # After each attribute, we can then configure it
        # the nAttr object remembers the last object created
        nAttr.storable = True  # Allows us to store data on this plug
        nAttr.keyable = True  # Allows us to key it, but also needed to see in Node Editor

        # Finally we can do the same for the next attribute
        minMaxNode.inputB = nAttr.create('inputB', 'ib', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.keyable = True

        # Then lets create our output in the same way
        minMaxNode.output = nAttr.create('output', 'out', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True

        # We should also create our mode selection
        # This is a different type called enum
        eAttr = om.MFnEnumAttribute()
        minMaxNode.mode = eAttr.create('mode', 'm')
        eAttr.addField('min', 0)
        eAttr.addField('max', 1)
        eAttr.storable = True

        # We then add our attributes to the node
        # Otherwise they won't show up
        minMaxNode.addAttribute(minMaxNode.inputA)
        minMaxNode.addAttribute(minMaxNode.inputB)
        minMaxNode.addAttribute(minMaxNode.mode)
        minMaxNode.addAttribute(minMaxNode.output)

        # Finally we need to tell our node which attributes affect the output of other attributes
        # If we don't do this then our attributes won't update dynamically
        # In this case both our inputs affect the output
        # Our mode selection will also affect it
        minMaxNode.attributeAffects(minMaxNode.inputA, minMaxNode.output)
        minMaxNode.attributeAffects(minMaxNode.inputB, minMaxNode.output)
        minMaxNode.attributeAffects(minMaxNode.mode, minMaxNode.output)

    # Finally all of our computation will happen in this method here
    # We get two inputs, the MPlug being requested, and the MDatablock which stores this nodes data
    def compute(self, plug, data):
        # We handle the computation differently based on which node is requested.
        # In our case we only have one output to compute for
        if plug != minMaxNode.output:
            return

        # The inputValue gives us back an MDataHandle
        iaHandle = data.inputValue(minMaxNode.inputA)
        ibHandle = data.inputValue(minMaxNode.inputB)
        mHandle = data.inputValue(minMaxNode.mode)

        # From these data handles we can extract their values
        # Mode returns 0 or 1 integers
        mode = mHandle.asInt()

        ia = iaHandle.asFloat()
        ib = ibHandle.asFloat()

        if mode:
            value = max([ia, ib])
        else:
            value = min([ia, ib])

        # Then we can set this value on our node
        outHandle = data.outputValue(minMaxNode.output)
        outHandle.setFloat(value)

        # Finally we set out node to clean, meaning that its data is fresh
        data.setClean(plug)


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.registerNode(
            minMaxNode.kNodeName,  # The name of the node
            minMaxNode.kNodeID,  # The unique ID for this node
            minMaxNode.creator,  # The function to create this node
            minMaxNode.initialize,  # The function to initalize the node
        )
    except:
        om.MGlobal.displayError('Failed to register node %s' % minMaxNode.kNodeName)
        raise


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(minMaxNode.kNodeID)
    except:
        om.MGlobal.displayError('Failed to unregister node %s' % minMaxNode.kNodeName)
        raise


"""
To load
from Nodes import minMaxNode
try:
    # Force is important 
    mc.unloadPlugin('minMaxNode', force=True)
finally:
    mc.loadPlugin(minMaxNode.__file__)
"""

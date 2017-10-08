# Unfortunately, OpenMaya 2 doesn't support creating deformers
# Therefore we must use the old OpenMaya instead

from maya import OpenMaya as om
from maya import OpenMayaMPx as ompx
import maya.cmds as cmds

# Unfortunately the API has changed somewhat between Maya 2015 and 2016 so we need to get the right attributes instead
# This isn't a big deal, and if you're only using Maya 2016 or above you can skip half of this if statement
kApiVersion = cmds.about(apiVersion=True)
if kApiVersion < 201600:
    inputAttr = ompx.cvar.MPxDeformerNode_input
    inputGeomAttr = ompx.cvar.MPxDeformerNode_inputGeom
    outputGeomAttr = ompx.cvar.MPxDeformerNode_outputGeom
    envelopeAttr = ompx.cvar.MPxDeformerNode_envelope
else:
    inputAttr = ompx.cvar.MPxGeometryFilter_input
    inputGeomAttr = ompx.cvar.MPxGeometryFilter_inputGeom
    outputGeomAttr = ompx.cvar.MPxGeometryFilter_outputGeom
    envelopeAttr = ompx.cvar.MPxGeometryFilter_envelope


class PushDeformer(ompx.MPxDeformerNode):
    id = om.MTypeId(0x01012)  # Setup the ID
    name = 'push'  # Setup the name

    # Now add the attributes we'll be using
    # Unlike OpenMaya 2, we need to use an empty MObject here instead of just None
    push = om.MObject()

    @classmethod
    def creator(cls):
        # Unlike OpenMaya API 2, we need to return this as a MPxPtr instead
        return ompx.asMPxPtr(cls())

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()

        PushDeformer.push = nAttr.create('push', 'p', om.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(True)
        nAttr.setStorable(True)
        nAttr.setChannelBox(True)

        PushDeformer.addAttribute(PushDeformer.push)
        PushDeformer.attributeAffects(PushDeformer.push, outputGeomAttr)

        # We also want to make our node paintable
        cmds.makePaintable(
            PushDeformer.name,
            'weights',
            attrType='multiFloat',
            shapeMode='deformer'
        )

    def deform(self, data, geoIterator, matrix, geometryIndex):

        # Get the push value
        pushHandle = data.inputValue(self.push)
        push = pushHandle.asFloat()

        # get the envelope value
        envelopeHandle = data.inputValue(envelopeAttr)
        envelope = envelopeHandle.asFloat()

        # Get the input geometry
        mesh = self.getInputMesh(data, geometryIndex)

        # Create an empty array(list) of Float Vectors to store our normals in
        normals = om.MFloatVectorArray()
        # Then make the meshFn to interact with the mesh
        meshFn = om.MFnMesh(mesh)
        # And we use this to get and store the normals from the mesh onto the normals array we created above
        # Remember to pay attention to the pluralization of normals
        meshFn.getVertexNormals(
            True, # If True, the normals are angleWeighted which is what we want
            normals, # We tell it what to store the data in, in this case our array above,
            om.MSpace.kTransform # Finally we tell it what space we want the normals in, in this case the local object space
        )

        # Now we can iterate through the geometry vertices and do our deformation
        while not geoIterator.isDone():
            # Get the index of our current point
            index = geoIterator.index()
            # Look up the normals for this point from our array
            normal = om.MVector(normals[index])
            # Get the position of the point
            position = geoIterator.position()
            # Then calculate the offset
            # we do this by multiplying the magnitude of the normal vector by the intensity of the push and envelope
            offset = (normal * push * envelope)

            # We then query the painted weight for this area
            weight = self.weightValue(data, geometryIndex, index)
            offset = (offset * weight)

            # Finally we can set the position
            geoIterator.setPosition(position+offset)
            # And always remember to go on to the next item in the list
            geoIterator.next()



    def getInputMesh(self, data, geomIdx):
        # To get the mesh we need to check the input of the node
        inputHandle = data.outputArrayValue(inputAttr)
        inputHandle.jumpToElement(geomIdx)
        # Once we have the input handle, we get its values, then find the children mesh and get it as a mesh MObject
        mesh = inputHandle.outputValue().child(inputGeomAttr).asMesh()
        return mesh


def initializePlugin(plugin):
    pluginFn = ompx.MFnPlugin(plugin)
    try:
        pluginFn.registerNode(
            PushDeformer.name,
            PushDeformer.id,
            PushDeformer.creator,
            PushDeformer.initialize,
            ompx.MPxNode.kDeformerNode # One extra argument to tell it the type of node
                              )
    except:
        om.MGlobal.displayError('Failed to register node: %s' % PushDeformer.name)
        raise

def uninitializePlugin(plugin):
    pluginFn = ompx.MFnPlugin(plugin)

    try:
        pluginFn.deregisterNode(PushDeformer.id)
    except:
        om.MGlobal.displayError('Failed to unregister node: %s' % PushDeformer.name)
        raise

"""
To load
from Nodes import pushDeformer
import maya.cmds as mc

try:
    # Force is important 
    mc.unloadPlugin('pushDeformer', force=True)
finally:
    mc.loadPlugin(pushDeformer.__file__)
    
mc.polySphere()
mc.deformer(type='push')
"""

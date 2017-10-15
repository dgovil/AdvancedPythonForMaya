import maya.cmds as cmds
from maya.api import OpenMaya as om


class CreatedNodesContext(object):
    """The CreatedNodesContext keeps track of all the objects created during the execution of the code block"""

    def __init__(self):
        # We create a list to hold on to the nodes creates
        self.__nodes = []
        # as well as the id of the handler we'll register
        self.__handlerID = None

    def __enter__(self):
        # When we enter the context, we'll register the handler
        # We care about all nodes that are subclasses of dependNode, essentially every single node
        self.__handlerID = om.MDGMessage.addNodeAddedCallback(self.__handler, 'dependNode')
        # Then we return this class
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # When we exit, we'll deregister the handler from the ID we stored
        om.MDGMessage.removeCallback(self.__handlerID)
        # We'll also empty out our list so as to prevent any errors from holding onto objects
        self.__nodes = []

        # Then if there was an error, we'll raise it
        if exc_val:
            raise exc_val

    def __handler(self, node, *args):
        # The handler is simple and stores the given nodes in the nodes list
        # The nodes given to this function are MObjects
        self.__nodes.append(node)

    def nodes(self):
        # The nodes function will filter through the nodes and make sure we only give back valid nodes
        validNodes = []

        # The selection list will help us validate whether a node exists or not
        sel = om.MSelectionList()

        # Lets iterate through the node list we've captured
        for node in self.__nodes:
            # If the node is null, it means the MObject no longer points to valid data so we can ignore it
            if node.isNull():
                continue

            # We now have to get the path of the node
            # If the node is a dagNode (checked by seeing if it has that function set)
            # Then we need to get its shortest unique path
            if node.hasFn(om.MFn.kDagNode):
                # We create an MFnDagNode for it
                dag = om.MFnDagNode(node)
                # The partial path is the shortest unique name to the object
                # A full path can be wasteful in terms of memory
                # But just the name can lead to ambiguity if multiple objects share the name
                # The partial path instead gives us the shortest name we know to be unique
                path = dag.partialPathName()
            else:
                # If it isn't a DAGNode, then it's a DG node and always has a unique name
                dg = om.MFnDependencyNode(node)
                path = dg.name()

            # Even once we have the path, it may not exist anymore (if deleted etc)
            # We'll try and add it to the selection list and if it fails to add then we'll assume it no longer exists
            try:
                sel.add(path)
            except:
                continue

            # Then add it to the validNodes list
            validNodes.append(path)

        # Finally return the node list
        return validNodes


def test():
    cmds.file(new=True, force=True)
    with CreatedNodesContext() as cnc:
        cubes = cmds.polyCube()
        cmds.polySphere()
        cmds.spaceLocator()
        cmds.delete(cubes)
        print "Created the following nodes:\n\t%s" % ('\n\t'.join(cnc.nodes()))

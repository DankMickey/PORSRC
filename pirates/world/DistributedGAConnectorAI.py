from panda3d.core import getModelPath
# STUB

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedGAConnectorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAConnectorAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

    # setModelPath(string) required broadcast ram
    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    # setLinks(uint8, string, Link []) broadcast ram

    # setUniqueId(string) required broadcast ram
    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    # requestPrivateArea(uint32) airecv clsend

    # setPrivateArea(uint32, uint32, uint32, bool) airecv clsend

    def posControlledByCell(self):
        return False

    @staticmethod
    def makeFromObjectKey(air, objKey, data):
        obj = DistributedGAConnectorAI(air)
        obj.setUniqueId(objKey)
        obj.setPos(data.get('Pos', 0))
        obj.setHpr(data.get('Hpr', 0))
        obj.setModelPath(data['Visual']['Model'])

        if 'GridPos' in data:
            obj.setPos(data.get('GridPos', 0))

        return obj


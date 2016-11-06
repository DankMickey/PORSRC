from direct.distributed.DistributedObjectAI import *
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *

class DistributedSmileyAI(DistributedInteractiveAI, DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSmileyAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)
        self.color = [0, 0, 0, 0]
        self.visZone = ''

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)


    def setVisZone(self, visZone):
        self.visZone = visZone

    def getVisZone(self):
        return self.visZone

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def getSphereScale(self):
        return self.sphereScale

    def handleInteract(self, avId, interactType, instant):
        return REJECT #TODO

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        if 'VisZone' in data:
            obj.setVisZone(data['VisZone'])

        gridPos = data.get('GridPos')
        if gridPos:
            obj.setPos(gridPos)

        obj.setSphereScale(int(float(data.get('Aggro Radius', 1.0))))
        return obj

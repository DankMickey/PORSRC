from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.distributed.GridParent import GridParent
from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
import WorldGlobals

from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.piratesbase import PiratesGlobals

from DistributedInteriorDoorAI import DistributedInteriorDoorAI

class DistributedGAInteriorAI(DistributedGameAreaAI, DistributedCartesianGridAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAInteriorAI')

    def __init__(self, air, extDoor):
        DistributedGameAreaAI.__init__(self, air, '')

        cellWidth = WorldGlobals.GAME_AREA_INTERIOR_CELL_SIZE
        gridSize = WorldGlobals.GAME_AREA_INTERIOR_GRID_SIZE
        gridRadius = WorldGlobals.GAME_AREA_INTERIOR_GRID_RADIUS
        zoneId = WorldGlobals.GAME_AREA_INTERIOR_STARTING_ZONE

        DistributedCartesianGridAI.__init__(self, air, zoneId, gridSize, gridRadius, cellWidth)

        self.extDoor = extDoor
        self.intDoors = []

    def setBuildingInterior(self, buildingInterior):
        self.buildingInterior = buildingInterior

    def getBuildingInterior(self):
        return self.buildingInterior

    def setCaveInterior(self, caveInterior):
        self.caveInterior = caveInterior

    def getCaveInterior(self):
        return self.caveInterior

    def createObject(self, objType, parent, objKey, object):
        genObj = None

        if objType == 'Island Game Area':
            if not self.getUniqueId():
                self.b_setUniqueId(objKey)
                
                if object['Visual']['Model']:
                    self.b_setModelPath(object['Visual']['Model'])

        elif objType == 'Building Interior':
            if not self.getUniqueId():
                self.b_setUniqueId(objKey)
                self.b_setModelPath(object['Visual']['Model'])

        elif objType == 'Door Locator Node':
            genObj = self.createIntDoor(objKey, object)

        else:
            genObj = DistributedGameAreaAI.createObject(self, objType, parent, objKey, object)

        return genObj

    def createIntDoor(self, objKey, object):
        if not self.buildingInterior:
            return

        intDoor = DistributedInteriorDoorAI.makeFromObjectKey(self.air, objKey,
                                         object, self.extDoor.getBuildingUid())
        intDoor.setOtherDoorId(self.extDoor.doId)
        self.generateChild(intDoor)
        self.intDoors.append(intDoor)
        return intDoor
    
    def getZoneFromXYZ(self, *args):
        return 2709

    def generateChild(self, obj, zoneId = None, cellParent = False):
        if not hasattr(obj, 'getPos') and zoneId is None:
            self.notify.warning("Failed to spawn '%s'. Object does not have a getPos()" % type(obj).__name__)
            return

        if zoneId is None:
            zoneId = 2709

        if self.buildingInterior:
            obj.interior = self

        obj.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId)

        if hasattr(obj, 'posControlledByCell'):
            cellParent = obj.posControlledByCell()

        if hasattr(obj, 'posControlledByIsland'): #LEGACY.
            self.notify.warning("posControlledByIsland is deprecated. Please switch '%s' to posControlledByCell as soon as possible." % type(obj).__name__)
            cellParent = obj.posControlledByIsland()

        if cellParent and not self.buildingInterior and not self.caveInterior:
            cell = GridParent.getCellOrigin(self, zoneId)
            pos = obj.getPos()

            obj.reparentTo(cell)
            obj.setPos(self, pos)

            obj.sendUpdate('setPos', obj.getPos())
            obj.sendUpdate('setHpr', obj.getHpr())

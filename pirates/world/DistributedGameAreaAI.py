from panda3d.core import NodePath, getModelPath
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.distributed.GridParent import GridParent
from pirates.battle.DistributedEnemySpawnerAI import DistributedEnemySpawnerAI
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame.DistributedBlackjackTableAI import DistributedBlackjackTableAI
from pirates.minigame.DistributedHoldemTableAI import DistributedHoldemTableAI
from pirates.minigame.Distributed7StudTableAI import Distributed7StudTableAI
from pirates.minigame.DistributedLiarsDiceAI import DistributedLiarsDiceAI

class DistributedGameAreaAI(DistributedNodeAI):
    def __init__(self, air, modelPath):
        DistributedNodeAI.__init__(self, air)

        self.uid = ''
        self.name = ''
        self.modelPath = modelPath

        self.buildingInterior = False

        self.spawner = DistributedEnemySpawnerAI(self)
        self.npcs = {}

        self._movementNodes = {}
        self._movementPaths = {}

        self.setPythonTag('npTag-gameArea', self)

    def setUniqueId(self, uid):
        self.uid = uid
        self.air.uid2do[uid] = self

    def d_setUniqueId(self, uid):
        self.sendUpdate('setUniqueId', [uid])

    def b_setUniqueId(self, uid):
        self.setUniqueId(uid)
        self.d_setUniqueId(uid)

    def getUniqueId(self):
        return self.uid

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def getModelPath(self):
        return self.modelPath

    def createObject(self, objType, parent, objKey, object):
        genObj = None

        if objType == 'Spawn Node' and config.GetBool('want-enemies', False):
            self.spawner.addEnemySpawnNode(objKey, object)

        elif objType == 'Dormant NPC Spawn Node' and config.GetBool('want-enemies', False) and config.GetBool('want-dormant-spawns', False):
            self.spawner.addEnemySpawnNode(objKey, object)

        elif objType == 'Movement Node' and config.GetBool('want-enemies', False):
            genObj = self.generateNode(objType, objKey, object, parent)
            self._movementNodes[objKey] = genObj

        elif objType == 'Animal' and config.GetBool('want-animals', False):
            self.spawner.addAnimalSpawnNode(objKey, object)

        elif objType == 'Townsperson' and config.GetBool('want-npcs', False):
            genObj = self.spawner.spawnNPC(objKey, object)
            self.npcs[genObj.doId] = genObj

            gridPos = object.get('GridPos')
            if gridPos and isinstance(parent, NodePath):
                genObj.setPos(self, gridPos)
                genObj.d_updateSmPos()
                newZoneId = self.getZoneFromXYZ(genObj.getPos(self))
                genObj.b_setLocation(genObj.parentId, newZoneId)

        elif objType == 'Parlor Game' and config.GetBool('want-parlor-games', True):
            gameType = object.get('Category')
            if gameType == "Blackjack":
                genObj = DistributedBlackjackTableAI.makeFromObjectKey(self.air, objKey, object)
            elif gameType == "Poker":
                genObj = DistributedPokerTableAI.makeFromObjectKey(self.air, objKey, object)
            elif gameType == "Holdem":
               genObj = DistributedHoldemTableAI.makeFromObjectKey(self.air, objKey, object)
            elif gameType == "7Stud":
                genObj = Distributed7StudTableAI.makeFromObjectKey(self.air, objKey, object)
            else:
                self.notify.warning("Unknown Parlor Game type: %s" % gameType)

            if genObj != None:
                self.generateChild(genObj, cellParent = True)

        elif objType == 'Dice Game' and config.GetBool('want-dice-games', True):
            self.notify.info("Generating Dice Game.")
            gameType = object.get('Category')
            if gameType == "Liars":
                genObj = DistributedLiarsDiceAI.makeFromObjectKey(self.air, objKey, object)
            else:
                self.notify.warning("Unknown Dice Game type: %s" % gameType)

            if genObj != None:
                self.generateChild(genObj, cellParent = True)

        elif objType == 'Collision Barrier':
            genObj = self.generateNode(objType, objKey, object, parent)

        else:
            genObj = self.generateNode(objType, objKey, object, parent, gridPos=True)

        return genObj

    def generateChild(self, obj, zoneId=None, cellParent=False):

        if not hasattr(obj, 'getPos'):
            return

        if zoneId is None:
            zoneId = self.getZoneFromXYZ(obj.getPos())

        obj.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId)

        if hasattr(obj, 'posControlledByCell'):
            cellParent = obj.posControlledByCell()

        if hasattr(obj, 'posControlledByIsland'): #LEGACY.
            self.notify.warning("posControlledByIsland is deprecated. Please switch '%s' to posControlledByCell as soon as possible." % type(obj).__name__)
            cellParent = obj.posControlledByIsland()

        if cellParent: 
            cell = GridParent.getCellOrigin(self, zoneId)
            pos = obj.getPos()

            obj.reparentTo(cell)
            obj.setPos(self, pos)

            obj.sendUpdate('setPos', obj.getPos())
            obj.sendUpdate('setHpr', obj.getHpr())

    def generateNode(self, objType, objKey, object, parent=None, gridPos=False, noLight=False):
        genObj = None
        nodeName =  'objNode-%s-%s' % (objType, objKey)

        if isinstance(parent, NodePath):
            genObj = parent.attachNewNode(nodeName)

        else:
            genObj = NodePath(nodeName)

            if 'Pos' in object:
                genObj.setPos(object['Pos'])

            if 'Hpr' in object:
                genObj.setHpr(object['Hpr'])

            if 'GridPos' in object and gridPos:
                genObj.setPos(object['GridPos'])

            if noLight:
                genObj.setLightOff()

        return genObj
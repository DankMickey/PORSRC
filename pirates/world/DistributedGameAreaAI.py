from panda3d.core import NodePath, getModelPath
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.distributed.GridParent import GridParent
from pirates.battle.DistributedEnemySpawnerAI import DistributedEnemySpawnerAI
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.interact.DistributedInteractivePropAI import DistributedInteractivePropAI
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame.DistributedBlackjackTableAI import DistributedBlackjackTableAI
from pirates.minigame.DistributedHoldemTableAI import DistributedHoldemTableAI
from pirates.minigame.Distributed7StudTableAI import Distributed7StudTableAI
from pirates.minigame.DistributedLiarsDiceAI import DistributedLiarsDiceAI
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI
from pirates.holiday.DistributedHolidayPigAI import DistributedHolidayPigAI
from pirates.holiday.DistributedHolidayBonfireAI import DistributedHolidayBonfireAI
from pirates.quest.DistributedQuestPropAI import DistributedQuestPropAI
from pirates.world.DistributedFortAI import DistributedFortAI

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

        self.wantNPCS = config.GetBool('want-npcs', False)
        self.wantEnemies = config.GetBool('want-enemies', False)
        self.wantBosses = config.GetBool('want-bosses', True)
        self.wantForts = config.GetBool('want-simple-forts', True)
        self.wantQuestProps = config.GetBool('want-quest-props', True)
        self.wantHolidayObjects = config.GetBool('want-holiday-objects', True)

        self.debugPrints = config.GetBool('want-debug-world-prints', True)

        self.wantInvasions = config.GetBool('want-invasions', True)
        self._invasionSpawns = {}
        self._invasionBarricades = {}

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

        if objType == 'Spawn Node' and self.wantEnemies:
            self.spawner.addEnemySpawnNode(objKey, object)

        elif objType == 'Dormant NPC Spawn Node' and self.wantEnemies and config.GetBool('want-dormant-spawns', False):
            self.spawner.addEnemySpawnNode(objKey, object)

        elif objType == 'Movement Node' and self.wantEnemies:
            genObj = self.generateNode(objType, objKey, object, parent)
            self._movementNodes[objKey] = genObj

        elif objType == 'Animal' and config.GetBool('want-animals', False):
            self.spawner.addAnimalSpawnNode(objKey, object)

        elif objType == 'Townsperson' and self.wantNPCS:

            #quick hack to prevent holiday npcs
            holiday = object.get('Holiday', '')
            if holiday != '' and config.GetBool('remove-holiday-npcs', True):
                self.notify.info("Preventing Holiday NPC spawn.")
                return None

            genObj = self.spawner.spawnNPC(objKey, object)
            self.npcs[genObj.doId] = genObj

            gridPos = object.get('GridPos')
            if gridPos and isinstance(parent, NodePath):
                genObj.setPos(self, gridPos)
                genObj.d_updateSmPos()
                newZoneId = self.getZoneFromXYZ(genObj.getPos(self))
                genObj.b_setLocation(genObj.parentId, newZoneId)

        elif objType == 'Skeleton' and self.wantBosses:
            self.__printUnimplementedNotice(objType) #TODO

        elif objType == 'NavySailor' and self.wantBosses:
            self.__printUnimplementedNotice(objType) #TODO

        elif objType == 'Creature' and self.wantBosses:
            self.__printUnimplementedNotice(objType) #TODO

        elif objType == 'Searchable Container' and config.GetBool('want-searchables', False):
            genObj = DistributedSearchableContainerAI.makeFromObjectKey(self.air, objKey, object)
            self.generateChild(genObj)

        elif objType == 'Holiday' and self.wantHolidayObjects:
            #self.__printUnimplementedNotice(objType) #TODO
            genObj = self.generateNode(objType, objKey, object, parent, gridPos=True)

        elif objType == 'Holiday Object' and self.wantHolidayObjects:
            subType = object.get('SubType')
            if subType == 'Roast Pig':
                genObj = DistributedHolidayPigAI.makeFromObjectKey(self.air, objKey, object)
            elif subType == 'Bonfire':
                genObj = DistributedHolidayBonfireAI.makeFromObjectKey(self.air, objKey, object)
            else:
                self.notify.warning("Unsupported Holiday Object SubType: %s" % subType)

        elif objType == 'Building Exterior':
            genObj = self.air.worldCreator.createBuilding(self, objKey, object)

        elif objType == 'Island Game Area' and config.GetBool('want-link-tunnels', False):
            self.__printUnimplementedNotice(objType)

        elif objType == 'Invasion Barricade' and self.wantInvasions:
            self._invasionBarricades[objKey] = self.generateNode(objType, objKey, object, parent, gridPos=True)
            if config.GetBool('force-invasion-barricades', False):
                self.__printUnimplementedNotice(objType)

        elif objType == 'Invasion Barrier' and self.wantInvasions:
            self.generateNode(objType, objKey, object, parent, gridPos=True)

        elif objType == 'Invasion NPC Spawn Node' and self.wantInvasions:
            self._invasionSpawns[objKey] = self.generateNode(objType, objKey, object, parent, gridPos=True)
            if config.GetBool('force-invasion-spawns', True):
                self.spawner.addEnemySpawnNode(objKey, object)

        elif objType == 'Fort' and self.wantForts: #TODO find objType
            self.notify.info("Spawning %s on %s" % (objType, self.getName()))
            genObj = DistributedFortAI.makeFromObjectKey(self.air, objKey, object)
            #self.__printUnimplementedNotice(objType)

        elif objType == 'Interactive Prop':
            #self.__printUnimplementedNotice(objType) #TODO object doesnt properly spawn
            genObj = DistributedInteractivePropAI.makeFromObjectKey(self.air, objKey, object)

        elif objType == 'Quest Prop' and self.wantQuestProps:
            self.__printUnimplementedNotice(objType) #TODO
            #DistributedQuestPropAI.makeFromObjectKey(self.air, objKey, object)

        elif objType == 'Parlor Game' and config.GetBool('want-parlor-games', True):
            gameType = object.get('Category', 'Poker')
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
            gameType = object.get('Category', 'Dice')
            if gameType == "Liars":
                genObj = DistributedLiarsDiceAI.makeFromObjectKey(self.air, objKey, object)
            else:
                self.notify.warning("Unknown Dice Game type: %s" % gameType)

            if genObj != None:
                self.generateChild(genObj, cellParent = True)

        elif objType == 'Collision Barrier':
            genObj = self.generateNode(objType, objKey, object, parent)

        else:
            self.__logMissing(objType)
            genObj = self.generateNode(objType, objKey, object, parent, gridPos=True)

        return genObj

    def __printDebugInfo(self, objType, data):
        if self.debugPrints:
            self.notify.info("Type: %s Data: %s" % (objType, data))

    def __printUnimplementedNotice(self, objType):
        from pirates.world.WorldCreatorAI import WorldCreatorAI
        WorldCreatorAI.registerUnimplemented(objType)

    def __logMissing(self, objType):
        if not self.debugPrints:
            return

        ignoreList = [
            'Port Collision Sphere',
            'Holiday',
            'Holiday Object',
            'Ambient SFX Node',
            'Animated Avatar - Navy',
            'Player Spawn Node',
            'Shop - Jeweler',
            'Shop - Tailor',
            'Shop - Barber',
            'Furniture',
            'Hay',
            'Barrel',
            'Pig_stuff',
            'Location Sphere',
            'Horse_trough',
            'Crane',
            'Mortar_Pestle',
            'Cacti',
            'Spanish Walls',
            'Voodoo',
            'Volcano',
            'Log_Stack',
            'Grass',
            'Stairs',
            'Sack',
            'Cups',
            'Shanty Gypsywagon',
            'Shanty Tents',
            'Flower_Pots',
            'Pier',
            'Cemetary',
            'LaundryRope',
            'TreeBase',
            'Swamp_props',
            'Paddle',
            'Bush',
            'Fountain',
            'Swamp_props_small',
            'Tunnel Cap',
            'Burnt_Props',
            'Pan',
            'Military_props',
            'Interior_furnishings',
            'Jungle_Props',
            'Food',
            'Cart',
            'Pots',
            'Wall_Hangings',
            'Enemy_Props',
            'Arch',
            'Chimney',
            'Jugs_and_Jars',
            'Tree - Animated',
            'FountainSmall',
            'Shop - Fisherman',
            'Bucket',
            'Tree',
            'Vines',
            'Rope',
            'Prop_Groups',
            'Rock',
            'Trellis',
            'Light - Dynamic',
            'Ship_Props',
            'Bridge',
            'Cave_Props',
            'Well',
            'Cave_Pieces',
            'Writing_Paper',
            'Furniture - Fancy',
            'Wall',
            'Crate',
            'Baskets',
            'Ocean_Props',
            'Mining_props',
            'Tools',
            'Jungle_Props_large',
            'Treasure Chest',
            'Trunks',
            'Light_Fixtures',
            'ChickenCage',
            'Effect Node',
            'Player Boot Node',
            'Ship Wreck',
            'Quest Node',
            'Switch Prop',
            'Jail Cell Door',
            'Portal Node',
            'Locator Node',
            'Simple Fort',
            'Door Locator Node'
        ]

        if objType in ignoreList and config.GetBool('want-debug-ignore-list', True):
            return

        from pirates.world.WorldCreatorAI import WorldCreatorAI
        WorldCreatorAI.registerMissing(objType)

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
from panda3d.core import Character
from direct.directnotify import DirectNotifyGlobal

from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
from pirates.npc.DistributedKillerGhostAI import DistributedKillerGhostAI
from pirates.npc.DistributedBountyHunterAI import DistributedBountyHunterAI
from pirates.npc.DistributedVoodooZombieAI import DistributedVoodooZombieAI
from pirates.npc.DistributedGhostAI import DistributedGhostAI

from pirates.battle.DistributedBattleNPCAI import *
from pirates.creature.DistributedCreatureAI import *
from pirates.creature.DistributedAnimalAI import *
from pirates.creature.DistributedRavenAI import *

from pirates.ship import ShipGlobals
from pirates.ship.DistributedNPCSimpleShipAI import DistributedNPCSimpleShipAI
from pirates.ship.DistributedPlayerSeizeableShipAI import DistributedPlayerSeizeableShipAI

import random, os

NPC_CACHE = {}
ANIMAL_CACHE = {}
SHIP_CACHE = {}

class EnemySpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('EnemySpawnNode')

    def __init__(self, spawner, data):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'EnemySpawnNode-%d' % self.air.allocateChannel()
        self.npcs = {}

        self.data = data
        if 'Spawnables' not in data:
            return

        self.spawnable = self.data['Spawnables']
        if self.spawnable not in AvatarTypes.NPC_SPAWNABLES:
            return

        self.avType = AvatarTypes.NPC_SPAWNABLES[self.spawnable][0]()
        self.avClass = self.getClassFromAvatarType(self.avType)
        if self.avClass == None:
            self.notify.warning("Unknown avatar class: %s" % self.spawnable)
            DistributedEnemySpawnerAI.missingAvatarClass(self.avType)
            return

        self.desiredNumAvatars = self.data['Min Population'] or 1
        self.acceptOnce('startShardActivity', self.died)

    def getClassFromAvatarType(self, avatar):
        avatarClass = None

        miscList = [
        	AvatarTypes.FireBat]

        if avatar in NPC_CACHE:
            return NPC_CACHE[avatar]

        if avatar.isA(AvatarTypes.Animal):
            avatarClass = DistributedAnimalAI
        elif avatar.isA(AvatarTypes.SeaMonster):
            pass
        elif avatar.isA(AvatarTypes.Undead):
            if avatar.isA(AvatarTypes.FrenchBoss) or avatar.isA(AvatarTypes.SpanishBoss):
                #avatarClass = DistributedBossSkeletonAI
                pass
            elif avatar == AvatarTypes.BomberZombie:
                #avatarClass = DistributeBomberZombieAI
                pass
            else:
                avatarClass = DistributedNPCSkeletonAI
        elif avatar.isA(AvatarTypes.Navy):
            avatarClass = DistributedNPCNavySailorAI
        elif avatar.isA(AvatarTypes.GhostPirate):
            avatarClass = DistributedGhostAI
        elif avatar.isA(AvatarTypes.KillerGhost):
            avatarClass = DistributedKillerGhostAI
        elif avatar.isA(AvatarTypes.BountyHunter):
            avatarClass = DistributedBountyHunterAI
        elif avatar.isA(AvatarTypes.TradingCo):
            avatarClass = DistributedNPCNavySailorAI
        elif avatar.isA(AvatarTypes.VoodooZombie):
            if avatar.isA(AvatarTypes.VoodooZombieBoss):
             	pass
            else:
                avatarClass = DistributedVoodooZombieAI
        elif avatar.isA(AvatarTypes.LandCreature):
            avatarClass = DistributedCreatureAI
        elif avatar.isA(AvatarTypes.AirCreature):
        	avatarClass = DistributedCreatureAI

        if avatar not in NPC_CACHE and avatarClass != None:
            NPC_CACHE[avatar] = avatarClass

        return avatarClass

    def died(self):
        taskMgr.doMethodLater(random.random() * 7, self.__checkCreatures, self.uniqueName('checkCreatures'))

    def __checkCreatures(self, task):
        deadNpcs = []
        for doId, npc in self.npcs.items():
            if npc.isDeleted():
                deadNpcs.append(doId)

        for doId in deadNpcs:
            del self.npcs[doId]

        # Upkeep population
        numNpcs = len(self.npcs)
        if numNpcs < self.desiredNumAvatars:
            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            npc = self.avClass.makeFromObjectKey(self.avClass, self, uid,
                                                 self.avType, self.data)
            self.spawner.spawn(npc)
            self.npcs[npc.doId] = npc

        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class AnimalSpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('AnimalSpawnNode')

    def __init__(self, spawner, data):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'AnimalSpawnNode-%d' % self.air.allocateChannel()
        self.npcs = {}

        self.data = data
        if 'Species' not in data:
            return

        self.spawnable = self.data['Species']
        if self.spawnable not in AvatarTypes.NPC_SPAWNABLES:
            self.notify.warning("Unknown animal species: %s" % self.spawnable)
            return

        self.avType = AvatarTypes.NPC_SPAWNABLES[self.spawnable][0]()

        self.avClass = self.getClassFromAnimalType(self.spawnable)
        if self.avClass == None:
            self.notify.warning("Unknown animal class: %s" % self.spawnable)
            DistributedEnemySpawnerAI.missingAnimalClass(self.spawnable)
            return            

        self.desiredNumAvatars = 1
        self.acceptOnce('startShardActivity', self.died)

    def getClassFromAnimalType(self, animal): #Done like this for potential future expansion
        avatarClass = None
        if animal in ANIMAL_CACHE:
            return ANIMAL_CACHE[animal]

        if animal == "Raven":
            avatarClass = DistributedRavenAI
        elif animal == "Seagull":
            avatarClass = None #TODO
        else:
            avatarClass = DistributedAnimalAI

        if avatarClass != None and animal not in ANIMAL_CACHE:
            ANIMAL_CACHE[animal] = avatarClass

        return avatarClass

    def died(self):
        taskMgr.doMethodLater(random.random() * 7, self.__checkCreatures, self.uniqueName('checkCreatures'))

    def __checkCreatures(self, task):
        deadNpcs = []
        for doId, npc in self.npcs.items():
            if npc.isDeleted():
                deadNpcs.append(doId)

        for doId in deadNpcs:
            del self.npcs[doId]

        # Upkeep population
        numNpcs = len(self.npcs)
        if numNpcs < self.desiredNumAvatars:
            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            npc = self.avClass.makeFromObjectKey(self.avClass, self, uid,
                                                 self.avType, self.data)
            self.spawner.spawn(npc)
            self.npcs[npc.doId] = npc

        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class ShipSpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipSpawnNode')

    def __init__(self, spawner, data):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'ShipSpawnNode-%d' % self.air.allocateChannel()
        self.ships = {}

        self.data = data
        if 'Spawnables' not in data:
            return

        self.spawnable = self.data['Spawnables']
        self.flagship = self.data['Flagship'] or False

        if self.spawnable not in ShipGlobals.SHIP_CLASS_LIST:
            self.notify.warning("Unknown ship class: %s" % self.spawnable)
            DistributedEnemySpawnerAI.missingShipClass(self.spawnable)
            return

        self.shipClass = DistributedNPCSimpleShipAI

        self.desiredNumShips = 1
        self.acceptOnce('startShardActivity', self.died)

    def died(self):
        taskMgr.doMethodLater(random.random() * 7, self.__checkShips, self.uniqueName('checkShips'))

    def __checkShips(self, task):
        deadShips = []
        for doId, ship in self.ships.items():
            if ship.isDeleted():
                deadShips.append(doId)

        for doId in deadShips:
            del self.ships[doId]

        # Upkeep population
        numShips = len(self.ships)
        if numShips < self.desiredNumShips:
            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            ship = self.shipClass.makeFromObjectKey(self.shipClass, self, uid, self.data)
            self.spawner.spawn(ship)
            self.ships[ship.doId] = ship

        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class DistributedEnemySpawnerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawnerAI')
    _avatarMissing = set() # Debug
    _shipMissing = set() # Debug
    _animalMissing = set() #Debug

    def __init__(self, gameArea):
        self.gameArea = gameArea
        self.air = self.gameArea.air

        self.spawnNodes = {}

    def addEnemySpawnNode(self, objKey, data):
        self.spawnNodes[objKey] = EnemySpawnNode(self, data)

    def addAnimalSpawnNode(self, objKey, data):
        self.spawnNodes[objKey] = AnimalSpawnNode(self, data)

    def addShipSpawnNode(self, objKey, data):
        self.spawnNodes[objKey] = ShipSpawnNode(self, data)

    def spawnNavy(self, objKey, data):
        npc = DistributedNPCPirateAI.makeFromObjectKey(None, self, objKey, data)
        self.spawn(npc, False)
        return npc

    def spawnMarine(self, objKey, data):
        npc = DistributedNPCNavySailorAI.makeFromObjectKey(None, self, objKey, data)
        self.spawn(npc, False)
        return npc

    def spawnNPC(self, objKey, data):
        npc = DistributedNPCTownfolkAI.makeFromObjectKey(None, self, objKey, data)
        self.spawn(npc, False)
        return npc

    def spawn(self, npc, setLevel=True):
        if not npc.getLevel():
            if setLevel:
                npc.setLevel(0) # Random

        self.gameArea.generateChild(npc)

    @classmethod
    def missingAvatarClass(cls, avType):
        cls._avatarMissing.add(avType)

    @classmethod
    def printMissingAvatarTypes(cls):
        if not cls._avatarMissing:
            return

        cls.notify.warning('Missing avatar types:')
        for avType in cls._avatarMissing:
            print '   %r' % avType

        del cls._avatarMissing

    @classmethod
    def missingShipClass(cls, shipType):
        cls._shipMissing.add(shipType)

    @classmethod
    def printMissingShipTypes(cls):
        if not cls._shipMissing:
            return

        cls.notify.warning('Missing ship types:')
        for shipType in cls._shipMissing:
            print '   %r' % shipType

        del cls._shipMissing   

    @classmethod
    def missingAnimalClass(cls, avType):
        cls._animalMissing.add(avType)

    @classmethod
    def printMissingAnimalTypes(cls):
        if not cls._animalMissing:
            return

        cls.notify.warning('Missing animal types:')
        for avType in cls._animalMissing:
            print '   %r' % avType

        del cls._animalMissing 

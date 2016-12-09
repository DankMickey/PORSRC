from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pirates.inventory.DistributedLootContainerAI import DistributedLootContainerAI
from pirates.inventory import DropGlobals
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
import random

class LootManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootManagerAI')

    def __init__(self, air):
        self.air = air
        self.containers = {}
        
        self.forceType = config.GetInt('force-loot-chest', 0)

        if self.forceType > 0:
            self.notify.info("Launching with force-loot-chest active. Forcing to type: %s" % self.forceType)

        self.accept('goingOffline', self.__goingOffline)
        self.accept('containerDied', self.deleteContainer)
        taskMgr.doMethodLater(15, self.__removeContainers, 'purgeContainers')

    def spawnLoot(self, npc):
        if not config.GetBool('want-loot', False):
            return

        self.notify.info("Attempting to spawn loot")

        try:
            enemyLevel = npc.getLevel()
            players = npc.enemySkills.keys()
            enemyGrade = self.getEnemyGradeFromLevels(enemyLevel, players)
            dropRate = DropGlobals.getContainerDropRate(enemyGrade)
            
            print 'Enemy level %s Players %s Enemy Grade %s Drop Rate %s' % (enemyLevel, players, enemyGrade, dropRate)

            if not random.randrange(100) > dropRate and not config.GetBool('always-spawn-loot', True):
                print 'Oh well. Not spawning.'
                return

            chestType = self.getChestTypeFromEnemyLevel(enemyLevel)
            plunder = self.getContainerPlunder(chestType, npc)

            container = DistributedLootContainerAI.makeFromObjectData(self.air, npc, type=chestType, plunder=plunder)
            container.setTimeout(config.GetInt('loot-timeout', 120))

            self.containers[container.doId] = container
            self.notify.info("Spawned Loot Container of type(%s). Contains: %s" % (chestType, plunder))
        except Exception, e:
             self.notify.warning("Failed to spawn Loot. An unknown error has occured")
             self.notify.warning(e)

    def getChestTypeFromEnemyLevel(self, enemyLevel):
        if self.forceType > 0:
            return self.forceType

        sacRate, chestRate, rareRate = DropGlobals.getContainerTypeRate(enemyLevel)
        rareRate = 100 - rareRate
        chestRNG = random.randrange(100)

        if chestRNG < sacRate:
            return PiratesGlobals.ITEM_SAC
        elif chestRNG >= sacRate and chestRNG <= rareRate:
            return PiratesGlobals.TREASURE_CHEST
        elif chestRNG >= rareRate:
            return PiratesGlobals.RARE_CHEST
        else:
            return PiratesGlobals.ITEM_SAC

    def getEnemyGradeFromLevels(self, npcLevel, players):
        return EnemyGlobals.GREEN #TODO

    def getContainerPlunder(self, containerType, npc):
        enemyItems = DropGlobals.getEnemyDropItemsByType(npc.avatarType, npc.getUniqueId())

        crudeRate, commonRate, rareRate, famedRate, legendaryRate = DropGlobals.getItemRarityRate(containerType)
        swordRate, gunRate, dollRate, daggerRate, grenadeRate, staffRate, cannonRate = DropGlobals.getItemTypeRate(containerType)
        weaponRate, charmRate, consumableRate, clothingRate, jewelryRate, tattooRate = DropGlobals.getNumItemsRate(containerType)

        numItems = 5 #TODO

        plunder = []
        for item in enemyItems:

            categoryId = -1 #TODO
            extraArg = 0 #TODO
            typeCheck = False #TODO

            if item == 1:
                self.notify.info("SPAWNING 1!")
                categoryId = 1
                typeCheck = True

            if len(plunder) <= numItems and categoryId >= 0 and typeCheck:
                plunderItem = [categoryId, item, extraArg]
                plunder.append(plunderItem)

        return plunder

    def __removeContainers(self, task):
        garbage = []

        for containerId, container in self.containers.iteritems():
            container.tick(task.time)
            timeout = container.getTimeout()

            if container.getEmpty() or container.getTimeout() <= 0 or not container.locks:
                garbage.append(containerId)
        
        for containerId in garbage:
            self.notify.info("Deleting Loot Container: %s" % containerId)
            self.deleteContainer(containerId)

        return task.again

    def deleteContainer(self, containerId):
        if containerId not in self.containers:
            print 'Container missing?'
            return

        container = self.containers[containerId]
        container.delete()
        del self.containers[containerId]

    def __goingOffline(self, avId):
        for container in [container for container in self.containers.values() if avId in container.getCreditLocks()]:
            container.removePirateFromCreditLock(avId)
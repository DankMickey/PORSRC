from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task
from pirates.inventory.DistributedLootContainerAI import DistributedLootContainerAI
from pirates.inventory import DropGlobals
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
import random

class DistributedLootManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.containers = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.forceType = config.GetInt('force-loot-chest', 0)
        if self.forceType > 0:
            self.notify.info("Launching with force-loot-chest active. Forcing to type: %s" % self.forceType)

        self.purgeContainers = taskMgr.doMethodLater(15, self.__removeContainers, 'purgeContainers')

    def delete(self):
        DistributedObjectAI.delete(self)
        taskMgr.remove(self.purgeContainers)
        
        for containerId in self.containers:
            self.deleteContainer(containerId)

    def spawnLoot(self, npc):
        if not config.GetBool('want-loot', False):
            return 

        self.notify.info("Attempting to spawn loot")
        try:
            enemyLevel = npc.getLevel()
            players = npc.enemySkills.keys()
            enemyGrade = self.getEnemyGradeFromLevels(enemyLevel, players)
            dropRate = DropGlobals.getContainerDropRate(enemyGrade)
            if not random.randrange(100) > dropRate and not config.GetBool('always-spawn-loot', True):
                return

            chestType = self.getChestTypeFromEnemyLevel(enemyLevel)
            plunder = self.getContainerPlunder(chestType, npc)

            container = DistributedLootContainerAI.makeFromObjectData(self.air, npc, type=chestType, plunder=plunder)
            container.setTimeout(config.GetInt('loot-timeout', 600))

            self.containers[container.getUniqueId()] = container
            self.notify.info("Spawned Loot Container of type(%s). Contains: %s" % (chestType, plunder))
        except Exception, e:
             self.notify.warning("Failed to spawn Loot. An unknown error has occured")
             self.notify.warning(e)

    def getChestTypeFromEnemyLevel(self, enemyLevel):
        sacRate, chestRate, rareRate = DropGlobals.getContainerTypeRate(enemyLevel)
        rareRate = 100 - rareRate
        chestRNG = random.randrange(100)
        chestType = PiratesGlobals.ITEM_SAC
        if chestRNG < sacRate:
            chestType = PiratesGlobals.ITEM_SAC
        elif chestRNG >= sacRate and chestRNG <= rareRate:
            chestType = PiratesGlobals.TREASURE_CHEST
        elif chestRNG >= rareRate:
            chestType = PiratesGlobals.RARE_CHEST

        if self.forceType > 0:
            chestType = self.forceType

        return chestType

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

    def sendContainerRemoveWarning(self, containerId):
        self.sendUpdate('warnRemoveLootContainerFromScoreboard', [containerId])

    def sendContainerRemove(self, containerId):
        self.sendUpdate('removeLootContainerFromScoreboard', [containerId])

    def __removeContainers(self, task=None):
        garbage = []

        for containerId, container in self.containers.iteritems():
            container.tick()
            timeout = container.getTimeout()
            
            if timeout < 600 and timeout > 0:
                self.sendContainerRemoveWarning(container.doId)

            if container.getEmpty() or container.getTimeout() <= 0 or len(container.locks) <= 0:
                garbage.append(containerId)
        
        for containerId in garbage:
            self.notify.info("Deleting Loot Container: %s" % containerId)
            self.deleteContainer(containerId)

        return Task.again

    def deleteContainer(self, containerId):
        self.sendContainerRemove(self.containers[containerId].doId)
        self.containers[containerId].delete()
        del self.containers[containerId]

    def requestItemFromContainer(self, containerId, itemInfo):
        self.notify.info("requestItemFromContainer. containerId: %s itemInfo: %s" % (containerId, itemInfo))

    def requestItems(self, containers): 
        self.notify.info("requestItems. containers: %s" % containers)

    def pirateWentOffline(self, avatarId): #TODO FIX
        for containerId, container in self.containers.iteritems():
            if avatarId in container.getCreditLocks():
                self.notify.info("Removing %s from container: %s" % (avatarId, containerId))
                container.removePirateFromCreditLock(avatarId)
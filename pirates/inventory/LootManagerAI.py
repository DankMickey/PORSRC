from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pirates.inventory.DistributedLootContainerAI import DistributedLootContainerAI
from pirates.inventory import DropGlobals, ItemGlobals
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
import random

ItemTypes = [InventoryType.ItemTypeWeapon, InventoryType.ItemTypeClothing, InventoryType.ItemTypeClothing, InventoryType.ItemTypeClothing, InventoryType.ItemTypeWeapon, InventoryType.ItemTypeWeapon]
#ItemTypes = [InventoryType.ItemTypeWeapon, InventoryType.ItemTypeConsumable, InventoryType.ItemTypeCharm, InventoryType.ItemTypeClothing, InventoryCategory.CARDS, InventoryCategory.WEAPON_PISTOL_AMMO]

class LootManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootManagerAI')

    def __init__(self, air):
        self.air = air
        self.containers = {}
        
        self.forceType = config.GetInt('force-loot-chest', 0)

        self.accept('goingOffline', self.__goingOffline)
        self.accept('containerDied', self.deleteContainer)
        taskMgr.doMethodLater(15, self.__removeContainers, 'purgeContainers')

    def spawnLoot(self, npc):
        if not config.GetBool('want-loot', False):
            return

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
            container.setTimeout(config.GetInt('loot-timeout', 120))

            self.containers[container.doId] = container
        except Exception, e:
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
        return EnemyGlobals.GREEN

    def getRandomItem(self, enemyItems, itemRarities, itemTypes):
        itemRarity = self.chooseFromRate(itemRarities)
        itemType = ItemTypes[self.chooseFromRate(itemTypes)]

        random.shuffle(enemyItems)
            
        for itemId in enemyItems:
            if ItemGlobals.getClass(itemId) == itemType and ItemGlobals.getRarity(itemId) == itemRarity:
                return (itemType, itemId, 1)
    
    def chooseFromRate(self, rates):
        rolled = random.uniform(0, 1)
        
        for i, rate in enumerate(rates):
            if rate <= rolled:
                return i
        
        return 0
        
    def getContainerPlunder(self, containerType, npc):
        enemyItems = DropGlobals.getEnemyDropItemsByType(npc.avatarType, npc.getUniqueId())

        itemRarities = DropGlobals.getItemRarityRate(containerType)
        itemTypes = DropGlobals.getItemTypeRate(containerType)
        itemRate = self.chooseFromRate(DropGlobals.getNumItemsRate(containerType)) + 1
        items = []
        
        if random.random() >= 0.8:
            gold = random.randint(*DropGlobals.getItemGoldRate(containerType))
            items.append((InventoryType.ItemTypeMoney, 0, gold))
            itemRate -= 1
        
        for i in xrange(itemRate):
            item = self.getRandomItem(enemyItems, itemRarities, itemTypes)
            
            if item:
                items.append(item)

        return items

    def __removeContainers(self, task):
        garbage = []

        for containerId, container in self.containers.iteritems():
            container.tick(15)
            timeout = container.getTimeout()

            if container.getEmpty() or container.getTimeout() <= 0 or not container.locks:
                garbage.append(containerId)
        
        for containerId in garbage:
            self.deleteContainer(containerId)

        return task.again

    def deleteContainer(self, containerId):
        if containerId not in self.containers:
            return

        container = self.containers[containerId]
        container.deleteContainer()
        del self.containers[containerId]

    def __goingOffline(self, avId):
        for container in [container for container in self.containers.values() if avId in container.getCreditLocks()]:
            container.removePirateFromCreditLock(avId)
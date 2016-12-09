from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.GridParent import GridParent
from pirates.distributed.DistributedInteractiveAI import *
from pirates.inventory.LootableAI import LootableAI
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
import copy, os

class DistributedLootContainerAI(DistributedInteractiveAI, LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        LootableAI.__init__(self, air)
        self.vizZone = ''
        self.lootType = PiratesGlobals.ITEM_SAC
        self.locks = []
        self.empty = False
        self.timeout = 36000
        self.avatarType = None
        self.avatarLevel = 0
        self.plunder = {}
    
    def delete(self):
        DistributedInteractiveAI.delete(self)
        taskMgr.remove(self.uniqueName('deleteContainer'))

    def setVisZone(self, vizZone):
        self.vizZone = vizZone

    def getVisZone(self):
        return self.vizZone

    def setType(self, type):
        self.lootType = type

    def getType(self):
        return self.lootType

    def setEmpty(self, empty):
        self.empty = empty

    def d_setEmpty(self, empty):
        self.sendUpdate('setEmpty', [empty])

    def b_setEmpty(self, empty):
        self.setEmpty(empty)
        self.d_setEmpty(empty)
    
    def f_setEmpty(self, avId, empty):
        self.sendUpdateToAvatarId(avId, 'setEmpty', [empty])

    def getEmpty(self):
        return self.empty

    def setCreditLocks(self, locks):
        self.locks = locks

    def getCreditLocks(self):
        return self.locks
    
    def deleteContainer(self):
        if not taskMgr.hasTaskNamed(self.uniqueName('deleteContainer')):
            self.b_setEmpty(True)
            taskMgr.doMethodLater(1.5, lambda task: self.requestDelete(), self.uniqueName('deleteContainer'))
    
    def removePirateFromCreditLock(self, avatarId):
        if avatarId in self.plunder:
            del self.plunder[avatarId]
            self.f_setEmpty(avatarId, True)

        if avatarId in self.locks:
            self.locks.remove(avatarId)
            
            if not self.locks:
                messenger.send('containerDied', [self.doId])

    def setTimeout(self, timeout):
        self.timeout = timeout

    def tick(self, amount):
        self.timeout -= amount

    def getTimeout(self):
        return self.timeout
    
    def setAvatarType(self, avatarType):
        self.avatarType = avatarType
    
    def getAvatarType(self):
        return self.avatarType
    
    def setAvatarLevel(self, avatarLevel):
        self.avatarLevel = avatarLevel
    
    def getAvatarLevel(self):
        return self.avatarLevel
    
    def posControlledByCell(self):
        return False

    def setPlunder(self, plunder):
        self.plunder = {avId: copy.deepcopy(plunder) for avId in self.locks}

    def getPlunder(self):
        return self.plunder

    def startLooting(self, avId, timer):
        self.sendUpdateToAvatarId(avId, 'startLooting', [self.plunder[avId], timer])
    
    def handleInteract(self, avId, interactType, instant):
        if avId not in self.locks:
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), message='Client bypassed lock check and tried to interact with DistributedLootContainerAI')
            return REJECT

        if avId not in self.plunder or not self.plunder[avId]:
            return REJECT

        self.startLooting(avId, 0)
        return ACCEPT | ACCEPT_SEND_UPDATE
    
    def requestItem(self, item):
        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.locks or avId not in self.plunder:
            return
        
        items = self.plunder[avId]
        
        if item not in items:
            return

        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        del self.plunder[avId][items.index(item)]
        
        if not self.plunder[avId]:
            self.removePirateFromCreditLock(avId)

        self.giveItem(av, item)

    def requestItems(self):
        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.locks or avId not in self.plunder:
            return
        
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        items = self.plunder[avId]
        
        for item in items:
            self.giveItem(av, item)
        
        self.removePirateFromCreditLock(avId)
    
    def giveItem(self, av, item):
        itemClass, itemId, amount = item
        
        if itemClass == InventoryType.ItemTypeMoney:
            av.giveGold(amount)
            return
        
        inv = av.getInventory()
        
        if not inv:
            return

        location = inv.findAvailableLocation(itemClass, itemId=itemId, count=amount, equippable=True)
        
        if location != -1:
            inv.addLocatable(itemId, location, amount, inventoryType=itemClass)

    @staticmethod
    def makeFromObjectData(air, npc, type=PiratesGlobals.ITEM_SAC, plunder=[]):
        obj = DistributedLootContainerAI(air)
        obj.setCreditLocks(npc.enemySkills.keys())
        obj.setAvatarType(npc.avatarType)
        obj.setAvatarLevel(npc.getLevel())
        obj.setType(type)
        obj.setPlunder(plunder)

        if not plunder:
            obj.setEmpty(True)
        
        area = npc.getParentObj()
        cell = GridParent.getCellOrigin(area, npc.zoneId)
        
        obj.setPos(npc.getPos(cell))
        obj.setHpr(npc.getHpr())
        obj.generateWithRequiredAndId(air.allocateChannel(), area.doId, npc.zoneId)
        obj.sendUpdate('setPos', list(obj.getPos()))

        return obj
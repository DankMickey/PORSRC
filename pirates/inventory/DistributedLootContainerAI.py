from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.GridParent import GridParent
from pirates.distributed.DistributedInteractiveAI import *
from pirates.inventory.LootableAI import LootableAI
from pirates.piratesbase import PiratesGlobals
#from pirates.inventory.InventoryUIPlunderGridContainer import InventoryUIPlunderGridContainer
import os

class DistributedLootContainerAI(DistributedInteractiveAI, LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        LootableAI.__init__(self, air)
		#InventoryUIPlunderGridContainer.__init__.(self, air)
        self.vizZone = ''
        self.lootType = PiratesGlobals.ITEM_SAC
        self.locks = []
        self.empty = False
        self.timeout = 36000
        self.avatarType = None
        self.avatarLevel = 0
        self.plunder = []

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

    def getEmpty(self):
        return self.empty

    def setCreditLocks(self, locks):
        self.locks = locks

    def getCreditLocks(self):
        return self.locks

    def removePirateFromCreditLock(self, avatarId):
        if avatarId in self.locks:
            self.locks.remove(avatarId)

    def setTimeout(self, timeout):
        self.timeout = timeout

    def tick(self, amount=15):
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
        self.plunder = plunder

    def getPlunder(self):
        return self.plunder

    def startLooting(self, avId, avType, avLevel):
        LootableAI.startLooting(self, avId, self.plunder, len(self.plunder), 0)
    
    def handleInteract(self, avId, interactType, instant):
        if avId not in self.locks:
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), message='Client bypassed lock check and tried to interact with DistributedLootContainerAI')
            return REJECT
        
        #return REJECT
        self.startLooting(avId, self.avatarType, self.avatarLevel)
        return ACCEPT | ACCEPT_SEND_UPDATE

    @staticmethod
    def makeFromObjectData(air, npc, type=PiratesGlobals.ITEM_SAC, plunder=[]):
        obj = DistributedLootContainerAI(air)
        obj.setUniqueId("%s-lootcontainer-%s" % (npc.getUniqueId(), os.urandom(4).encode('hex')))
        obj.setCreditLocks(npc.enemySkills.keys())
        obj.setAvatarType(npc.avatarType)
        obj.setAvatarLevel(npc.getLevel())
        obj.setType(type)
        obj.setPlunder(plunder)

        if len(plunder) <= 0:
            obj.setEmpty(True)
        
        area = npc.getParentObj()
        cell = GridParent.getCellOrigin(area, npc.zoneId)
        
        obj.setPos(npc.getPos(cell))
        obj.setHpr(npc.getHpr())
        obj.generateWithRequiredAndId(air.allocateChannel(), area.doId, npc.zoneId)
        obj.sendUpdate('setPos', list(obj.getPos()))

        return obj
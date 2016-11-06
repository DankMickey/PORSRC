from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.GridParent import GridParent
from pirates.distributed.DistributedInteractiveAI import *
from pirates.inventory.LootableAI import LootableAI
from pirates.piratesbase import PiratesGlobals

class DistributedLootContainerAI(DistributedInteractiveAI, LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        LootableAI.__init__(self, air)
        self.vizZone = ''
        self.lootType = PiratesGlobals.ITEM_SAC
        self.locks = []
        self.empty = False
        self.timeout = 0
        self.avatarType = None
        self.avatarLevel = 0

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
    
    def startLooting(self, avId, avType, avLevel):
        # TODO
        pass
    
    def handleInteract(self, avId, interactType, instant):
        if avId not in self.locks:
            return REJECT
        
        self.startLooting(avId, self.avatarType, self.avatarLevel)
        return ACCEPT | ACCEPT_SEND_UPDATE

    @staticmethod
    def makeFromObjectData(air, npc):
        obj = DistributedLootContainerAI(air)
        obj.setUniqueId(npc.getUniqueId() + "-lootcontainer")
        obj.setCreditLocks(npc.enemySkills.keys())
        obj.setAvatarType(npc.avatarType)
        obj.setAvatarLevel(npc.getLevel())
        
        area = npc.getParentObj()
        cell = GridParent.getCellOrigin(area, npc.zoneId)
        
        obj.setPos(npc.getPos(cell))
        obj.generateWithRequiredAndId(air.allocateChannel(), area.doId, npc.zoneId)
        obj.sendUpdate('setPos', list(obj.getPos()))

        return obj
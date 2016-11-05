from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
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

    @staticmethod
    def makeFromObjectData(air, npc):
        obj = DistributedLootContainerAI(air)
        obj.setUniqueId(npc.getUniqueId() + "-lootcontainer")
        obj.setPos(npc.getPos())
        obj.setHpr(npc.getHpr())
        return obj
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

class DistributedShipLoaderUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)


    def initPlayerShip(self, avId, shipId, shipName):
        self.notify.warning("Insert creation code here.")


from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class LootableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('LootableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    # startLooting(PlunderListItem [], int8, uint8, bool)
    def startLooting(self, avId, plunderInfo, itemsToTake=0, timer=0, autoShow=False):
        self.notify.info("startLooting. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
        self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, itemsToTake, timer, autoShow])

    # stopLooting()
    def stopLooting(self):
        self.notify.info("stopLooting.")

    # doneTaking() airecv clsend
    def doneTaking(self):
        self.notify.info("doneTaking.")

    # requestItem(PlunderItemLocationInfo) airecv clsend
    def requestItem(self, plunderLocationInfo):
        self.notify.info("requestItem. plunderLocationInfo: %s" % plunderLocationInfo)

    # requestItems(PlunderItemInfo []) airecv clsend
    def requestItems(self, pluderInfo):
        self.notify.info("requestItems. plunderInfo: %s" % plunderInfo)



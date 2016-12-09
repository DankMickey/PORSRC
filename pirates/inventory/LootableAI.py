from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class LootableAI(DistributedObjectAI):
    notify = directNotify.newCategory('LootableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
     
    def startLooting(self, avId, plunderInfo, timer=0):
        self.notify.info("startLooting. plunderInfo: %s timer: %s" % (plunderInfo, timer))
        self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, timer])

    def stopLooting(self):
        self.notify.info("stopLooting Sent ")

    def doneTaking(self):
        self.notify.info("doneTaking Sent ")

    def requestItem(self, item):
        self.notify.info("requestItem. item: %s" % (item,))

    def requestItems(self):
        self.notify.info("requestItems.")

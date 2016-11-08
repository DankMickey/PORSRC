from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.BossAI import BossAI

class DistributedBossSkeletonAI(DistributedNPCSkeletonAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossSkeletonAI')

    def __init__(self, air):
        DistributedNPCSkeletonAI.__init__(self, air)
        BossAI.__init__(self, air)

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        avType.setBoss(True)
        obj = DistributedNPCSkeletonAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['DNA'], avType)
        return obj
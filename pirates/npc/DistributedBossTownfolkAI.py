from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.npc.BossAI import BossAI

class DistributedBossTownfolkAI(DistributedNPCTownfolkAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossTownfolkAI')

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        obj = DistributedGhostAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['objKey'], avType)
        obj.setDNAId(data['objKey'])
        return obj
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI

class DistributedBossNavySailorAI(DistributedNPCNavySailorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCNavySailorAI')

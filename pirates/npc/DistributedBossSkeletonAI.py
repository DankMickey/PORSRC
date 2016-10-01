from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI

class DistributedBossSkeletonAI(DistributedNPCSkeletonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossSkeletonAI')

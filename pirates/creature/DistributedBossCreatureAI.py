from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI

class DistributedBossCreatureAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCreature')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
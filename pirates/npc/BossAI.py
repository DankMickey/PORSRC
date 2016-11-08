from direct.directnotify import DirectNotifyGlobal
from pirates.npc.BossBase import BossBase
from pirates.npc.BossNPCList import BOSS_NPC_LIST

class BossAI(BossBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossAI')

    def __init__(self, air):
        self.air = air

    def _getDefaultValue(self, key):
        return BOSS_NPC_LIST[''][key]

    def _getScale(self):
        return self.bossData['ModelScale']

    def _getDamageScale(self):
        return self.bossData['DamageScale']

    def _setupBossValues(self, uid, avType):
        self.loadBossData(uid, avType)

        scale = self._getScale()
        self.setScale(scale, scale, scale)
        self.setName(self.getNameText())
        self.setDamageScale(self._getDamageScale())

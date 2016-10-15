from direct.directnotify import DirectNotifyGlobal
from pirates.distributed import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals

class DistributedGameTableAI(DistributedInteractiveAI.DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.tableType = 1
        self.gameVariation = 1
        self.dealerName = 'Dealer'
        self.aiList = []

    def handleInteraction(self):
        return ACCEPT # gonna return it as accept, will need to have checks soon

    def setTableType(self, type):
        self.tableType = type

    def getTableType(self):
        return self.tableType

    def setGameVariation(self, variant):
        self.gameVariation = variant

    def getGameVariation(self):
        return self.gameVariation

    def setDealerName(self, name):
        self.dealerName = name

    def getDealerName(self):
        return self.dealerName

    def setDealerType(self, type):
        self.dealerType = type

    def getDealerType(self):
        return PiratesGlobals.VILLAGER_TEAM

    def setAIList(self, list):
        self.aiList = list

    def getAIList(self):
        return self.aiList

    def requestSeat(self, todo0, todo1):
        pass

from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *
import DistributedGameTableAI

class DistributedPokerTableAI(DistributedGameTableAI.DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPokerTableAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.gameType = ''
        self.betMultiplier = 1
        self.anteList = []
        self.posSize = 0
        self.tableState = (0, 0, [], [], [], [0, 0, 0, 0, 0, 0, 0, 0])

    def announceGenerate(self):
        DistributedPokerTableAI.announceGenerate(self)

    def delete(self):
        DistributedPokerTableAI.delete(self) 

    def handleInteract(self, avId, interactType, instant):
        return REJECT #TODO

    def setGameType(self, gameType):
        self.gameType = gameType

    def getGameType(self):
        return self.gameType

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = multiplier

    def getBetMultiplier(self):
        return self.betMultiplier

    def setAnteList(self, list):
        self.anteList = list

    def getAnteList(self):
        return self.anteList

    def setTableState(self, round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount):
        self.tableState = (round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount)

    def getTableState(self):
        return self.tableState

    def setPotSize(self, potSize):
        self.potSize = potSize

    def getPotSize(self):
        return self.potSize

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setGameType(data.get('Category', 'Holdem'))
        obj.setBetMultiplier(int(data.get('BetMultiplier', '1')))
        return obj
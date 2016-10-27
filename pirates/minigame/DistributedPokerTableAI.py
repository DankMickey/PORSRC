from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.piratesbase import PiratesGlobals
import random


class DistributedPokerTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPokerTableAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.potSize = 0
        self.anteList = []
        self.tableState = (0, 0, [], [], [], [0, 0, 0, 0, 0, 0, 0, 0])

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)

    def delete(self):
        DistributedGameTableAI.delete(self)

    def handleInteract(self, avId, interactType, instant):
        if config.GetBool('want-tables-closed', False):
            msg = 'Client bypassed sanity check and called DistributedPokerTableAI'
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), message=msg)
            return REJECT
        
        return REJECT

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

    def generatePlayers(self, seats=7, ai=3, available=[PiratesGlobals.VILLAGER_TEAM]):
        players = [0] * seats

        randomGen = random.Random()
        randomGen.seed(self.getUniqueId()) 

        if (ai > seats):
            self.notify.warning("Cannot have more ai then seats! reducing to 5")
            ai = 5

        for i in range(0, ai):
            aiType = randomGen.choice(available)
            players[i] = aiType

        randomGen.shuffle(players)
        self.setAIList(players)

    def posControlledByCell(self):
        return True

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedGameTableAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setGameType(data.get('Category', 'Holdem'))
        obj.setBetMultiplier(int(data.get('BetMultiplier', '1')))
        obj.generatePlayers()
        return obj
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.holidayIdList = []
        self.newPathList = []

    def holidayNotify(self):
        pass

    def getHolidayIdList(self, holidayIdList):
        return self.holidayIdList

    def setHolidayIdList(self, holidayIdList):
        self.holidayIdList = holidayIdList

    def d_setHolidayIdList(self, holidayIdList):
        self.sendUpdate('setHolidayIdList', [holidayIdList])

    def b_setHolidayIdList(self, holidayIdList):
        self.setHolidayIdList(holidayIdList)
        self.d_setHolidayIdList(holidayIdList)

    def addActiveHoliday(self, holidayId, time):
        self.holidayIdList.append((holidayId, time))
        self.b_setHolidayIdList(self.holidayId)

    def displayMessage(self, messageId):
        self.sendUpdate('displayMessage', [messageId])

    def playMusic(self, musicInfo):
        self.sendUpdate('playMusic', [musicInfo])

    def setNoteablePathList(self, newPathList):
        self.newPathList = newPathList

    def d_setNoteablePathList(self, newPathList):
        self.sendUpdate('setNoteablePathList', [newPathList])

    def b_setNoteablePathList(self, newPathList):
        self.setNoteablePathList(newPathList)
        self.d_setNoteablePathList(newPathList)

    def getNoteablePathList(self):
        return self.newPathList

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def newsMsg(messageId):
        """Send a news message to the whole district (system)"""
        air = spellbook.getInvoker().air

        if messageId < 0 or messageId >= 70:
            return "Unable to send debug news message. MessageId must be between 0-69."

        air.newsManager.displayMessage(messageId)
        return "Sent debug news message '%s' to all pirates in the district." % str(messageId)

    @magicWord(CATEGORY_GAME_DEVELOPER)
    def newsMusic(musicName):
        """Send a news music packet to the whole district (system)"""
        air = spellbook.getInvoker().air
        musicInfo = ['']
        musicInfo[0] = musicName
        air.newsManager.playMusic(musicInfo)
        return "Sent debug news music packet '%s' to all pirates in the district." % str(musicName)     


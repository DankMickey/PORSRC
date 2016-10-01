from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from pirates.ai import HolidayGlobals
from pirates.ai.HolidayDates import HolidayDates

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.holidayIdList = []
        self.newPathList = []

        if config.GetBool('want-holiday-dev', False):
            self.forcedHolidays = []

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        if config.GetBool('want-holidays', False):
            self.__checkHolidays()
            self.checkHolidays = taskMgr.doMethodLater(15, self.__checkHolidays, 'holidayCheckTask')

    def delete(self):
        DistributedObjectAI.delete(self)
        if hasattr(self, 'checkHolidays'):
            taskMgr.remove(self.checkHolidays)

    def __checkHolidays(self, task=None):
        holidays = HolidayGlobals.getAllHolidayIds()
        for id in holidays:
            holiday = HolidayGlobals.getHolidayDates(id)
            if not hasattr(holiday, 'getCurrentDate'):
                continue

            if len(holiday.startDates) <= 0:
                continue

            date = holiday.getCurrentDate()
            if hasattr(self, 'forcedHolidays'):
                if id in self.forcedHolidays:
                    self.notify.info("Starting forced holiday with id: %s" % id)
                    self.startHoliday(id)
            elif False: #TODO date check
                if not self.isHolidayRunning(id):
                    self.startHoliday(id)
            else:
                if self.isHolidayRunning(id):
                    self.endHoliday(id)
        return Task.again

    def attemptToRunRandom(self, keyword="Invasion"):
        randoms = HolidayGlobals.RandomizedSchedules
        if keyword in randoms:
            data = randoms[keyword]
            runnable, default = data['configs'][0]
            if not config.GetBool(runnable, default):
                return False
            canStart = True
            if 'conflictingIds' in data:
                for id in data['conflictingIds']:
                    if self.isHolidayRunning(id):
                        canStart = False

            for id in data['holdayIds']:
                if self.isHolidayRunning(id):
                    canStart = False

            if canStart:
                start, end = data['duration']
                holidayId = 0 #TODO finish
                self.notify.info("Starting random '%s'" % keyword)
                self.startHoliday(holdayId, end)
                return True
        return False

    def holidayNotify(self):
        self.notify.info("Received Holiday Notify! I have no idea what im doing. - Disney")

    def isHolidayRunning(self, holidayId):
        return holidayId in self.holidayIdList

    def getHolidayIdList(self):
        return self.holidayIdList

    def setHolidayIdList(self, holidayIdList):
        self.holidayIdList = holidayIdList

    def d_setHolidayIdList(self, holidayIdList):
        self.sendUpdate('setHolidayIdList', [holidayIdList])

    def b_setHolidayIdList(self, holidayIdList):
        self.setHolidayIdList(holidayIdList)
        self.d_setHolidayIdList(holidayIdList)

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

    def startHoliday(self, holidayId, time=0):
        if self.isHolidayRunning(holidayId):
            return

        if not holidayId in HolidayGlobals.getAllHolidayIds():
            self.notify.warning("Failed to start holiday. %s is an invalid holiday Id" % holidayId)
            return

        self.notify.info("Starting holiday: %s" % holidayId)
        self.holidayIdList.append((holidayId, time))
        self.sendUpdate('setHolidayIdList', [self.holidayIdList])

    def endHoliday(self, holidayId):
        if not self.isHolidayRunning(holidayId):
            return
        #TODO write this

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def forceStartHoliday(holidayId):
        """Force starts a holiday for the district"""
        air = spellbook.getInvoker().air
        if not hasattr(air.newsManager, 'forcedHolidays'):
            return "Sorry, holiday dev mode is not enabled on this district"

        if air.newsManager.isHolidayRunning(holidayId):
            return "Sorry, holiday %s is already running" % holdayId

        if not holidayId in HolidayGlobals.getAllHolidayIds():
            return "Sorry, %s is not a valid holiday." % holidayId

        air.newsManager.forcedHolidays.append(holidayId)
        return "Force starting holiday %s for the district" % holidayId

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def forceEndHoliday(holidayId):
        """Stops a force started holiday on the district"""
        air = spellbook.getInvoker().air
        if not hasattr(air.newsManager, 'forcedHolidays'):
            return "Sorry, holiday dev mode is not enabled on this district" 

        if holidayId not in air.newsManager.forcedHolidays:
            return "%s is not currently being run by force." % holidayId

        air.newsManager.forcedHolidays.remove(holidayId)
        return "Stopping force started holiday %s for the district" % holidayId   

    @magicWord(CATEGORY_GAME_DEVELOPER)
    def getHolidays():
        """Gets the active holiday list from the district"""
        air = spellbook.getInvoker().air
        holidays = air.newsManager.getHolidayIdList()
        if len(holidays) <= 0:
            return "No active holidays."

        response = "Active Holidays: "
        for holiday in holidays:
            holdayId, time = holiday
            response = response + " {0}({1})".format(holidayId, time)
        return response

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def newsMsg(messageId):
        """Send a news message to the whole district (system)"""
        air = spellbook.getInvoker().air

        if messageId < 0 or messageId >= 70:
            return "Unable to send debug news message. MessageId must be between 0-69."

        air.newsManager.displayMessage(messageId)
        return "Sent debug news message '%s' to all pirates in the district." % str(messageId)

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[str])
    def newsMusic(musicName):
        """Send a news music packet to the whole district (system)"""
        air = spellbook.getInvoker().air
        musicInfo = ['']
        musicInfo[0] = musicName
        air.newsManager.playMusic(musicInfo)
        return "Sent debug news music packet '%s' to all pirates in the district." % str(musicName)     


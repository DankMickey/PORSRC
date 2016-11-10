from panda3d.core import Notify
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from pirates.ai import HolidayGlobals
from pirates.ai.HolidayDates import HolidayDates
from pirates.audio import SoundGlobals
from pirates.piratesbase import PLocalizer
from datetime import datetime
from random import randint
import random

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.holidayIdList = {}
        self.newPathList = []

        self.randomsDay = {}
        self.randomsMonth = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.wantHolidays = config.GetBool('want-holidays', True)
        if self.wantHolidays:
            self.__checkHolidays()
            self.checkHolidays = taskMgr.doMethodLater(15, self.__checkHolidays, 'holidayCheckTask')
            self.__processHolidayTime()
            self.holidayTime = taskMgr.doMethodLater(15, self.__processHolidayTime, 'holidayTime')

        if config.GetBool('want-auto-messages', True):
            autoCycle = max(config.GetInt('auto-message-cycle', 2700), 60)
            self.__runAutoMessages()
            self.autoMessages = taskMgr.doMethodLater(autoCycle, self.__runAutoMessages, 'autoMessages')

        if self.wantHolidays and config.GetBool('want-random-schedules', False):
            self.__runRandoms()
            self.runRandoms = taskMgr.doMethodLater(15, self.__runRandoms, 'randomSchedules')


    def delete(self):
        DistributedObjectAI.delete(self)
        if hasattr(self, 'checkHolidays'):
            taskMgr.remove(self.checkHolidays)
        if hasattr(self, 'holidayTime'):
            taskMgr.remove(self.holidayTime)
        if hasattr(self, 'autoMessages'):
            taskMgr.remove(self.autoMessages)
        if hasattr(self, 'runRandoms'):
            taskMgr.remove(self.runRandoms)

    def __runAutoMessages(self, task=None):
        messageId = randint(0, (len(PLocalizer.ChatNewsMessages) - 1)) or 0
        if messageId is not None:
            self.displayChatMessage(messageId)
        return Task.again

    def __processHolidayTime(self, task=None):
        garbage = []
        for holiday in self.holidayIdList:
            time = self.holidayIdList[holiday]
            time = max(time - 15, 0)
            if time <= 0:
                garbage.append(holiday)
            else:
                self.holidayIdList[holiday] = time
            self.notify.debug("Processing HolidayId: %s. Time is now %s" % (holiday, time))
        if len(garbage) > 0:
            self.notify.debug("Ending Holidays: %s" % garbage)
            for trash in garbage:
                self.endHoliday(trash)
        self.d_setHolidayIdList(self.buildHolidayList())
        return Task.again

    def __checkHolidays(self, task=None):
        holidays = HolidayGlobals.getAllHolidayIds()
        for id in holidays:
            holiday = HolidayGlobals.getHolidayDates(id)
            if not hasattr(holiday, 'getCurrentDate'):
                continue

            if len(holiday.startDates) <= 0:
                continue

            date = holiday.getCurrentDate()
            if False: #TODO date check
                if not self.isHolidayRunning(id):
                    self.startHoliday(id, time=holiday.getEndTime(0))
        return Task.again

    def __runRandoms(self, task=None):

        #TODO implement counter reset

        for randomized in HolidayGlobals.RandomizedSchedules:
            dice = randint(1, 100)
            if dice < 50:
                continue

            self.notify.debug("Attempting to run %s" % randomized)
            ranType = HolidayGlobals.RandomizedSchedules[randomized]
            configs = ranType['configs']

            canRun = True
            for configOption in configs:
                key, default = configOption
                if not config.GetBool(key, default):
                    canRun = False
                    break

            conflictingIds = ranType['conflictingIds']
            for conflict in conflictingIds:
                if self.isHolidayRunning(conflict):
                    canRun = False
                    break

            holidayIds = ranType['holidayIds']
            for holiday in holidayIds:
                if self.isHolidayRunning(holiday):
                    canRun = False
                    break

            holidayId = random.choice(holidayIds)
            if holidayId in self.randomsDay:
                times = self.randomsDay[holidayId]
                if times >= ranType['numPerDay']:
                    canRun = False

            if self.isHolidayRunning(holidayId):
                canRun = False

            start, end = ranType['duration']
            duration = randint((max(start, 1) * 60), (max(end, 2) * 60))

            if canRun:
                if holidayId in self.randomsDay:
                    self.randomsDay[holidayId] = self.randomsDay[holidayId] + 1
                else:
                    self.randomsDay[holidayId] = 1

                if holidayId in self.randomsMonth:
                    self.randomsMonth[holidayId] = self.randomsMonth[holidayId] + 1
                else:
                    self.randomsMonth[holidayId] = 1

                self.notify.debug("Starting %s" % randomized)
                self.startHoliday(holidayId, duration)

    def holidayNotify(self):
        self.sendUpdate('holidayNotify', [])

    def isHolidayRunning(self, holidayId):
        return holidayId in self.holidayIdList

    def getHolidayIdList(self):
        return self.buildHolidayList()

    def getRawHolidayIdList(self):
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

    def displayChatMessage(self, messageId):
        self.notify.info("Broadcasting Message Id: %s" % messageId)
        self.sendUpdate('displayChatMessage', [messageId])

    def playMusic(self, musicInfo):
        self.sendUpdate('playMusic', [musicInfo])

    def playHolidayMusic(self):
        self.sendUpdate('playHolidayMusic', [])

    def setNoteablePathList(self, newPathList):
        self.newPathList = newPathList

    def d_setNoteablePathList(self, newPathList):
        self.sendUpdate('setNoteablePathList', [newPathList])

    def b_setNoteablePathList(self, newPathList):
        self.setNoteablePathList(newPathList)
        self.d_setNoteablePathList(newPathList)

    def getNoteablePathList(self):
        return self.newPathList

    def buildHolidayList(self):
        holidayList = []
        if len(self.holidayIdList) <= 0:
            return []
        for holiday in self.holidayIdList:
            time = max(self.holidayIdList[holiday], 0)
            holidayList.append([holiday, time])
        return holidayList

    def startHoliday(self, holidayId, time=0):
        if self.isHolidayRunning(holidayId):
            return

        if not holidayId in HolidayGlobals.getAllHolidayIds():
            self.notify.warning("Failed to start holiday. %s is an invalid holiday Id" % holidayId)
            return

        self.notify.info("Starting holiday: %s" % (HolidayGlobals.getHolidayName(holidayId) or holidayId))
        self.holidayIdList[holidayId] = time
        self.d_setHolidayIdList(self.buildHolidayList())
        self.processHolidayStart(holidayId)

        if holidayId == 17:
            self.playHolidayMusic()

        messenger.send('holidayListChanged')

    def processHolidayStart(self, holidayId):
        
        if holidayId in HolidayGlobals.INVASION_HOLIDAYS:
            if self.air.todManager:
                self.air.todManager.setMoonJolly(True)

    def endHoliday(self, holidayId):
        if not self.isHolidayRunning(holidayId):
            return

        self.notify.info("Stopping holiday: %s" % (HolidayGlobals.getHolidayName(holidayId) or holidayId))
        self.holidayIdList[holidayId] = 0
        del self.holidayIdList[holidayId]

        self.d_setHolidayIdList(self.buildHolidayList())
        self.processHolidayEnd(holidayId)

        if holidayId == 17:
            self.playHolidayMusic()

        messenger.send('holidayListChanged')

    def processHolidayEnd(self, holidayId):

        if holidayId in HolidayGlobals.INVASION_HOLIDAYS:
            if self.air.todManager:
                self.air.todManager.setMoonJolly(False)

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int, int])
    def forceStartHoliday(holidayId, time):
        """Force starts a holiday for the district"""
        air = spellbook.getInvoker().air

        if air.newsManager.isHolidayRunning(holidayId):
            return "Sorry, holiday %s is already running" % holidayId

        if not holidayId in HolidayGlobals.getAllHolidayIds():
            return "Sorry, %s is not a valid holiday." % holidayId

        air.newsManager.startHoliday(holidayId, time * 60)
        return "Force starting holiday %s for the district with a time of %s minutes" % (holidayId, time)

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def forceEndHoliday(holidayId):
        """Stops a holiday on the district"""
        air = spellbook.getInvoker().air

        if not air.newsManager.isHolidayRunning(holidayId):
            return "Holiday %s is not currently running on the District." % holidayId

        air.newsManager.endHoliday(holidayId)
        return "Stopping force started holiday %s for the district" % holidayId   

    @magicWord(CATEGORY_GAME_DEVELOPER)
    def getHolidays():
        """Gets the active holiday list from the district"""
        air = spellbook.getInvoker().air
        holidays = air.newsManager.getRawHolidayIdList()
        if len(holidays) <= 0:
            return "No active holidays."

        response = "Active Holidays: "
        for holiday in holidays:
            time = holidays[holiday]
            response = response + " {0}({1})".format(HolidayGlobals.getHolidayName(holiday), time)
        return response

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def isHoliday(holidayId):
        air = spellbook.getInvoker().air
        return air.newsManager.isHolidayRunning(holidayId)
        
    @magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
    def newsMsg(messageId):
        """Send a news message to the whole district (system)"""
        air = spellbook.getInvoker().air

        if messageId < 0 or messageId > 70:
            return "Unable to send debug news message. MessageId must be between 0-70."

        air.newsManager.displayMessage(messageId)
        return "Sent debug news message '%s' to all pirates in the district." % str(messageId)

    @magicWord(CATEGORY_GAME_DEVELOPER, types=[str])
    def newsMusic(musicName):
        """Send a news music packet to the whole district (system)"""
        air = spellbook.getInvoker().air
        musicInfo = ['', 10, 0]
        musicInfo[0] = musicName
        air.newsManager.playMusic(musicInfo)
        return "Sent debug news music packet '%s' to all pirates in the district." % str(musicName)     


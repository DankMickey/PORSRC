from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal
from TimeOfDayManagerBase import TimeOfDayManagerBase
from pirates.piratesbase import TODGlobals
from direct.distributed.ClockDelta import globalClockDelta
from otp.ai.MagicWordGlobal import *
import TODGlobals
import time

class DistributedTimeOfDayManagerAI(DistributedObjectAI, TimeOfDayManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        TimeOfDayManagerBase.__init__(self)
        self.isPaused = False
        self.cycleType = TODGlobals.TOD_REGULAR_CYCLE
        self.cycleSpeed = 1
        self.tempTime = globalClockDelta.getFrameNetworkTime(bits = 32)
        self.startingNetTime = globalClockDelta.networkToLocalTime(self.tempTime)
        self.timeOffset = 0
        self.envSubEntry = []
        self.isJolly = 0
        self.isRain = 0
        self.isStorm = 0
        self.isDarkFog = 0
        self.clouds = 1
        self.fromCurrent = 0
        self.startPhase = 0
        self.targetPhase = 0
        self.targetTime = 0

    def syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.cycleType = cycleType
        self.cycleSpeed = cycleSpeed
        self.startingNetTime = startingNetTime
        self.timeOffset = timeOffset

    def getSyncTOD(self):
        return (self.cycleType, self.cycleSpeed, self.startingNetTime, self.timeOffset)

    def setIsPaused(self, isPaused):
        self.isPaused = isPaused
        self.sendUpdate('setIsPaused', [isPaused])

    def getIsPaused(self):
        return self.isPaused

    def requestSync(self):
        pass #TODO

    def setEnvSubs(self, envSubEntry):
        self.envSubEntry = envSubEntry

    def getEnvSubs(self):
        return self.envSubEntry

    def setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.fromCurrent = fromCurrent
        self.startPhase = startPhase
        self.targetPhase = targetPhase
        self.targetTime = targetTime

    def getMoonPhaseChange(self):
        return (self.fromCurrent, self.startPhase, self.targetPhase, self.targetTime)

    def setMoonJolly(self, isJolly):
        self.isJolly = isJolly
        self.sendUpdate('setMoonJolly', [isJolly])

    def getMoonJolly(self):
        return self.isJolly

    def setRain(self, isRain):
        self.isRain = isRain
        self.sendUpdate('setRain', [isRain])

    def getRain(self):
        return self.isRain

    def setStorm(self, isStorm):
        self.isStorm = isStorm
        self.sendUpdate('setStorm', [isStorm])

    def getStorm(self):
        return self.isStorm

    def setBlackFog(self, isDarkFog):
        self.isDarkFog = isDarkFog
        self.sendUpdate('setBlackFog', [isDarkFog])

    def getBlackFog(self):
        return self.isDarkFog

    def setClouds(self, cloudType):
        self.clouds = cloudType
        self.sendUpdate('setClouds', [cloudType])

    def getClouds(self):
        return self.clouds

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def setRain(state):
    air = spellbook.getInvoker().air
    if air.config.GetBool('advanced-weather', False):
        air.todManager.setRain((state == 1))
        return 'Setting rain state to %s for district.' % state
    return "Sorry, Weather is not enabled on this district."

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def setStorm(state):
    air = spellbook.getInvoker().air
    if air.config.GetBool('advanced-weather', False):
        if air.config.GetBool('want-storm-weather', False):
            air.todManager.setStorm((state == 1))
            return 'Setting storm state to %s for district.' % state
        else:
            return "Sorry, Storms are not enabled on this district."
    return "Sorry, Weather is not enabled on this district."

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def setDarkFog(state):
    air = spellbook.getInvoker().air
    if air.config.GetBool('advanced-weather', False):
        air.todManager.setBlackFog((state == 1))
        return 'Setting dark fog state to %s for district.' % state
    return "Sorry, Weather is not enabled on this district."

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def setClouds(state):
    air = spellbook.getInvoker().air
    if air.config.GetBool('advanced-weather', False):
        air.todManager.setClouds(state)
        return 'Setting cloud state to %s for district.' % state
    return "Sorry, Weather is not enabled on this district."

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def setJollyMoon(state):
    air = spellbook.getInvoker().air
    air.todManager.setMoonJolly((state == 1))
    return "Setting jolly moon state to %s for district." % state
from panda3d.core import Datagram, Point3
from otp.ai.MagicWordGlobal import *
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from pirates.uberdog.PirateInventoryAI import PirateInventoryAI
from pirates.uberdog.UberDogGlobals import *
from pirates.inventory import ItemConstants, ItemGlobals, InventoryGlobals
from pirates.reputation import RepChart
from pirates.battle import WeaponGlobals
from pirates.battle.DistributedBattleAvatarAI import *
from pirates.inventory import ItemGlobals
from pirates.pirate.HumanDNA import HumanDNA
import random
import math

class DummyInventory(PirateInventoryAI):
    doId = 0

    def __init__(self, air):
        air.dclassesByName['DummyInventory'] = air.dclassesByName['PirateInventoryAI']
        PirateInventoryAI.__init__(self, air)

    def sendUpdate(self, *args):
        return

    def sendUpdateToChannel(self, *args):
        return

class DistributedPlayerPirateAI(DistributedBattleAvatarAI, DistributedPlayerAI):
    avatarType = AvatarTypes.Player

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)
        DistributedPlayerAI.__init__(self, air)

        self.inventory = DummyInventory(air)
        self.levelBuff = {}
        self.penaltyStartTime = 0
        self.gameState = ''

        self.returnLocation = ''
        self.jailCell = None
        self.underArrest = 0
        self.inventoryId = 0
        self.founder = False
        self.allegiance = 0
        self.gmNametag = ('', '')
        self.gmHidden = False
        self.defaultShard = 0
        self.tempdoublexp = 0
        self.zombied = (0, False)
        self.shipHat = 0
        self.luck = 0
        self.maxluck = 0
        self.welcomeWorld = False
        self.badge = (0, 0)
        self.shipIcon = (0, 0)
        self.crewIcon = 0
        self.redeemedCodes = []
        self.style = HumanDNA()
        self.dnaString = ""
        self.guildId = 0
        self.guildName = ""

    def announceGenerate(self):
        DistributedBattleAvatarAI.announceGenerate(self)
        DistributedPlayerAI.announceGenerate(self)
        
        if self.defaultShard != self.air.districtId:
            self.b_setDefaultShard(self.air.districtId)
        
        self.__checkGuildName()
        
        taskMgr.doMethodLater(15, self.__checkCodeExploit, self.taskName('codeTask'))
        taskMgr.doMethodLater(10, self.__healthTask, self.taskName('healthTask'))
        taskMgr.doMethodLater(15, self.__doubleXpTask, self.taskName('doubleXPTask'))

    def getInventory(self):
        return self.inventory

    def gotInventory(self):
        self.repChanged()
    
    def b_setInventoryId(self, inventoryId):
        self.setInventoryId(inventoryId)
        self.d_setInventoryId(inventoryId)
    
    def d_setInventoryId(self, inventoryId):
        self.sendUpdate('setInventoryId', [inventoryId])
    
    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId
    
    def getInventoryId(self):
        return self.inventoryId

    def b_setFounder(self, founder):
        self.setFounder(founder)
        self.d_setFounder(founder)
    
    def d_setFounder(self, founder):
        self.sendUpdate('setFounder', [founder])
    
    def setFounder(self, founder):
        self.founder = founder
    
    def getFounder(self):
        return self.founder
    
    def b_setAllegiance(self, allegiance):
        self.setAllegiance(allegiance)
        self.d_setAllegiance(allegiance)
    
    def d_setAllegiance(self, allegiance):
        self.sendUpdate('setAllegiance', [allegiance])
    
    def setAllegiance(self, allegiance):
        self.allegiance = allegiance
    
    def getAllegiance(self):
        return self.allegiance
    
    def b_setGMNametag(self, color, string):
        self.setGMNametag(color, string)
        self.d_setGMNametag(color, string)
    
    def d_setGMNametag(self, color, string):
        self.sendUpdate('setGMNametag', [color, string])
    
    def setGMNametag(self, color, string):
        self.gmNametag = (color, string)
    
    def getGMNametag(self):
        return self.gmNametag
    
    def b_setGMHidden(self, hidden):
        self.setGMHidden(hidden)
        self.d_setGMHidden(hidden)
    
    def d_setGMHidden(self, hidden):
        self.sendUpdate('setGMHidden', [hidden])
    
    def setGMHidden(self, hidden):
        self.gmHidden = hidden
    
    def getGMHidden(self):
        return self.gmHidden
    
    def b_setDefaultShard(self, defaultShard):
        self.d_setDefaultShard(defaultShard)
        self.setDefaultShard(defaultShard)

    def d_setDefaultShard(self, defaultShard):
        self.sendUpdate('setDefaultShard', [defaultShard])

    def setDefaultShard(self, defaultShard):
        self.defaultShard = defaultShard

    def getDefaultShard(self):
        return self.defaultShard

    def setDNAString(self, dna):
        self.dnaString = dna
        self.style.makeFromNetString(dna)

    def d_setDNAString(self, dna):
        self.sendUpdate('setDNAString', [dna])

    def b_setDNAString(self, dna):
        self.setDNAString(dna)
        self.d_setDNAString(dna)

    def getDNAString(self):
        return self.dnaString

    def getGender(self):
        if self.style != None:
            return self.style.getGender()
        return 'm'

    def setZombie(self, value, cursed=False):
        self.zombied = (value, cursed)

    def d_setZombie(self, value, cursed=False):
        self.sendUpdate('setZombie', [value, cursed])

    def b_setZombie(self, value, cursed=False):
        self.setZombie(value, cursed)
        self.d_setZombie(value, cursed)

    def getZombie(self):
        return self.zombied

    def setTempDoubleXPReward(self, value):
        self.tempdoublexp = value

    def d_setTempDoubleXPReward(self, value):
        self.sendUpdate('setTempDoubleXPReward', [value])

    def b_setTempDoubleXPReward(self, value):
        self.setTempDoubleXPReward(value)
        self.d_setTempDoubleXPReward(value)

    def getTempDoubleXPReward(self):
        return self.tempdoublexp

    def hasTempDoubleXP(self):
        return (self.tempdoublexp > 0)

    def __doubleXpTask(self, task):
        if not self.hasTempDoubleXP():
            return task.again

        self.tempdoublexp -= 15
        if self.tempdoublexp < 0:
            self.tempdoublexp = 0
        self.b_setTempDoubleXPReward(self.tempdoublexp)

        return task.again

    def setOnWelcomeWorld(self, state):
        self.welcomeWorld = state

    def d_setOnWelcomeWorld(self, state):
        self.sendUpdate('setOnWelcomeWorld', [state])

    def b_setOnWelcomeWorld(self, state):
        self.setOnWelcomeWorld(state)
        self.d_setOnWelcomeWorld(state)

    def getOnWorldWorld(self):
        return self.welcomeWorld

    def setBadgeIcon(self, title, rank):
        self.badge = (title, rank)

    def d_setBadgeIcon(self, title, rank):
        self.sendUpdate('setBadgeIcon', [title, rank])

    def b_setBadgeIcon(self, title, rank):
        self.setBadgeIcon(title, rank)
        self.d_setBadgeIcon(title, rank)

    def getBadgeIcon(self):
        return self.badge

    def setShipIcon(self, title, rank):
        self.shipIcon = (title, rank)

    def d_setShipIcon(self, title, rank):
        self.sendUpdate('setShipBadgeIcon', [title, rank])

    def b_setShipIcon(self, title, rank):
        self.setShipIcon(title, rank)
        self.d_setShipIcon(title, rank)

    def getShipIcon(self):
        return self.shipIcon

    def addReputation(self, repId, amount, ignoreDouble=False):
        repAmount = amount
        if self.hasTempDoubleXP() and not ignoreDouble:
            repAmount = repAmount * 2
        self.inventory.addReputation(repId, repAmount)
    
    def repChanged(self):
        newLevel = self.calcLevel()
        levelChanged = newLevel != self.level
        if levelChanged:
            self.b_setLevel(self.calcLevel())

        # TO DO: Endurance bonus
        maxHp = 250
        mana = 50

        for i in xrange(InventoryType.begin_Accumulator, InventoryType.end_Accumulator):
            newLevel = self.calcLevel(i)
            oldLevel = self.levelBuff.get(i, 0)
            if oldLevel and oldLevel != newLevel:
                self.sendUpdate('levelUpMsg', [i, newLevel, 0])
                earnedUnspent, earnedSkill = RepChart.getLevelUpSkills(i, newLevel)
                for eu in earnedUnspent:
                    self.inventory.addStackItem(eu)

                for es in earnedSkill:
                    self.inventory.addStackItem(es)

            self.levelBuff[i] = newLevel
            maxHp += RepChart.getHpGain(i) * (newLevel - 1)
            mana += RepChart.getManaGain(i) * (newLevel - 1)

            if not oldLevel:
                # Ensure they have level 0 and 1 skills
                for es in RepChart.getLevelUpSkills(i, 0)[1] + RepChart.getLevelUpSkills(i, 1)[1]:
                    if not self.inventory.getStackQuantity(es):
                        self.inventory.addStackItem(es)

        self.b_setMaxHp(maxHp)
        self.b_setMaxMojo(mana)

        if levelChanged:
            self.fillHpMeter()

    def addDeathPenalty(self, force=False):
        duration = 5

        if (10 < self.level < 50) or force:
            self.inventory.setStackQuantity(InventoryType.Vitae_Level, 12)
            self.inventory.setStackQuantity(InventoryType.Vitae_Cost, duration)
            self.inventory.setStackQuantity(InventoryType.Vitae_Left, duration)

            self.penaltyStartTime = globalClock.getRealTime()

        self.fillHpMeter()

    def removeDeathPenalty(self):
        self.penaltyStartTime = 0
        self.inventory.setStackQuantity(InventoryType.Vitae_Level, 0)
        self.inventory.setStackQuantity(InventoryType.Vitae_Cost, 0)
        self.inventory.setStackQuantity(InventoryType.Vitae_Left, 0)

    def hasDeathPenalty(self):
        return self.inventory.getStackQuantity(InventoryType.Vitae_Level)

    def calcHpAndMojoLimit(self, hp=None, mojo=None, fill=False):
        mult = .75 if self.hasDeathPenalty() else 1
        hpLimit = self.maxHp * mult
        mojoLimit = self.maxMojo * mult

        if hp is None:
            hp = self.hp

        if mojo is None:
            mojo = self.mojo

        hp = min(hp, hpLimit)
        mojo = min(mojo, mojoLimit)

        if fill:
            hp = hpLimit
            mojo = mojoLimit

        return (hp, mojo)

    def fillHpMeter(self):
        hp, mojo = self.calcHpAndMojoLimit(fill=True)
        self.b_setHp(hp, 1)
        self.b_setMojo(mojo)

    def setHp(self, hp, *args):
        hp, _ = self.calcHpAndMojoLimit(hp=hp)
        DistributedBattleAvatarAI.setHp(self, hp, *args)

    def setMojo(self, mojo):
        _, mojo = self.calcHpAndMojoLimit(mojo=mojo)
        DistributedBattleAvatarAI.setMojo(self, mojo)

    def d_refreshName(self):
        self.sendUpdate('refreshName', [])
    
    def __checkGuildName(self):
        if self.guildName == 'Null':
            self.b_setGuildName('')
            self.d_refreshName()
    
    def __checkCodeExploit(self, task):
        newCodes = []
        changed = False
        
        for code in self.redeemedCodes:
            if code.lower() not in newCodes:
                changed = True
                newCodes.append(code.lower())
        
        if changed:
            self.b_setRedeemedCodes(newCodes)

    def __healthTask(self, task):
        if self.gameState in ('Battle', 'Injured', 'Death'):
            return task.again

        if self.hasDeathPenalty():
            duration = self.inventory.getStackQuantity(InventoryType.Vitae_Cost) * 60
            elapsed = globalClock.getRealTime() - self.penaltyStartTime
            left = math.ceil(int(duration - elapsed) / 60)

            if left <= 0:
                self.removeDeathPenalty()

            elif left != self.inventory.getStackQuantity(InventoryType.Vitae_Left):
                self.inventory.setStackQuantity(InventoryType.Vitae_Left, left)

        else:
            mult = random.randint(6, 13) / 2.0 + .5
            tp = int(self.level * mult)
            self.toonUp(tp)

            # Toon up mojo
            mojo = self.mojo + tp
            self.b_setMojo(mojo)

        return task.again

    def delete(self):
        self.inventory = DummyInventory(self.air)
        taskMgr.remove(self.taskName('codeTask'))
        taskMgr.remove(self.taskName('healthTask'))
        taskMgr.remove(self.taskName('doubleXPTask'))

        self.air.netMessenger.send('goingOffline', [self.doId])
        DistributedBattleAvatarAI.delete(self)
        DistributedPlayerAI.delete(self)

    def calcLevel(self, rep=InventoryType.OverallRep):
        return self.inventory.getCategoryLevel(rep)

    def requestCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        weapons = (x[1] for x in self.inventory.getWeapons().values())
        reason = ItemConstants.REASON_NONE
        msg = ''

        if currentWeapon not in weapons:
            msg = 'tried to use weapon they don\'t own!'
            reason = ItemConstants.REASON_INVENTORY

        else:
            canUse, reason = self.canUseItem((InventoryType.ItemTypeWeapon, currentWeapon))
            if not canUse:
                msg = 'tried to use weapon they cannot!'

        if reason != ItemConstants.REASON_NONE:
            msg += ' weapons = %r, requested = %d, reason = %d' % (weapons, currentWeapon, reason)
            self.notify.warning(msg)
            self.air.writeServerEvent('suspicious', avId=self.doId, message=msg)
            return

        self.b_setCurrentWeapon(currentWeapon, isWeaponDrawn)

    def canUseItem(self, itemTuple):
        canUse = 1
        reason = ItemConstants.REASON_NONE
        itemCat, itemId = itemTuple

        if itemCat == InventoryType.ItemTypeClothing:
            gender = self.style.getGender()
            if gender == 'm' and ItemGlobals.getMaleModelId(itemId) == -1:
                canUse = 0
                reason = ItemConstants.REASON_GENDER

            elif gender == 'f' and ItemGlobals.getFemaleModelId(itemId) == -1:
                canUse = 0
                reason = ItemConstants.REASON_GENDER
        elif itemCat in (InventoryType.ItemTypeWeapon, InventoryType.ItemTypeCharm):
            reqs = self.inventory.getItemRequirements(itemId)
            if reqs == None or filter(lambda x: reqs[x][1] == False, reqs):
                return 0, ItemConstants.REASON_LEVEL

        return (canUse, reason)

    def requestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList,
                             timestamp, pos, charge):
        pos = Point3(pos)
        self.attemptUseTargetedSkill(skillId, ammoSkillId, clientResult, targetId, areaIdList,
                                     timestamp, pos, charge)

    def spendSkillPoint(self, skillId):
        if 0 < self.inventory.getStackQuantity(skillId) < 5:
            unspent = self.getUnspent(skillId)
            
            if not unspent:
                self.notify.warning("Skill ID %s doesn't have an unspent value!" % skillId)
                return

            if self.inventory.getStackQuantity(unspent):
                self.inventory.addStackItem(skillId)
                self.inventory.addStackItem(unspent, -1)
                self.sendUpdate('spentSkillPoint', [skillId])

    def getUnspent(self, rep):
        if InventoryType.begin_WeaponSkillPistol <= rep < InventoryType.end_WeaponSkillPistol:
            return InventoryType.UnspentPistol
        elif InventoryType.begin_WeaponSkillMelee <= rep < InventoryType.end_WeaponSkillMelee:
            return InventoryType.UnspentMelee
        elif InventoryType.begin_WeaponSkillCutlass <= rep < InventoryType.end_WeaponSkillCutlass:
            return InventoryType.UnspentCutlass
        elif InventoryType.begin_WeaponSkillMusket <= rep < InventoryType.end_WeaponSkillMusket:
            return InventoryType.UnspentMusket
        elif InventoryType.begin_WeaponSkillDagger <= rep < InventoryType.end_WeaponSkillDagger:
            return InventoryType.UnspentDagger
        elif InventoryType.begin_WeaponSkillGrenade <= rep < InventoryType.end_WeaponSkillGrenade:
            return InventoryType.UnspentGrenade
        elif InventoryType.begin_WeaponSkillDoll <= rep < InventoryType.end_WeaponSkillDoll:
            return InventoryType.UnspentDoll
        elif InventoryType.begin_SkillSailing <= rep < InventoryType.end_SkillSailing:
            return InventoryType.UnspentSailing
        elif InventoryType.begin_WeaponSkillWand <= rep < InventoryType.end_WeaponSkillWand:
            return InventoryType.UnspentWand
        elif InventoryType.begin_WeaponSkillCannon <= rep < InventoryType.end_WeaponSkillCannon:
            return InventoryType.UnspentCannon
        elif InventoryType.begin_WeaponSkillKettle <= rep < InventoryType.end_WeaponSkillKettle:
            return InventoryType.UnspentKettle
    
    def getUnspentFromRep(self, rep):
        if rep == InventoryType.CutlassRep:
            return InventoryType.UnspentCutlass
        elif rep == InventoryType.DaggerRep:
            return InventoryType.UnspentDagger
        elif rep == InventoryType.PistolRep:
            return InventoryType.UnspentPistol
        elif rep == InventoryType.GrenadeRep:
            return InventoryType.UnspentGrenade
        elif rep == InventoryType.DollRep:
            return InventoryType.UnspentDoll
        elif rep == InventoryType.WandRep:
            return InventoryType.UnspentWand
        elif rep == InventoryType.SailingRep:
            return InventoryType.UnspentSailing
        else:
            return InventoryType.UnspentCannon

    def setGameState(self, state, *args):
        self.gameState = state

        if state == 'ThrownInJail':
            world = self.getWorld()
            if world and self.jailCell:
                x, y, z = self.jailCell.getPos()
                h = self.jailCell.getH()
                world.sendUpdateToAvatarId(self.doId, 'setSpawnInfo', [x, y, z, h, 0, []])

    def requestReturnLocation(self, doId):
        obj = self.air.doId2do.get(doId)
        if hasattr(obj, 'getUniqueId'):
            returnLocation = obj.getUniqueId()
            self.b_setReturnLocation(returnLocation)

    def setReturnLocation(self, location):
        self.returnLocation = location

    def d_setReturnLocation(self, location):
        self.sendUpdate('setReturnLocation', [location])

    def b_setReturnLocation(self, location):
        self.setReturnLocation(location)
        self.d_setReturnLocation(location)
    
    def getReturnLocation(self):
        return self.returnLocation
    
    def setGoldInPocket(self, goldInPocket):
        self.goldInPocket = goldInPocket

    def d_setGoldInPocket(self, goldInPocket):
        self.sendUpdate('setGoldInPocket', [goldInPocket])

    def b_setGoldInPocket(self, goldInPocket):
        self.setGoldInPocket(goldInPocket)
        self.d_setGoldInPocket(goldInPocket)

    def getGoldInPocket(self):
        return self.goldInPocket
    
    def takeGold(self, gold):
        if gold > 0:
            self.b_setGoldInPocket(max(0, self.getGoldInPocket() - gold))
    
    def giveGold(self, gold):
        if gold > 0:
            self.b_setGoldInPocket(min(InventoryGlobals.GOLD_CAP, self.getGoldInPocket() + gold))

    def requestGotoJailWhileInjured(self):
        messenger.send('sendAvToJail', [self])

    def setUnderArrest(self, flag):
        self.underArrest = flag

    def d_setUnderArrest(self, flag):
        self.sendUpdate('setUnderArrest', [flag])

    def b_setUnderArrest(self, flag):
        self.setUnderArrest(flag)
        self.d_setUnderArrest(flag)

    def getUnderArrest(self):
        return self.underArrest

    def setShipHat(self, shipClass):
        self.shipHat = shipClass

    def d_setShiphat(self, shipClass):
        self.sendUpdate('setShipHat', [shipClass])

    def b_setShiphat(self, shipClass):
        self.setShipHat(shipClass)
        self.d_setShiphat(shipClass)

    def getShipHat(self):
        return self.shipHat

    def setRedeemedCodes(self, codes):
        self.redeemedCodes = codes

    def d_setRedeemedCodes(self, codes):
        self.sendUpdate('setRedeemedCodes', [codes])
    
    def b_setRedeemedCodes(self, codes):
        self.setRedeemedCodes(codes)
        self.d_setRedeemedCodes(codes)

    def getRedeemedCodes(self):
        return self.redeemedCodes

    def addRedeemedCode(self, code):
        if code in self.redeemedCodes:
            return
        self.redeemedCodes.append(code)
        self.d_setRedeemedCodes(self.redeemedCodes)

    def removeRedeemedCode(self, code):
        if code not in self.redeemedCodes:
            return
        self.redeemedCodes.remove(code)
        self.d_setRedeemedCodes(sef.redeemedCodes)

    def setGuildId(self, id):
        self.guildId = id

    def d_setGuildId(self, id):
        self.sendUpdate('setGuildId', [id])

    def b_setGuildId(self, id):
        self.setGuildId(id)
        self.d_setGuildId(id)

    def getGuildId(self):
        return self.guildId

    def setGuildName(self, name):
        self.guildName = name

    def d_setGuildName(self, name):
        self.sendUpdate('setGuildName', [name])

    def b_setGuildName(self, name):
        self.setGuildName(name)
        self.d_setGuildName(name)

    def getGuildName(self):
        return self.guildName

    def setStatus(self, todo0):
        pass

    def enterAreaSphere(self, todo0, todo1):
        pass

    def requestRegionUpdate(self, todo0):
        pass

    def leaveAreaSphere(self, todo0, todo1):
        pass

    def requestInteraction(self, avId, interactType, instant):
        pass

    def submitErrorLog(self, errorString):
        pass

    def setCrewIconIndicator(self, iconId):
        self.crewIcon = iconId

    def getCrewIconIndicator(self):
        return self.crewIcon

    def requestBadgeIcon(self, titleId, rank):
        pass

    def requestShipBadgeIcon(self, titleId, rank):
        pass

    def setAFK(self, isAFK):
        pass

    def setInInvasion(self, inInvasion):
        pass

    def setActiveShipId(self, shipId):
        pass

    def requestExit(self):
        pass

    def setAuraActivated(self, todo0):
        pass

    def requestKill(self, variable):
        pass
    
    def d_doRegeneration(self):
        self.sendUpdate('doRegeneration', [])
    
    def requestClothes(self, dna):
        style = HumanDNA()
        style.makeFromNetString(dna)

        self.style.clothes = style.clothes
        self.d_setDNAString(self.style.makeNetString())
        self.d_doRegeneration()

@magicWord(CATEGORY_GAME_DEVELOPER)
def suicide(reason = "kindergarten is elsewhere."):
    """ Kick yourself from the game server. """
    av = spellbook.getInvoker()
    dg = PyDatagram()
    dg.addServerHeader(av.GetPuppetConnectionChannel(av.doId), simbase.air.ourChannel, CLIENTAGENT_EJECT)
    dg.addString(reason)
    dg.addUint16(155)
    simbase.air.send(dg)
    return "Kicked %s from the game." % av

@magicWord(CATEGORY_SYSTEM_ADMINISTRATOR)
def system(text):
    """Send a whisper to the whole district (system), un-prefixed."""
    air = spellbook.getInvoker().air
    air.systemMsgAll(text)
    return "Sent system message '%s' to all pirates in the district." % text

@magicWord(CATEGORY_SYSTEM_ADMINISTRATOR)
def sysadmin(text):
    """Send a whisper to the whole district, prefixed with 'ADMIN:'."""
    air = spellbook.getInvoker().air
    text = 'ADMIN: ' + text # Prefix text with "ADMIN".
    air.systemMsgAll(text)
    return "Sent system message '%s' to all pirates in the district." % text

@magicWord(CATEGORY_SYSTEM_ADMINISTRATOR)
def sysname(text):
    """Send a whisper to the whole district, prefixed with 'ADMIN Name:'."""
    air = spellbook.getInvoker().air
    text = 'ADMIN ' + spellbook.getInvoker().getName() + ': ' + text # Prepend text with "ADMIN ", then the Invoker's pirate name.
    air.systemMsgAll(text)
    return "Sent system message '%s' to all pirates in the district." % text

@magicWord(CATEGORY_GAME_DEVELOPER)
def update(reason="for an update"):
    """Send a whisper to the whole gameserver, prefixed with 'ADMIN Name:'."""
    air = spellbook.getInvoker().air
    text = "ADMIN: Ahoy, maties! Pirates Online Retribution will be closing momentarily " + reason + "." # Maintenance text
    air.systemMsgAll(text)
    return "Sent maintenance warning message to all pirates in the gameserver!"

@magicWord(CATEGORY_MODERATION, types=[int])
def hp(value=-1):
    av = spellbook.getTarget()
    if value < 0:
        value = av.getMaxHp()

    value = min(value, av.getMaxHp())
    av.b_setHp(value)

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def mojo(value=-1):
    av = spellbook.getTarget()
    if value < 0:
        value = av.getMaxMojo()

    value = min(value, av.getMaxMojo())
    av.b_setMojo(value)

@magicWord(CATEGORY_GAME_MASTER)
def groggy():
    av = spellbook.getTarget()
    av.addDeathPenalty(True)

@magicWord(CATEGORY_GAME_MASTER)
def rmgroggy():
    av = spellbook.getTarget()
    av.removeDeathPenalty()
    av.fillHpMeter()

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def rep(amount):
    av = spellbook.getInvoker()
    repId = ItemGlobals.getItemRepId(av.currentWeaponId)
    if not repId:
        return 'Pick the weapon you want to add reputation to!'

    av.inventory.addReputation(repId, amount)

@magicWord(CATEGORY_GAME_DEVELOPER, types=[str])
def allegiance(side=None):
    allegiances = ['pirate', 'spanish', 'french']
    side = side.lower()
    
    if side not in allegiances:
        return 'Allegiance can only be pirate, spanish or french!'
    
    av = spellbook.getTarget()
    av.b_setAllegiance(allegiances.index(side))
    return "%s's allegiance has been set!" % av.getName()

@magicWord(CATEGORY_YOUTUBER)
def hideGM():
    av = spellbook.getInvoker()
    av.b_setGMHidden(not av.getGMHidden())
    return 'GM tag has been %s.' % ('hidden' if av.getGMHidden() else 'shown')

@magicWord(CATEGORY_GAME_DEVELOPER, types=[str, str])
def gm(color=None, tag=None):
    av = spellbook.getTarget()
    
    if not color:
        av.b_setGMNametag('', '')
        return 'Cleared GM nametag!'
    elif color not in ('gold', 'red', 'green', 'blue'):
        return 'Color must be gold, red, green or blue!'
    elif not tag:
        return 'You must specify a tag!'
    else:
        av.b_setGMNametag(color, tag)
        return 'GM nametag set!'

@magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
def giveGold(gold):
    target = spellbook.getTarget()
    invoker = spellbook.getInvoker()
    target.giveGold(gold)
    return 'Given %d gold to %s! Balance: %d' % (gold, target.getName(), target.getGoldInPocket())

@magicWord(CATEGORY_SYSTEM_ADMINISTRATOR, types=[int])
def takeGold(gold):
    target = spellbook.getTarget()
    invoker = spellbook.getInvoker()
    target.takeGold(gold)
    return 'Taken %d gold from %s! Balance: %d' % (gold, target.getName(), target.getGoldInPocket())

@magicWord(CATEGORY_GAME_MASTER)
def cursed():
    target = spellbook.getTarget()
    state, cursed = target.getZombie()
    response = ''
    if state:
        target.b_setZombie(0, 0)
        response = 'The curse has worn off...'
    else:
        target.b_setZombie(1, 1)
        response = '%s has been cursed!' % target.getName()
    return response

@magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
def setDoubleXP(value):
    target = spellbook.getTarget()
    target.b_setTempDoubleXPReward(value * 60)
    return "Set %s's TempDoubleXPReward to %s minutes" % (target.getName(), value)

@magicWord(CATEGORY_GAME_DEVELOPER)
def getDoubleXP():
    target = spellbook.getTarget()
    return '%s has %s minutes left of double xp' % (target.getName(), str(target.getTempDoubleXPReward()))

@magicWord(CATEGORY_GAME_DEVELOPER, types=[int, int])
def setBadge(title, rank):
    target = spellbook.getTarget()
    target.b_setBadgeIcon(title, rank)
    return "Set {0}'s badgeIcon to ({1}, {2})".format(target.getName(), title, rank)

@magicWord(CATEGORY_GAME_DEVELOPER, types=[int, int])
def setShipBadge(title, rank):
    target = spellbook.getTarget()
    target.b_setShipIcon(title, rank)
    return "Set {0}'s shipBadge to ({1}, {2})".format(target.getName(), title, rank)

@magicWord(CATEGORY_GAME_DEVELOPER, types=[int, int, int])
def giveLocatable(type, itemId, amount):
    target = spellbook.getTarget()
    invoker = spellbook.getInvoker()

    from pirates.uberdog.TradableInventoryBase import InvItem

    if not invoker or not target:
        return "Failed to give locatable, Unknown error has occured."

    inv = target.getInventory()

    if not inv:
        return "Failed to get target's inventory."

    location = inv.findAvailableLocation(type, itemId=itemId, count=amount, equippable=True)
    if location == -1:
        return "Failed to give locatable. Target's inventory is full"

    success = inv.addLocatable(itemId, location, 1)
    if not success:
        return "Failed to give locatable. Target's inventory is most likely full."

    return "Locatable given to %s." % target.getName()

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def giveWeapon(itemId):
    target = spellbook.getInvoker()
    invokerAccess = target.getAdminAccess()
    
    from pirates.uberdog.UberDogGlobals import InventoryType
    from pirates.uberdog.TradableInventoryBase import InvItem
    
    if invokerAccess >= CATEGORY_GAME_DEVELOPER.access:
        target = spellbook.getTarget()

        if not target:
            return "Failed to give weapon. Unknown error has occured."

        inv = target.getInventory()
        if not inv:
            return "Failed to get target's inventory."

        location = inv.findAvailableLocation(InventoryType.ItemTypeWeapon, itemId=itemId, count=1, equippable=True)
        if location == -1:
            return "Failed to give weapon. Target's inventory is full"

        success = inv.addLocatable(itemId, location, 1, InventoryType.ItemTypeWeapon)
        if not success:
            return "Failed to give weapon. Target's inventory is most likely full."

        return "Weapon (%s) given to %s." % (itemId, target.getName())

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def giveClothing(itemId):
    
    target = spellbook.getInvoker()
    invokerAccess = target.getAdminAccess()

    from pirates.uberdog.UberDogGlobals import InventoryType
    from pirates.uberdog.TradableInventoryBase import InvItem

   if invokerAccess >= CATEGORY_GAME_DEVELOPER.access:
        target = spellbook.getTarget()

        if not target:
            return "Failed to give clothing Item. Unknown error has occured."

        inv = target.getInventory()
        if not inv:
            return "Failed to get target's inventory."

        location = inv.findAvailableLocation(InventoryType.ItemTypeClothing, itemId=itemId, count=1, equippable=True)
        if location == -1:
            return "Failed to give clothing item. Target's inventory is full"

        success = inv.addLocatable(itemId, location, 1, InventoryType.ItemTypeClothing)
        if not success:
            return "Failed to give clothing item. Target's inventory is most likely full."

        return "Clothing (%s) given to %s." % (itemId, target.getName())
        

@magicWord(CATEGORY_GAME_DEVELOPER, types=[int])
def giveJewelry(itemId):
    
    target = spellbook.getInvoker()
    invokerAccess = target.getAdminAccess()

    from pirates.uberdog.UberDogGlobals import InventoryType
    from pirates.uberdog.TradableInventoryBase import InvItem
    
    if invokerAccess >= CATEGORY_GAME_DEVELOPER.access:
        target = spellbook.getTarget()

        if not target:
            return "Failed to give jewelry item. Unknown error has occured."

        inv = target.getInventory()
        if not inv:
            return "Failed to get target's inventory."

        location = inv.findAvailableLocation(InventoryType.ItemTypeJewelry, itemId=itemId, count=1, equippable=True)
        if location == -1:
            return "Failed to give jewelry item. Target's inventory is full"

        success = inv.addLocatable(itemId, location, 1, InventoryType.ItemTypeJewelry)
        if not success:
            return "Failed to give jewelry item. Target's inventory is most likely full."

        return "Jewelry (%s) given to %s." % (itemId, target.getName())

@magicWord(CATEGORY_GAME_MASTER, types=[int])
def ghost(color=None):
    av = spellbook.getInvoker()
    if color == None:
        av.b_setIsGhost(False)
        return "Set your ghost state to false" % av.getName()
    else:
        if color > 13 or color < 1:
            return "Invalid ghost color. Valid range is 1-13"

        av.b_setIsGhost(True)
        av.b_setGhostColor(color)
        return "Set your ghost color to %s" % color

@magicWord(CATEGORY_GAME_DEVELOPER)
def mypos():
    av = spellbook.getInvoker()
    return "Pos: %s" % str(av.getPos())

@magicWord(CATEGORY_GAME_DEVELOPER)
def getUsedCodes():
    av = spellbook.getTarget()
    return "Codes: %s" % str(av.getRedeemedCodes())

@magicWord(CATEGORY_GAME_DEVELOPER)
def clearUsedCodes():
    invoker = spellbook.getInvoker()
    av = spellbook.getTarget()
    av.d_setRedeemedCodes([])
    av.setRedeemedCodes([])
    return "Cleared Redeemed codes."

@magicWord(CATEGORY_GAME_DEVELOPER, types=[str])
def clearCode(code):
    invoker = spellbook.getInvoker()
    av = spellbook.getTarget()
    if code not in av.getRedeemedCodes():
        return "%s has not redeemed '%s'." % (av.getName(), code)
    av.removeRedeemedCode(code)
    return "Removed '%s'!" % code 

@magicWord(CATEGORY_GAME_DEVELOPER, types=[str])
def registerCodeUsed(code):
    invoker = spellbook.getInvoker()
    av = spellbook.getTarget()
    if code in av.getRedeemedCodes():
        return "%s has already redeemed '%s'." % (av.getName(), code)
    av.addRedeemedCode(code)
    return "Registered '%s' as used for %s." % (code, av.getName())
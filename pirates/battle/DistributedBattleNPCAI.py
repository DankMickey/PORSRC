from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.GridParent import GridParent
from direct.distributed.ClockDelta import *
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pirates.pathfinding.core.nai import NAI
from pirates.battle.DistributedBattleAvatarAI import *
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import EnemyGlobals
from direct.interval.LerpInterval import LerpPosInterval
import sys
from math import sin, pi, cos
import random

class BattleFSM(FSM):

    def __init__(self, owner):
        FSM.__init__(self, 'BattleFSM')

        self._owner = owner
        self._target = None

        self.__interval = None

    def setTarget(self, target):
        self._target = target

    def getTarget(self):
        return self._target

    def __update(self, task):
        
        #print '__update'
        '''
        distance = self._owner.getDistance(self._target)

        if distance <= self._owner.aggroRadius:
            print '<='
            print distance
            return task.cont
        else: 
            print '>'
            print distance
        '''

       # if self.__interval:
       #     self.__interval.finish()

       # self.__interval = self._owner.posInterval(5, Point3(self._target.getX() - self._owner.aggroRadius, self._target.getY(), self._target.getZ()), self._owner.getPos(), other=None, blendType='easeInOut', bakeInStart=1, fluid=1, name=None)

        #self.__interval.start()
        
       # print self.__interval
        #print self._owner.getPos()

        self._owner.lookAt(self._target)
        #self._owner.updateSmPos(self._target.getPos(), self._target.getHpr())
        #LerpPosInterval(self, 1, self._target.getPos(), startPos=self.getPos())
        #self._owner.d_updateSmPos()
        #elf.setAI()
        
        return task.cont
        
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterAttack(self):
        if not self._target:
            return

        taskMgr.add(self.__update, 'update-%d' % (self._owner.doId))

    def exitAttack(self):
        taskMgr.remove('update-%d' % (self._owner.doId))

class DistributedBattleNPCAI(DistributedBattleAvatarAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')
    isNpc = True

    def __init__(self, spawner):
        self.spawner = spawner
        DistributedBattleAvatarAI.__init__(self, spawner.air)
        FSM.__init__(self, 'DistributedBattleNPCAI')
        self.spawnPos = (0, 0, 0)
        self.spawnPosIndex = ''
        self.associatedQuests = []

        self.animSet = 'default'
        self.noticeAnim1 = ''
        self.noticeAnim2 = ''
        self.greetingAnim = ''

        self.collisionMode = PiratesGlobals.COLL_MODE_ALL
        self.initZ = 0
        self.uniqueId = ''
        self.dnaId = ''

        self.damageScale = 1

        self.enemies = set()

        self.battleFSM = BattleFSM(self)
        
        #self.nai = NAI(tagto=self.getParentObj())
        #self.nai.addcharacter("pursuer", self, 100, 0.05, 5)

    def setDNAId(self, dnaId):
        self.dnaId = dnaId

    def getDNAId(self):
        return self.dnaId

    def getSpawnPos(self):
        return self.spawnPos
    
    def setLevel(self, level):
        if not level:
            level = EnemyGlobals.getRandomEnemyLevel(self.avatarType)
        DistributedBattleAvatarAI.setLevel(self, level)
        maxHp = EnemyGlobals.getMonsterHp(level)
        self.setHp(maxHp)
        self.setMaxHp(maxHp)

    def announceGenerate(self):
        #print 'announceGenerate'
        DistributedBattleAvatarAI.announceGenerate(self)
        self.demand('Spawn')

        self.skills = EnemyGlobals.getEnemySkills(self.avatarType, self.level)
        self.weapons = EnemyGlobals.getEnemyWeapons(self.avatarType, self.level)
        self.startPos = self.getPos()
        
        self.mainWeapon = self.weapons.keys()[0]
        if self.mainWeapon > 1:
            startDrawn = self.animSet in EnemyGlobals.DRAWN_ANIME
            if self.mainWeapon in EnemyGlobals.DRAWN_WEAPONS:
                startDrawn = True
            self.b_setCurrentWeapon(self.mainWeapon, startDrawn)
            
        self.nai = NAI(tagto=self.getParentObj())
        self.nai.addcharacter(self.getName(), self, 100, 0.05, 5)
        print self.nai.getname()

    def enterSpawn(self):
        self.sendUpdate('setSpawnIn', [globalClockDelta.getRealNetworkTime(bits=32)])
        self.addSkillEffect(WeaponGlobals.C_SPAWN)
        taskMgr.doMethodLater(8, self.__removeSpawn, self.uniqueName('spawned'))

    def __removeSpawn(self, task):
        self.removeSkillEffect(WeaponGlobals.C_SPAWN)
        self.demand(self.getStartState())
        return task.done

    def exitSpawn(self):
        taskMgr.remove(self.uniqueName('spawned'))
        self.removeSkillEffect(WeaponGlobals.C_SPAWN)
        self.d_updateSmPos()

    def delete(self):
        self.demand('Off')
        messenger.send('enemyDefeated', [self])
        DistributedBattleAvatarAI.delete(self)

    def setSpawnPos(self, spawnPos):
        self.spawnPos = spawnPos

    def getSpawnPos(self):
        return self.spawnPos

    def getSpawnPosIndex(self):
        # This seems related to quests, return uniqueId for now
        return self.getUniqueId()

    def setAssociatedQuests(self, associatedQuests):
        self.associatedQuests = associatedQuests

    def getAssociatedQuests(self):
        return self.associatedQuests

    def setActorAnims(self, animSet, noticeAnim1, noticeAnim2, greetingAnim):
        self.animSet = animSet
        self.noticeAnim1 = noticeAnim1
        self.noticeAnim2 = noticeAnim2
        self.greetingAnim = greetingAnim

    def getActorAnims(self):
        return [self.animSet, self.noticeAnim1, self.noticeAnim2, self.greetingAnim]

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode

    def getCollisionMode(self):
        return self.collisionMode

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def setAvatarType(self, avatarType):
        DistributedBattleAvatarAI.setAvatarType(self, avatarType)
        self.setName(self.avatarType.getName())

    def getUniqueId(self):
        return self.uniqueId

    # setInitZ is not used by client
    def setInitZ(self, initZ):
        self.initZ = initZ

    def getInitZ(self):
        return self.initZ

    def posControlledByCell(self):
        area = self.getParentObj()

        cell = GridParent.getCellOrigin(area, self.zoneId)
        pos = self.getPos()
        self.reparentTo(cell)
        self.setPos(area, pos)

        self.d_updateSmPos()
        return False

    def d_updateSmPos(self):
        if ((self.getPos()) and (self.getHpr())):
            x, y, z, h, p, r = list(self.getPos()) + list(self.getHpr())
            #print self.getPos()
            self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, 0])
        else:
            pass
        
    def updateSmPos(self, pos, hpr):
        if ((pos) and (hpr)):
            x, y, z, h, p, r = list(pos) + list(hpr)
            self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, 0])
        else:
            pass

    def enterBattle(self):
        print 'enterBattle'
        remove = set()
        for enemy in self.enemies:
            av = self.air.doId2do.get(enemy)
        self.av = av
        self.setAI(self.av)
        #self.lookAt(self.av)
        self.sendUpdate('setLegState', ['1'])
        self.sendUpdate('setIsAlarmed', [1, self.getAggroRadius()])
        self.waitForNextBattleTask()
        if self.mainWeapon > 1:
            self.b_setCurrentWeapon(self.mainWeapon, 1)

    def waitForNextBattleTask(self):
        dt = random.random() * 6 + .15
        dt -= self.getLevel() / 25.0
        dt = max(.3, dt)
        taskMgr.doMethodLater(dt, self.__battleTask, self.taskName('battleTask'))

    def __battleTask(self, task):
        remove = set()
        for enemy in self.enemies:
            av = self.air.doId2do.get(enemy)
            
        self.battleFSM.setTarget(av)

        skillId = random.choice(self.skills.keys())
        ammoSkillId = 0
        pos = self.getPos()
        
        ''' If near player AOE
        if (pos != av.getPos()):
            self.setAI(av)
        else:
            self.evadeAI(av)
        '''
        
        #self.setAI(av)
        #self.lookAt(av)
        result = self.attemptUseTargetedSkill(skillId, ammoSkillId, 0, av.doId, [],
                                              globalClockDelta.getRealNetworkTime(bits=32),
                                              pos, 0)

        if result == WeaponGlobals.RESULT_OUT_OF_RANGE and not ammoSkillId:
            self.battleFSM.request('Attack')
            

        self.waitForNextBattleTask()
        return task.done
        
    def setAI(self, av):
        self.nai.follow(name=self.getName(), target=av)
        taskMgr.add(self.AIUpdate, "AIUpdate")
        print self.nai.getname()
        
    def unsetAI(self, av):
        self.nai.removeFollow(name=self.getName(), target=av)
        taskMgr.add(self.AIUpdate, "AIUpdate")
        print self.nai.getname()
        
    def evadeAI(self, av):
        self.nai.evade(name=self.getName(), target=av)
        taskMgr.add(self.AIUpdate, "AIUpdate")

    def AIUpdate(self, task):
        self.nai.getworld().update()
        self.d_updateSmPos()
        return task.cont

    def setDamageScale(self, damageScale):
        self.damageScale = damageScale

    def getMonsterDmg(self):
        return EnemyGlobals.getMonsterDmg(self.level) * self.damageScale

    def exitBattle(self):
        print 'exitBattle'
        self.unsetAI(self.av)
        self.lookAt(self.av)
        self.sendUpdate('setLegState', ['0'])
        self.sendUpdate('setIsAlarmed', [0, 0])
        taskMgr.remove(self.taskName('battleTask'))

        if self.mainWeapon > 1:
            endDrawn = self.animSet in EnemyGlobals.DRAWN_ANIME or self.mainWeapon in EnemyGlobals.DRAWN_WEAPONS
            self.b_setCurrentWeapon(self.mainWeapon, endDrawn)

        self.battleFSM.request('Off')

    # TO DO:
    # boardVehicle(uint32) broadcast ram
    # setChat(string, uint8) broadcast ownsend
    # requestAnimSet(string) broadcast

    def handleInteract(self, avId, interactType, instant):
        print interactType
        if interactType == PiratesGlobals.INTERACT_TYPE_HOSTILE:
            self.enemies.add(avId)
            if self.state not in ('Battle', 'Death'):
                self.demand('Battle')

            av = self.air.doId2do.get(avId)
            if av:
                av.sendUpdate('setCurrentTarget', [0])

        return IGNORE

    def requestHostilize(self):
        print 'requestHostilize'
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        self.handleInteract(avId, PiratesGlobals.INTERACT_TYPE_HOSTILE, 0)

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        self.removeEnemy(avId)

    def removeEnemy(self, avId):
        if avId in self.enemies:
            self.enemies.remove(avId)
            av = self.air.doId2do.get(avId)
            if av:
                av.sendUpdate('setCurrentTarget', [0])

    def enterAmbush(self):
        print 'enterAmbush'
        self.sendUpdate('setAmbush', [1])

    def ambushIntroDone(self):
        if self.state == 'Ambush':
            self.demand('Battle')

    def died(self):
        self.demand('Death')

    def enterDeath(self):
        def doDeath(task):
            self.spawner.died()
            self.requestDelete()
            return task.done

        self.applyRewards()

        if self.air.lootManager:
            self.air.lootManager.spawnLoot(self)

        messenger.send('enemyDefeated', [self])
        taskMgr.doMethodLater(5, doDeath, self.taskName('death'))

    def applyRewards(self):
        multiplier = random.randint(6, 12) / 1.2
        for avId, skills in self.enemySkills.items():
            av = self.air.doId2do.get(avId)
            if not av:
                continue

            repId2rep = {}
            for repId, skillId, ammoSkillId in skills:
                amount = int(self.level * WeaponGlobals.getAttackReputation(skillId, ammoSkillId) * multiplier)
                repId2rep[repId] = repId2rep.get(repId, 0) + amount

            for repId, amount in repId2rep.items():
                while amount > 125:
                    amount = int(amount / 1.173)
                av.addReputation(repId, amount)

            av.repChanged()

    def exitDeath(self):
        taskMgr.remove(self.taskName('death'))

    def demand(self, state, *args):
        FSM.demand(self, state, *args)
        self.sendUpdate('setGameState', [state, globalClockDelta.getRealNetworkTime()])

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        if cls is None:
            cls = DistributedBattleNPCAI

        obj = cls(spawner)

        x, y, z = data.get('Pos', (0, 0, 0))
        h, p, r = data.get('Hpr', (0, 0, 0))
        pos = (x, y, z)
        hpr = (h, p, r)

        gridPos = data.get('GridPos')
        if gridPos:
            pos = gridPos

        obj.setSpawnPos(pos)
        obj.setPos(pos)
        obj.setHpr(hpr)

        animSet = data.get('AnimSet', 'default')
        noticeAnim1 = data.get('Notice Animation 1', '')
        noticeAnim2 = data.get('Notice Animation 2', '')
        greetingAnim = data.get('Greeting Animation', '')

        obj.setAvatarType(avType)
        obj.setUniqueId(uid)
        obj.setActorAnims(animSet, noticeAnim1, noticeAnim2, greetingAnim)
        try:
            obj.setIsGhost(int(data['GhostFX']))
        except:
            # some objects don't have GhostFX declared in their data.
            obj.setIsGhost(0)
        try:
            obj.setGhostColor(int(data['GhostColor']))
        except:
            obj.setGhostColor(0)
            
        if 'Level' in data:
            obj.setLevel(int(data['Level']))

        if 'Aggro Radius' in data:
            obj.setAggroRadius(int(float(data['Aggro Radius'])))

        if 'Start State' in data:
            obj.setStartState(data['Start State'])
        return obj
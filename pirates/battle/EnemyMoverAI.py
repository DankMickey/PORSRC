from panda3d.core import Point3, Vec3
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import *
from direct.distributed.DistributedSmoothNodeBase import DistributedSmoothNodeBase
import random, math

def getRandomPoint(radius, originX, originY, originZ):
    angle = random.random() * math.pi * 2
    radius *= math.sqrt(random.random())
    
    return Point3(originX + radius * math.cos(angle), originY + radius * math.sin(angle), originZ)

class EnemyMoverAI(FSM):

    def __init__(self, enemy):
        FSM.__init__(self, 'EnemyMoverAI-%d' % enemy.doId)
        self.enemy = enemy
        self.sequence = None
        self.started = False
        self.fwdSpeed = 10.0
        self.rotSpeed = 360.0
    
    def destroy(self):
        self.demand('Off')
        self.unscheduleWander()
        self.unscheduleFollow()
        self.enemy = None
    
    def getParent(self):
        return self.enemy.getParent()
    
    def endSequence(self):
        if self.sequence:
            self.sequence.pause()
        
        self.sequence = None
    
    def enterOff(self):
        self.endSequence()
    
    def scheduleWander(self, min=12, max=22):
        self.unscheduleWander()
        taskMgr.doMethodLater(random.randint(min, max), self.wanderRandomly, self.enemy.uniqueName('next-wander'))
    
    def unscheduleWander(self):
        taskMgr.remove(self.enemy.uniqueName('next-wander'))
    
    def scheduleFollow(self):
        self.unscheduleFollow()
        taskMgr.doMethodLater(0.75, self.followEnemy, self.enemy.uniqueName('next-follow'))
    
    def unscheduleFollow(self):
        taskMgr.remove(self.enemy.uniqueName('next-follow'))
    
    def getWanderPoint(self):
        return getRandomPoint(self.enemy.getPatrolRadius(), *self.enemy.relativePos)
    
    def wanderRandomly(self, *args):
        point = self.getWanderPoint()
        self.walkToPoint(point, self.scheduleWander)
        
    def enterWander(self):
        self.wanderRandomly()
    
    def exitWander(self):
        self.endSequence()
        self.unscheduleWander()
    
    def enterFollowEnemy(self):
        self.followEnemy()
    
    def exitFollowEnemy(self):
        self.endSequence()
        self.unscheduleFollow()
    
    def followEnemy(self, *args):
        pos = self.enemy.getEnemyPosition()
        enemy = self.enemy.getFocusingEnemy()
        
        if enemy:
            self.enemy.headsUp(enemy.getPos(self.getParent()))
            self.enemy.d_updateSmPos()
        
        if pos:
            self.walkToPoint(pos, self.scheduleFollow)
        else:
            self.scheduleFollow()
    
    def getHeadsUp(self, target):
        hpr = self.enemy.getHpr()

        self.enemy.headsUp(target)

        result = self.enemy.getH()
        
        self.enemy.setHpr(hpr)
        return result % 360
    
    def walkToPoint(self, target, callback=None):
        if not callback:
            callback = lambda: 0
        
        here = self.enemy.getPos()
        dist = Vec3(here - target).length()
        headsUp = self.getHeadsUp(target)
        headsUpDist = abs(self.enemy.getH() - headsUp)
        
        if not self.started:
            self.enemy.startPosHprBroadcast()
            self.started = True

        self.endSequence()
        self.sequence = Sequence(
            self.enemy.hprInterval(headsUpDist / self.rotSpeed, (headsUp, 0, 0), (self.enemy.getH(), 0, 0)),
            self.enemy.posInterval(dist / self.fwdSpeed, target, here),
            Func(callback)
        )
        self.sequence.start()
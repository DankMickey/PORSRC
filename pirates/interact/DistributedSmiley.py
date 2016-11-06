from panda3d.core import NodePath, headsUp
import math
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.showbase.PythonUtil import quickProfile
from pirates.distributed import DistributedInteractive
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
containerCache = { }

class DistributedSmiley(DistributedInteractive.DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSmiley')
    deferrable = True

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedSmiley')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.sphereScale = 10
        self.smile = None

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale


    def getSphereScale(self):
        return self.sphereScale


    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)


    def setVisZone(self, zone):
        self.visZone = zone


    def getVisZone(self):
        return self.visZone


    def announceGenerate(self):
        self.setInteractOptions(proximityText = PLocalizer.InteractSearchableContainer, sphereScale = self.getSphereScale(), diskRadius = 10, exclusive = 0)
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.loadContainer()
        self.getParentObj().builder.addSectionObj(self.smile, self.visZone)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        if self.getParentObj():
            self.getParentObj().builder.removeSectionObj(self.smile, self.visZone)
        if self.smile:
            self.smile.remove_node()
            self.smile = None

    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)


    def loadContainer(self):
        if self.smile:
            return None

        modelPath = 'models/misc/smiley'
        model = loader.loadModel(modelPath)
        model.flattenStrong()
        model = model.copyTo(NodePath())
        model.reparentTo(self)
        self.smile = model


    def requestInteraction(self, avId, interactType = 0):
        localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)


    def rejectInteraction(self):
        localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)


    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        self.stopSearching(0)

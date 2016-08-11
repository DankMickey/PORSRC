from panda3d.core import NodePath
from pirates.distributed.DistributedInteractive import DistributedInteractive

class DistributedHolidayObject(DistributedInteractive):

    def __init__(self, cr, proximityText = None):
        NodePath.__init__(self, self.__class__.__name__)
        DistributedInteractive.__init__(self, cr)
        self.holiday = ''
        self.interactRadius = 10
        self.interactMode = 0
        self.proximityText = proximityText

    def setHoliday(self, holiday):
        self.holiday = holiday

    def setInteractRadius(self, radius):
        self.interactRadius = radius
        self.diskRadius = radius * 2.0

    def setInteractMode(self, mode):
        if (mode == 1 or mode == 2) and localAvatar.isGM():
            self.setInteractOptions(proximityText = self.proximityText, sphereScale = self.interactRadius, diskRadius = self.diskRadius)
        else:
            self.setInteractOptions(allowInteract = False)

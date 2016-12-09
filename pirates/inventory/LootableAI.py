from direct.gui.DirectGui import *
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
from pirates.uberdog import UberDogGlobals
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.inventory import ItemConstants
from pirates.inventory import InventoryGlobals
from pirates.inventory import InventoryPlunderPanel
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory import ItemGlobals
from pirates.inventory.InventoryUIGlobals import *
from pirates.uberdog.UberDogGlobals import *
from pirates.battle import WeaponGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class LootableAI(DistributedObjectAI):
    notify = directNotify.newCategory('LootableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
     
    def startLooting(self, avId, plunderInfo, itemsToTake=0, timer=0, autoShow=True):
        self.notify.info("startLooting. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
        self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, itemsToTake, timer, autoShow])

    def stopLooting(self):
        self.notify.info("stopLooting Sent ")

    def doneTaking(self):
        self.notify.info("doneTaking Sent ")

    def requestItem(self, item):
        self.notify.info("requestItem. item: %s" % (item,))

    def requestItems(self):
        self.notify.info("requestItems.")

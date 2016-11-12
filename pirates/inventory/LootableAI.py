from panda3d.core import Point3, TextNode
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
from pirates.inventory import Lootable


class LootableAI(DistributedObjectAI, Lootable.Lootable):
    notify = directNotify.newCategory('LootableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        Lootable.Lootable.__init__(self)
        self.heldItem = None
        self.heldFromCell = None
        self.withInCell = None
        self.withInBag = None
        self.pickupTimedOut = 0
        self.stackSplitter = None
        self.removeConfirm = None
        self.removeContainer = None
        self.plunderPanel = None
        self.showingItem = None
        self.locked = 0
        self.localInventoryOpen = 0
        self.standardButtonSize = 0.14
        self.pickUpTime = 0.3
        self.scoreboard = None
        self.lootContainer = None
        self.containerIsGeneric = False
        self.tradeContainer = None
        self.discoveredInventory = 0
        self.trashItem = None
        self.reasonNoUse = None
     
	 

    def startLooting(self, avId, plunderInfo, itemsToTake=0, timer=0, autoShow=True):
     self.notify.info("startLooting. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
     self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, itemsToTake, timer, autoShow])
     self.notify.info("Debug1.1")
     Lootable.Lootable.setupPlunderList(self)

    def stopLooting(self):
        self.notify.info("stopLooting Sent ")

    def doneTaking(self):
        self.notify.info("doneTaking Sent ")

    def requestItem(self, plunderLocationInfo):
        self.notify.info("requestItem. plunderLocationInfo: %s" % plunderLocationInfo)

    def requestItems(self, pluderInfo):
        self.notify.info("requestItems. plunderInfo: %s" % plunderInfo)

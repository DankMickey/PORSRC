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

    # (PlunderListItem array, int8, uint8, bool)
    def startLooting(self, avId, plunderInfo, itemsToTake=0, timer=0, autoShow=True):
     self.notify.info("startLooting. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
     self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, itemsToTake, timer, autoShow])
     self.notify.info("Debug Message 1")
     self.intiatePlunder()
	
    def intiatePlunder(self):
        plunderList = [(UberDogGlobals.InventoryType.ItemTypeMoney, 32)]
        self.buildPlunderContainer(plunderList)
	self.notify.info("Debug Message 2 with plunderList defined as: %s" % (plunderList))



    def buildPlunderContainer(self, plunderList, lootContainer = None, customName = None, timer = 0, autoShow = True):
         self.notify.info("Debug Message 3.1")
         if not self.plunderPanel:
            if self.lootContainer:
		self.notify.info("Debug Message 3.2")
                self.closePlunder()

            rating = 0
            typeName = ''
            if lootContainer:
		self.notify.info("Debug Message 4")
                self.lootContainer = lootContainer
                rating = lootContainer.getRating()
                typeName = lootContainer.getTypeName()
                numItems = lootContainer.getItemsToTake()
            else:
		self.notify.info("Debug Message 5")
                numItems = 0
            self.plunderPanel = InventoryPlunderPanel.InventoryPlunderPanel(self, plunderList, rating, typeName, numItems, customName, timer = timer, autoShow = autoShow) #InventoryPlunderPanel builds the scroll-like parent container which appends the child InventoryUIPlunderGridContainer which builds the item content for each loot type + their icons that are mapped to the general container made in InventoryPlunderPanel (the scroll)
            self.plunderPanel.reparentTo(self)
            self.plunderPanel.setPos(-1.1, 0.0, -0.2)

    def stopLooting(self):
        self.notify.info("stopLooting.")

    # airecv clsend
    def doneTaking(self):
        self.notify.info("doneTaking.")

    # (PlunderItemLocationInfo) airecv clsend
    def requestItem(self, plunderLocationInfo):
        self.notify.info("requestItem. plunderLocationInfo: %s" % plunderLocationInfo)

    # (PlunderItemInfo array) airecv clsend
    def requestItems(self, pluderInfo):
        self.notify.info("requestItems. plunderInfo: %s" % plunderInfo)



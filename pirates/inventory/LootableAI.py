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
#from pirates.inventory.InventoryUIPlunderGridContainer import InventoryUIPlunderGridContainer
#import InventoryUIPlunderGridContainer
#import Lootable
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
     #InventoryUIPlunderGridContainer.__init__(self, air)
	 

    # startLooting(PlunderListItem [], int8, uint8, bool)
    def startLooting(self, avId, plunderInfo, itemsToTake=0, timer=0, autoShow=True):
     self.notify.info("startLooting. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
     self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, itemsToTake, timer, autoShow])
     #self.itemsToTake = itemsToTake
     self.notify.info("niger1. ")
     self.testPlunder()
     #localAvatar.setPlundering(self.getDoId())
     #self.notify.info("fuck bitches 2. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
     #localAvatar.guiMgr.inventoryUIManager.testPlunder()
     #self.notify.info("i fuck ur mom spacebar kek 3. plunderInfo: %s itemsToTake: %s timer: %s autoShow: %s" % (plunderInfo, itemsToTake, timer, autoShow))
     #Lootable.Lootable.startLooting(self, plunderInfo, itemsToTake, timer, autoShow)
     #InventoryUIManager.testPlunder()
	#InventoryUIPlunderGridContainer.setupPlunder(self, plunderInfo)

    # stopLooting()
	
    def testPlunder(self):
        plunderList = [(UberDogGlobals.InventoryType.ItemTypeMoney, 32)]
        self.openPlunder(plunderList)
	self.notify.info("fuck bitches 2. %s !!" % (plunderList))



    def openPlunder(self, plunderList, lootContainer = None, customName = None, timer = 0, autoShow = True):
         self.notify.info("i fuck ur mom spacebar kek 3")
         if not self.plunderPanel:
            if self.lootContainer:
		self.notify.info("close plund 3.")
                self.closePlunder()

            rating = 0
            typeName = ''
            if lootContainer:
		self.notify.info("loot cont.")
                self.lootContainer = lootContainer
                rating = lootContainer.getRating()
                typeName = lootContainer.getTypeName()
                numItems = lootContainer.getItemsToTake()
            else:
		self.notify.info("else loot cont.")
                numItems = 0
            self.plunderPanel = InventoryPlunderPanel.InventoryPlunderPanel(self, plunderList, rating, typeName, numItems, customName, timer = timer, autoShow = autoShow)
            self.plunderPanel.reparentTo(self)
            self.plunderPanel.setPos(-1.1, 0.0, -0.2)

    def stopLooting(self):
        self.notify.info("stopLooting.")

    # doneTaking() airecv clsend
    def doneTaking(self):
        self.notify.info("doneTaking.")

    # requestItem(PlunderItemLocationInfo) airecv clsend
    def requestItem(self, plunderLocationInfo):
        self.notify.info("requestItem. plunderLocationInfo: %s" % plunderLocationInfo)

    # requestItems(PlunderItemInfo []) airecv clsend
    def requestItems(self, pluderInfo):
        self.notify.info("requestItems. plunderInfo: %s" % plunderInfo)



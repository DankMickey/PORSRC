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


class Lootable:
    notify = directNotify.newCategory('Lootable')

    def __init__(self):
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
	
    def startLooting(self, plunderList, itemsToTake = 0, timer = 0, autoShow = False):
        base.localAvatar.guiMgr.inventoryUIManager.plunderIntiate(plunderList, itemsToTake, timer, autoShow)
    
    def setupPlunderList(self, plunderList, itemsToTake = 0, timer = 0, autoShow = False):
        plunderArray = [(UberDogGlobals.InventoryType.ItemTypeMoney, 32)]
        customName = None
        self.openPlunderList(plunderList, self, customName, timer = timer, autoShow = autoShow)
        print '3?'
        self.notify.info("Debug1.2 %s !!" % (plunderList))
    
    def openPlunderList(self, plunderList, lootContainer = None, customName = None, timer = 0, autoShow = True):
        self.notify.info("Debug1.3")
        if not self.plunderPanel:
            if self.lootContainer:
                self.notify.info("Debug1.4")
                self.closePlunder()

        rating = 0
        typeName = ''
        if lootContainer:
            self.notify.info("Debug1.5")
            self.lootContainer = lootContainer
            rating = lootContainer.getRating()
            typeName = lootContainer.getTypeName()
            numItems = lootContainer.getItemsToTake()
        else:
            self.notify.info("Debug1.6")
            numItems = 0
        
        self.plunderPanel = InventoryPlunderPanel.InventoryPlunderPanel(self, plunderList, rating, typeName, numItems, customName, timer = timer, autoShow = autoShow)
        self.plunderPanel.reparentTo(self)
        self.plunderPanel.setPos(-1.1, 0.0, -0.2)


    def d_requestItem(self, itemInfo):
        self.sendUpdate('requestItem', [itemInfo])


    def d_requestItems(self, items):
        self.sendUpdate('requestItems', [items])


    def subtractItemsToTake(self, itemsToTake):
        self.itemsToTake -= itemsToTake


    def getItemsToTake(self):
        return self.itemsToTake


    def doneTaking(self):
        self.sendUpdate('doneTaking', [])


    def getRating(self):
        return -1

    def getTypeName(self):
        return ''

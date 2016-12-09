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
        self.itemsToTake = 0
    
    def startLooting(self, plunderList, itemsToTake = 0, timer = 0, autoShow = False):
        pass

    def d_requestItem(self, itemInfo):
        print 'Requesting item.'
        self.sendUpdate('requestItem', [itemInfo])


    def d_requestItems(self):
        self.sendUpdate('requestItems', [])


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

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.economy import EconomyGlobals
from pirates.inventory import ItemGlobals
from pirates.audio import SoundGlobals
from otp.uberdog.RejectCode import RejectCode
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.uberdog.UberDogGlobals import *

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
    
    
    def requestMusic(self, music):
        if not SoundGlobals.isSongId(music):
            return

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return
        
        requiredGold = EconomyGlobals.PLAY_MUSIC_COST
        
        if requiredGold > av.getGoldInPocket():
            return
        
        av.takeGold(requiredGold)
        self.sendUpdate('playMusic', [music])

    # requestSellShip(uint32) airecv clsend

    def requestPurchaseRepair(self, todo0):
    	pass

    def requestPurchaseOverhaul(self, todo0):
    	pass

    def requestSellShip(self, todo0):
    	pass

    def requestSellItem(self, todo0, todo1, todo2, todo3):
    	self.notify.info("requestSellItem ({0}) ({1}) ({2}) ({3})".format(todo0, todo1, todo2, todo3))

    def requestWeapon(self, buying, selling):

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        itemId, amount = buying[0]
        amount = max(1, amount)

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
        	self.notify.warning("Unable to locate price for itemId: %s" % itemId)
        	self.sendUpdate('makeSaleResponse', [RejectCode.TIMEOUT])
        	return

        requiredGold = requiredGold * amount
        if requiredGold > av.getGoldInPocket():
            return

        inv = av.getInventory()
        if not inv:
        	self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
        	self.sendUpdate('makeSaleResponse', [RejectCode.TIMEOUT])
        	return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeWeapon, itemId=itemId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, amount)
            self.notify.info(success)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2
        self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode])

    def requestAccessories(self, buying, selling):

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        itemId, amount, todo0, todo1 = buying[0] #TODO: figure out what todo0 and todo1 are
        amount = max(1, amount)    

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for itemId: %s" % itemId)
            self.sendUpdate('makeSaleResponse', [RejectCode.TIMEOUT])
            return

        requiredGold = requiredGold * amount
        if requiredGold > av.getGoldInPocket():
            return

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            self.sendUpdate('makeSaleResponse', [RejectCode.TIMEOUT])
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeClothing, itemId=itemId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, amount, inventoryType=InventoryType.ItemTypeClothing)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2

        self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode])

    def requestJewelry(self, buying, selling):

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        itemId, amount = buying[0]
        amount = max(1, amount)

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for itemId: %s" % itemId)
            self.sendUpdate('makeSaleResponse', [RejectCode.TIMEOUT])
            return

        requiredGold = requiredGold * amount
        if requiredGold > av.getGoldInPocket():
            return

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            self.sendUpdate('makeSaleResponse', [RejectCode.TIMEOUT])
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeJewelry, itemId=itemId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, amount, inventoryType=InventoryType.ItemTypeJewelry)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2

        self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode])

    def requestTattoo(self, todo0, todo1):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [0])

    def requestBarber(self, todo0, todo1):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return
    
        self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [0])

    # requestAccessoriesList(uint32) airecv clsend
    # requestJewelryList(uint32) airecv clsend
    # requestTattooList(uint32) airecv clsend
    # requestWeapon(WeaponInfo [], WeaponInfo []) airecv clsend;
    # requestAccessories(Accessory [], Accessory []) airecv clsend
    # requestJewelry(JewelryInfo [], JewelryInfo []) airecv clsend
    # requestAccessoryEquip(Accessory []) airecv clsend
    # requestJewelryEquip(Jewelry []) airecv clsend
    # requestTattooEquip(Tattoo []) airecv clsend
    # requestTattoo(TattooInfo [], TattooInfo []) airecv clsend
    # requestBarber(uint32, uint8) airecv clsend

    def requestStowaway(self, locationId):

        if not locationId in EconomyGlobals.StowawayCost:
            self.notify.warning("Unknown stowaway locationId: %s" % locationId)
            return

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        requiredGold = EconomyGlobals.StowawayCost[locationId]

        if requiredGold > av.getGoldInPocket():
            return

        #av.takeGold(requiredGold)

        #tpMgr = self.air.tpMgr
        #tpMgr.initiateStowawayTeleport(locationId)

    # responseShipRepair(uint32) ownrecv
    # makeTattooResponse(uint16, uint16, bool) ownrecv
    # makeBarberResponse(uint32, uint8, bool) ownrecv
    # responseClothingList(uint32, uint32 [][]) ownrecv
    # responseTattooList(uint32, TattooInfo []) ownrecv
    # responseJewelryList(uint32, JewelryInfo []) ownrecv


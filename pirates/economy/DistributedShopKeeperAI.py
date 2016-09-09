from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.economy import EconomyGlobals
from pirates.audio import SoundGlobals

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
        
        requiredGold = 5
        
        if requiredGold > av.getGoldInPocket():
            return
        
        av.takeGold(requiredGold)
        self.sendUpdate('playMusic', [music])

    # requestPurchaseRepair(uint32) airecv clsend
    # requestPurchaseOverhaul(uint32) airecv clsend
    # requestSellShip(uint32) airecv clsend
    # requestSellItem(uint32, uint32, uint16, uint16) airecv clsend
    # requestAccessoriesList(uint32) airecv clsend
    # requestJewelryList(uint32) airecv clsend
    # requestTattooList(uint32) airecv clsend
    # requestAccessories(Accessory [], Accessory []) airecv clsend
    # requestJewelry(JewelryInfo [], JewelryInfo []) airecv clsend
    # requestAccessoryEquip(Accessory []) airecv clsend
    # requestJewelryEquip(Jewelry []) airecv clsend
    # requestTattooEquip(Tattoo []) airecv clsend
    # requestTattoo(TattooInfo [], TattooInfo []) airecv clsend
    # requestBarber(uint32, uint8) airecv clsend
    # requestStowaway(string) airecv clsend
    # makeSaleResponse(uint32) ownrecv
    # responseShipRepair(uint32) ownrecv
    # makeTattooResponse(uint16, uint16, bool) ownrecv
    # makeBarberResponse(uint32, uint8, bool) ownrecv
    # responseClothingList(uint32, uint32 [][]) ownrecv
    # responseTattooList(uint32, TattooInfo []) ownrecv
    # responseJewelryList(uint32, JewelryInfo []) ownrecv

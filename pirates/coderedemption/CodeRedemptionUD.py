from pirates.uberdog.UberDogGlobals import InventoryType
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
import CodeRedemptionGlobals

class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def checkAlreadyRedeemed(self, avId, code):
        used = False

        #TODO check if code is already used

        if config.GetBool("reject-all-redeem-codes", False):
            used = True

        return used

    def registerCodeUsed(self, avId, awardId):
        pass

    def attemptToRedeemCode(self, code, avId):
        reward = None

        def buildResponse(status, type=-1, uid=0):
            return (status, type, uid)

        try:
            reward = CodeRedemptionGlobals.getAwardFromCode(code)
        except:
            self.notify.warning("Unexpected error has occured while retreiving award info for code %s. Most likely bad award formating." % code)
            return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

        try:
            if reward is not None:

                if self.checkAlreadyRedeemed(avId, code):
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                av = self.air.doId2do.get(avId)
                if not av:
                    self.notify.warning("Failed to locate Avatar for AvatarId: %s" % avId)
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                invType = reward[0]
                invItem = reward[1]
                rewardType = invItem[0] or -1

                femaleReward = invItem[2]
                isFemale = (av.getGender() == 'f')
                if femaleReward and isFemale:
                    rewardType = femaleReward

                itemId = invItem[1] or 0
                amount = reward[3] or 0

                if invType == CodeRedemptionGlobals.NORMAL_INVENTORY:
                    if rewardType == InventoryType.ItemTypeMoney:
                        return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add gold redemption
                        #av.giveGold(amount) #TODO implement on the UD
                    else:
                        return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add item redemption
                elif invType == CodeRedemptionGlobals.CLOTHING:
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add clothing redemption  
                elif invType == CodeRedemptionGlobals.JEWELRY:
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add jewelry redemption
                elif invType == CodeRedemptionGlobals.TATTOO:
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add tattoo redemption
                elif invType == CodeRedemptionGlobals.HAIR:
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add hair redemption
                else:
                    self.notify.warning("Unable to process redemption code for inventory type: %s" % invType)
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                registerCodeUsed(avId, CodeRedemptionGlobals.getAwardIdFromCode(code))
                return buildResponse(CodeRedemptionGlobals.ERROR_ID_GOOD, rewardType, itemId) 
            else:
                return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)
        except Exception, e:
            self.notify.warning(str(e))
            return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

    def sendCodeForRedemption(self, code, userName, accountId):
        self.notify.debug("Attempting to redeem code: %s" % code)
        response = (CodeRedemptionGlobals.ERROR_ID_BAD, -1, 0)
        avId = self.air.getAvatarIdFromSender()
        if avId:
            response = self.attemptToRedeemCode(code, avId)
        self.notify.debug("Sending code redemption response: %s" % str(response))
        try:
            self.sendUpdateToAvatarId(avId, 'notifyClientCodeRedeemStatus', [response[0], response[1], response[2]])
        except Exception, e:
            self.notify.warning("Unexpected error has occured while processing redemption code")
            self.notify.warning(str(e))




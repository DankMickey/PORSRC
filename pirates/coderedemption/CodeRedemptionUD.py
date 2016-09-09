from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
import CodeRedemptionGlobals

class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def sendCodeForRedemption(self, code, userName, accountId):
        reward = None

        try:
        	reward = CodeRedemptionGlobals.AWARD_ID[code]
        except:
        	return REJECT

        if reward is not None:
        	#Handle code redemption
        	return ACCEPT
        else:
        	return REJECT
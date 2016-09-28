from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedPirateBandManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBandManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

	def announceGenerate(self):
		DistributedObjectAI.announceGenerate(self)

	def delete(self):
		DistributedObjectAI.delete(self)

	def requestInvite(self, avId):
		self.notify.info("requestInvite: avId(%s)" % avId)

	def requestRejoin(self, avId, isManager):
		self.notify.info("requestRejoin: avId(%s) isManager(%s)" % (avId, isManager))

	def requestCancel(self, avId):
		self.notify.info("requestCancel: avId(%s)" % avId)

	def invitationResponce(self, avId, avName, responce):
		self.notify.info("inviationResponce: avId(%s) avName(%s) responce(%s)" % (avId, avName, responce))

	def rejoinResponce(self, avId, isManager, responce):
		self.notify.info("rejoinResponse: avId(%s) isManager(%s) responce(%s)" % (avId, isManager, responce))

	def requestBoot(self, avId):
		self.notify.info("requestBoot: avId(%s)" % avId)

	def requestRemove(self, avId):
		self.notify.info("requestRemove: avId(%s)" % avId)

	def requestRejoinCheck(self, avId):
		self.notify.info("requestRejoinCheck: avId(%s)" % avId)

	def requestCrewIconUpdate(self, iconKey):
		self.notify.info("requestCrewIconUpdate: iconKey(%s)" % iconKey)

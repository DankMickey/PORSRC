from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class AvatarFriendsManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("AvatarFriendsManagerUD")

    def announceGenerate(self):
        DistributedObjectUD.announceGenerate(self)
        self.invitations = {}

    def online(self):
        pass

    def requestInvite(self, avId):
        print("requestInvite: %s" % avId)


    def friendConsidering(self, avId):
        print("friendConsidering: %s" % avId)

    def invitationFrom(self, avId, avatarName):
        pass

    def retractInvite(self, avId):
        pass

    def rejectInvite(self, avId, reason):
        pass

    def requestRemove(self, avId, reason):
        pass

    def rejectRemove(self, todo0, todo1):
        pass

    def updateAvatarFriend(self, todo0, todo1):
        pass

    def removeAvatarFriend(self, todo0):
        pass

    def updateAvatarName(self, todo0, todo1):
        pass

    def avatarOnline(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def avatarOffline(self, todo0):
        pass

class AvatarHandle:
    dclassName = 'AvatarHandle'

    def getName(self):
        return ''

    def isOnline(self):
        return False

    def isUnderstandable(self):
        return True

    def setTalkWhisper(self, fromAV, avatarName, chat):
        if base.whiteList:
            chat = base.whiteList.processThroughAll(chat, base.localAvatar)

        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, chat)

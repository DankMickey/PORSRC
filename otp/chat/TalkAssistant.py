import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from otp.chat.TalkMessage import TalkMessage
import time
from otp.chat.TalkGlobals import *
from otp.chat.ChatGlobals import *
from otp.nametag.NametagConstants import CFSpeech, CFTimeout, CFThought
ThoughtPrefix = '.'

class TalkAssistant(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TalkAssistant')

    def __init__(self):
        self.logWhispers = 1
        self.whiteList = None
        self.clearHistory()
        self.zeroTimeDay = time.time()
        self.zeroTimeGame = globalClock.getRealTime()
        self.floodThreshold = 10.0
        self.useWhiteListFilter = base.config.GetBool('white-list-filter-openchat', 0)
        self.lastWhisperDoId = None
        self.lastWhisper = None
        self.SCDecoder = SCDecoders
        return

    def clearHistory(self):
        self.historyComplete = []
        self.historyOpen = []
        self.historyUpdates = []
        self.historyGuild = []
        self.historyByDoId = {}
        self.historyByDISLId = {}
        self.floodDataByDoId = {}
        self.spamDictByDoId = {}
        self.labelGuild = OTPLocalizer.TalkGuild
        self.messageCount = 0
        self.shownWhiteListWarning = 0

    def delete(self):
        self.ignoreAll()
        self.clearHistory()

    def start(self):
        pass

    def stop(self):
        pass

    def countMessage(self):
        self.messageCount += 1
        return self.messageCount - 1

    def getOpenText(self, numLines, startPoint = 0):
        return self.historyOpen[startPoint:startPoint + numLines]

    def getSizeOpenText(self):
        return len(self.historyOpen)

    def getCompleteText(self, numLines, startPoint = 0):
        return self.historyComplete[startPoint:startPoint + numLines]

    def getCompleteTextFromRecent(self, numLines, startPoint = 0):
        start = len(self.historyComplete) - startPoint
        if start < 0:
            start = 0
        backStart = max(start - numLines, 0)
        text = self.historyComplete[backStart:start]
        text.reverse()
        return text

    def getAllCompleteText(self):
        return self.historyComplete

    def getSizeCompleteText(self):
        return len(self.historyComplete)

    def addToHistoryDoId(self, message, doId):
        if message.getTalkType() == TALK_WHISPER and doId != localAvatar.doId:
            self.lastWhisperDoId = doId
            self.lastWhisper = self.lastWhisperDoId
        if not doId in self.historyByDoId:
            self.historyByDoId[doId] = []
        self.historyByDoId[doId].append(message)
        if not doId in self.floodDataByDoId:
            self.floodDataByDoId[doId] = [0.0, self.stampTime(), message]
        else:
            oldTime = self.floodDataByDoId[doId][1]
            newTime = self.stampTime()
            timeDiff = newTime - oldTime
            oldRating = self.floodDataByDoId[doId][0]
            contentMult = 1.0
            if len(message.getBody()) < 6:
                contentMult += 0.2 * float(6 - len(message.getBody()))
            if self.floodDataByDoId[doId][2].getBody() == message.getBody():
                contentMult += 1.0
            floodRating = max(0, 3.0 * contentMult + oldRating - timeDiff)
            self.floodDataByDoId[doId] = [floodRating, self.stampTime(), message]
            if floodRating > self.floodThreshold:
                if oldRating < self.floodThreshold:
                    self.floodDataByDoId[doId] = [floodRating + 3.0, self.stampTime(), message]
                    return 1
                else:
                    self.floodDataByDoId[doId] = [oldRating - timeDiff, self.stampTime(), message]
                    return 2
        return 0

    def stampTime(self):
        return globalClock.getRealTime() - self.zeroTimeGame

    def findName(self, id, isPlayer = 0):
        return self.findAvatarName(id)

    def findAvatarName(self, id):
        info = base.cr.identifyAvatar(id)
        if info:
            return info.getName()
        else:
            return ''

    def executeSlashCommand(self, text):
        pass

    def executeGMCommand(self, text):
        pass

    def isThought(self, message):
        if not message:
            return 0
        elif len(message) == 0:
            return 0
        elif message.find(ThoughtPrefix, 0, len(ThoughtPrefix)) >= 0:
            return 1
        else:
            return 0

    def removeThoughtPrefix(self, message):
        if self.isThought(message):
            return message[len(ThoughtPrefix):]
        else:
            return message

    def checkOpenSpeedChat(self):
        return True

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def checkGuildTypedChat(self):
        if localAvatar.guildId:
            return True
        return False

    def checkGuildSpeedChat(self):
        if localAvatar.guildId:
            return True
        return False

    def receiveWhisperTalk(self, avatarId, avatarName, message):
        if not avatarName and avatarId:
            avatarName = self.findAvatarName(avatarId)

        newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, avatarId, avatarName)
        self.historyComplete.append(newMessage)
        if avatarId:
            self.addToHistoryDoId(newMessage, avatarId)
        messenger.send('NewOpenMessage', [newMessage])

    def receiveGuildTalk(self, senderAvId, avatarName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_GUILD, self.countMessage(), message, senderAvId, avatarName)
            reject = self.addToHistoryDoId(newMessage, senderAvId)
            if reject == 1:
                newMessage.setBody(OTPLocalizer.AntiSpamInChat)
            if reject != 2:
                isSpam = self.spamDictByDoId.get(senderAvId) and reject
                if not isSpam:
                    self.historyComplete.append(newMessage)
                    self.historyGuild.append(newMessage)
                    messenger.send('NewOpenMessage', [newMessage])
                if newMessage.getBody() == OTPLocalizer.AntiSpamInChat:
                    self.spamDictByDoId[senderAvId] = 1
                else:
                    self.spamDictByDoId[senderAvId] = 0

    def receiveThought(self, avatarId, avatarName, message):
        if not avatarName and avatarId:
            avatarName = self.findAvatarName(avatarId)

        newMessage = TalkMessage(AVATAR_THOUGHT, self.countMessage(), message, avatarId, avatarName)
        reject = 0
        if avatarId:
            reject = self.addToHistoryDoId(newMessage, avatarId)
        if reject == 1:
            newMessage.setBody(OTPLocalizer.AntiSpamInChat)
        if reject != 2:
            self.historyComplete.append(newMessage)
            self.historyOpen.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])

    def receiveGameMessage(self, message):
        if not self.isThought(message):
            newMessage = TalkMessage(INFO_GAME, self.countMessage(), message, receiverAvatarId=localAvatar.doId, receiverAvatarName=localAvatar.getName())
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])

    def receiveSystemMessage(self, message):
        if not self.isThought(message):
            newMessage = TalkMessage(INFO_SYSTEM, self.countMessage(), message, receiverAvatarId=localAvatar.doId, receiverAvatarName=localAvatar.getName())
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])

    def receiveGuildMessage(self, senderId, senderName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_GUILD, self.countMessage(), message, senderId, senderName)
            self.historyComplete.append(newMessage)
            self.historyGuild.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])

    def receiveGuildUpdateMessage(self, message, senderId, senderName, receiverId, receiverName, extraInfo = None):
        if not self.isThought(message):
            newMessage = TalkMessage(INFO_GUILD, self.countMessage(), message, senderId, senderName, receiverId, receiverName, extraInfo)
            self.historyComplete.append(newMessage)
            self.historyGuild.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])

    def receiveFriendUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline
        else:
            onlineMessage = OTPLocalizer.FriendOffline
        newMessage = TalkMessage(UPDATE_FRIEND, self.countMessage(), onlineMessage, friendId, friendName, localAvatar.doId, localAvatar.getName())
        self.historyComplete.append(newMessage)
        self.historyUpdates.append(newMessage)
        messenger.send('NewOpenMessage', [newMessage])

    def receiveGuildUpdate(self, memberId, memberName, isOnline):
        if base.cr.identifyFriend(memberId) is None:
            if isOnline:
                onlineMessage = OTPLocalizer.GuildMemberOnline
            else:
                onlineMessage = OTPLocalizer.GuildMemberOffline
            newMessage = TalkMessage(UPDATE_GUILD, self.countMessage(), onlineMessage, memberId, memberName)
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
            self.historyGuild.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])

    def receiveAvatarWhisperSpeedChat(self, type, messageIndex, senderAvId, name = None):
        if not name and senderAvId:
            name = self.findName(senderAvId, 0)

        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)

        newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, senderAvId, name, localAvatar.doId, localAvatar.getName())
        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        self.addToHistoryDoId(newMessage, senderAvId)
        messenger.send('NewOpenMessage', [newMessage])

    def sendOpenTalk(self, message):
        try:
            message.encode('ascii')
        except UnicodeEncodeError:
            base.talkAssistant.receiveGameMessage("Non-ASCII messages are not permitted.")
            return

        if base.cr.wantMagicWords and len(message) > 0 and message[0] == '~':
            messenger.send('magicWord', [message])
        else:
            base.cr.chatAgent.sendChatMessage(message)

    def sendWhisperTalk(self, message, receiverAvId):
        # This is Pirates specific... which goes against all things OTP. But oh well.
        # Route through the PFMUD.
        base.cr.piratesFriendsManager.sendUpdate('sendTalkWhisper', [receiverAvId, message])

    def sendGuildTalk(self, message):
        if self.checkGuildTypedChat():
            base.cr.guildManager.sendTalk(message)

    def sendOpenSpeedChat(self, type, messageIndex):
        if type == SPEEDCHAT_NORMAL:
            messenger.send(SCChatEvent)
            messenger.send('chatUpdateSC', [messageIndex])
            base.localAvatar.b_setSC(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            messenger.send('chatUpdateSCEmote', [messageIndex])
            messenger.send(SCEmoteChatEvent)
            base.localAvatar.b_setSCEmote(messageIndex)
        elif type == SPEEDCHAT_CUSTOM:
            messenger.send('chatUpdateSCCustom', [messageIndex])
            messenger.send(SCCustomChatEvent)
            base.localAvatar.b_setSCCustom(messageIndex)

    def sendAvatarWhisperSpeedChat(self, type, messageIndex, receiverId):
        if type == SPEEDCHAT_NORMAL:
            base.localAvatar.whisperSCTo(messageIndex, receiverId, 0)
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            base.localAvatar.whisperSCEmoteTo(messageIndex, receiverId, 0)
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, localAvatar.getName())
        elif type == SPEEDCHAT_CUSTOM:
            base.localAvatar.whisperSCCustomTo(messageIndex, receiverId, 0)
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)

        if self.logWhispers:
            avatarName = None
            avatar = base.cr.identifyAvatar(receiverId)
            if avatar:
                avatarName = avatar.getName()
            newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, localAvatar.doId, localAvatar.getName(), receiverId, avatarName)
            self.historyComplete.append(newMessage)
            self.addToHistoryDoId(newMessage, localAvatar.doId)
            messenger.send('NewOpenMessage', [newMessage])

    def sendGuildSpeedChat(self, type, msgIndex):
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSC(msgIndex)

    def getWhisperReplyId(self):
        if self.lastWhisper:
            return self.lastWhisper

        return 0

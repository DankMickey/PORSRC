from pirates.piratesbase import PiratesGlobals
import os


class SubDetails:
    def __init__(self):
        self.subName = os.getenv('POR_PLAYCOOKIE', '???')


class AccountDetailRecord:
    def __init__(self):
        self.WLChatEnabled = False
        self.playerAccountId = PiratesGlobals.PiratesSubId
        self.playerName = os.getenv('POR_PLAYCOOKIE', '???')
        self.subDetails = {self.playerAccountId: SubDetails()}

    def canOpenChatAndNotGetBooted(self):
        return True

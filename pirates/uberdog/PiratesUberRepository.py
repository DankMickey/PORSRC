from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from pirates.coderedemption.CodeRedemptionUD import CodeRedemptionUD
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

if config.GetBool('want-rpc-server', False):
    from pirates.rpc.PiratesRPCServer import PiratesRPCServer
    from pirates.rpc.PiratesRPCHandler import PiratesRPCHandler

from DistributedInventoryManagerUD import DistributedInventoryManagerUD

from otp.ai.BanManagerUD import BanManagerUD

class PiratesUberRepository(PiratesInternalRepository):
    def __init__(self, baseChannel, serverId):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

        self.notify.setInfo(True)

    def handleConnected(self):
        PiratesInternalRepository.handleConnected(self)

        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', False):
            endpoint = config.GetString('rpc-server-endpoint', 'http://localhost:8080/')
            self.rpcServer = PiratesRPCServer(endpoint, PiratesRPCHandler(self))

        self.createManagers()
        self.createGlobals()
        self.notify.info('Done.')

    def createManagers(self):
        self.inventoryMgr = DistributedInventoryManagerUD(self)
        self.banMgr = BanManagerUD(self)
        
    def createGlobals(self):
        self.csm = self.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.piratesFriendsManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_FRIENDS_MANAGER, 'PiratesFriendsManager')
        self.matchMaker = self.generateGlobalObject(OTP_DO_ID_PIRATES_MATCH_MAKER, 'DistributedMatchMaker')
        self.guildManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_GUILD_MANAGER, 'DistributedGuildManager')
        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
        self.crewMatchManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_CREW_MATCH_MANAGER, 'DistributedCrewMatchManager')
        self.codeRedemption = self.generateGlobalObject(OTP_DO_ID_PIRATES_CODE_REDEMPTION, 'CodeRedemption')

    def _isValidPlayerLocation(self, parentId, zoneId):
        return True

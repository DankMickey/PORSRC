from panda3d.core import Datagram
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.distributed import OtpDoGlobals

from pirates.uberdog.ClientServicesManagerUD import RemoteAccountDB

class BanFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanFSM')
    
    def __init__(self, mgr):
        FSM.__init__(self, 'BanFSM')
        self.mgr = mgr
        
    def enterStart(self, bannerId, avId, accountId, duration, banReason):
        self.bannerId = bannerId
        self.avId = avId
        self.accountId = accountId
        self.duration = duration
        self.banReason = banReason
        
        self.demand('RetrieveBanner')

    def enterRetrieveBanner(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.bannerId, self.__handleRetrieveBanner)

    def __handleRetrieveBanner(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Banner object was not found in the database!')
            return

        self.bannerName = fields['setName'][0]
        self.banner = '%s (%s)' % (self.bannerName, self.bannerId)
        self.demand('RetrieveAccount')
        
    def enterRetrieveAccount(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.accountId, self.__handleRetrieveAccount)

    def __handleRetrieveAccount(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['AccountUD']:
            self.demand('Error', 'Banner object was not found in the database!')
            return
        
        self.targetUsername = fields['ACCOUNT_ID']
        self.demand('Ban')
        
    def enterBan(self):
        self.mgr.air.csm.accountDB.getBannedStatus(self.targetUsername, self.duration, self.__handleBannedAccount)
    
    def __handleBannedAccount(self, success, error):
        self.mgr.callback(self, success, error)
    
    def enterError(self, error):
        self.mgr.callback(self, False, error)

class BanManagerUD(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerUD')

    def __init__(self, air):
        self.air = air
        self.accept('BANMGR_ban', self.banUD)

    def banUD(self, bannerId, avId, accountId, duration, banReason):
        BanFSM(self).demand('Start', bannerId, avId, accountId, duration, banReason)
        
    def callback(self, fsm, success, error):            
        avId = self.air.csm.GetPuppetConnectionChannel(fsm.bannerId)
        if not success:
            # Better notify the banner
            msg = 'Failed to ban %s: %s' % (fsm.targetUsername, error)
            self.air.systemMessage(msg, avId)
            self.notify.warning(msg)
            return

        dg = PyDatagram()
        dg.addServerHeader(self.air.csm.GetPuppetConnectionChannel(fsm.avId), self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(152)
        dg.addString(fsm.banReason)
        self.air.send(dg)

        msg = '%s banned %s for %s hours: %s' % (fsm.banner, fsm.targetUsername, fsm.duration, fsm.banReason)
        
        if fsm.duration:
            self.air.systemMessage('You banned %s for %s hours!' % (fsm.targetUsername, fsm.duration), avId)
        else:
            self.air.systemMessage('You terminated %s!' % fsm.targetUsername, avId)
        self.notify.info(msg)
        self.air.writeServerEvent('banned', accountId=fsm.accountId, username=fsm.targetUsername, moreInfo=msg)

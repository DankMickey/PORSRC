from direct.directnotify import DirectNotifyGlobal
import sys, os
from datetime import datetime
from pirates.analytics import AnalyticsGlobals

__all__ = [
    "AnalyticsTracker",
]

class AnalyticsManager:
    notify = DirectNotifyGlobal.directNotify.newCategory('AnalyticsManager')

    def __init__(self):
        self.application_name = config.GetString("splunk-application", "por-server")
        self.splunk_info = {
            'host': config.GetString('splunk-host', 'localhost'),
            'port': config.GetInt('splunk-port', 8089),
            'scheme': config.GetString('splunk-scheme', 'http'),
            'owner': config.GetString('splunk-owner', ''),
            'app': config.GetString('splunk-app-namespace', ''),
            'token': config.GetString('splunk-token', ''),
            'autologin': True
        }
        self.index=AnalyticsGlobals.ANALYTICS_INDEX_NAME
        self.con = None

        try:
            from pirates.analytics.SplunkCon import SplunkCon
            self.con = SplunkCon(self.application_name, self.splunk_info, self.index)
        except Exception, e:
            self.notify.warning("Failed to initalize Analytics.")
            self.notify.warning(str(e))
            self.con = None
            return

        self.notify.info("Analytics Started!")

    def isReady(self):
        return self.con != None

    def track(self, event_name, time = None, distinct_id = None, **props):
        if not self.con: 
            return False

        self.con.track(event_name, time, distinct_id, props)
        return True
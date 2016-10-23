from direct.directnotify import DirectNotifyGlobal
import AnalyticsGlobalsAI

class AnalyticsManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('AnalyticsManagerAI')

    def __init__(self):
        self.applicationName = config.GetString('splunk-application', 'por-server')
        self.host = config.GetString('splunk-host', '').split(':')
        self.conn = None
        
        if not self.host[0]:
            self.notify.info('Not using analytics.')
            return

        try:
            from SplunkConnectionAI import SplunkConnectionAI
        except:
            self.notify.warning('Not using analytics - splunklib missing.')
            return

        self.splunkInfo = {
            'host': self.host[0],
            'port': (int(self.host[1]) if len(self.host) > 1 else 8088),
            'scheme': config.GetString('splunk-scheme', 'http'),
            'token': config.GetString('splunk-token', '')
        }

        self.index = config.GetString('splunk-index-name', AnalyticsGlobalsAI.ANALYTICS_INDEX_NAME)
        self.conn = None

        try:
            self.conn = SplunkConnectionAI(self.applicationName, self.splunkInfo, self.index)
        except Exception, e:
            self.notify.warning('Failed to initialize analytics.')
            self.notify.warning(str(e))
            self.conn = None
            return

        self.notify.info('Connected to Splunk.')

    def isReady(self):
        return self.conn != None

    def track(self, event_name, time = None, distinct_id = None, props={}):
        if not self.conn: 
            return False

        self.conn.track(event_name, time, distinct_id, **props)
        return True
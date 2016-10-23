from direct.directnotify import DirectNotifyGlobal
from datetime import datetime
import splunklib.client as client
import AnalyticsGlobalsAI

class SplunkConnectionAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('SplunkCon')

    def __init__(self, applicationName, splunkInfo, index=AnalyticsGlobalsAI.ANALYTICS_INDEX_NAME):
        self.applicationName = applicationName
        self.splunk = client.connect(**splunkInfo)
        self.index = index

    @staticmethod
    def encode(props):
        encoded = " "

        for k,v in props.iteritems():
            # We disallow dictionaries - it doesn't quite make sense.
            assert(not isinstance(v, dict))

            # We do not allow lists
            assert(not isinstance(v, list))

            # This is a hack to escape quotes
            if isinstance(v, str):
                v = v.replace('"', "'")

            encoded += ('%s%s="%s" ' % (AnalyticsGlobalsAI.PROPERTY_PREFIX, k, v))

        return encoded

    def __counts(self, job, result_key):
        reader = results.ResultsReader(job.results())

        return [{'name': result[result_key], 'count': int(result['count'] or 0)} for result in reader if isinstance(result, dict)]

    def getApplication(self, appName):
        if appName in self.client.apps:
            return self.client.apps[appName]

    def applications(self):
        query = "search index=%s | stats count by application" % (self.index)
        job = self.splunk.jobs.create(query, exec_mode="blocking")
        return self.__counts(job, "application")

    def events(self):          
        query = "search index=%s application=%s | stats count by event" % (self.index, self.applicationName)
        job = self.splunk.jobs.create(query, exec_mode="blocking")
        return self.__counts(job, "event")

    def track(self, event_name, time = None, distinct_id = None, **props):
        self.notify.info("Logging %s..." % event_name)

        if time is None:
            time = datetime.now().isoformat()
            
        event = '%s %s="%s" %s="%s" ' % (
            time,
            AnalyticsGlobalsAI.APPLICATION_KEY, self.applicationName, 
            AnalyticsGlobalsAI.EVENT_KEY, event_name)

        assert(not AnalyticsGlobalsAI.APPLICATION_KEY in props.keys())
        assert(not AnalyticsGlobalsAI.EVENT_KEY in props.keys())

        if distinct_id is not None:
            event += ('%s="%s" ' % (AnalyticsGlobalsAI.DISTINCT_KEY, distinct_id))
            assert(not AnalyticsGlobalsAI.DISTINCT_KEY in props.keys())

        event += self.encode(props)

        self.splunk.indexes[self.index].submit(event, sourcetype=AnalyticsGlobalsAI.ANALYTICS_SOURCETYPE)

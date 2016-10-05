from direct.directnotify import DirectNotifyGlobal
import sys, os
from datetime import datetime
try:
	import splunklib.client as client
except ImportError:
	raise Exception(":SplunkCon: Failed to initialize Analytics. Splunk SDK not installed.")
import AnalyticsGlobals

__all__ = [
    "AnalyticsTracker",
]

class SplunkCon:
    notify = DirectNotifyGlobal.directNotify.newCategory('SplunkCon')

    def __init__(self, application_name, splunk_info, index=AnalyticsGlobals.ANALYTICS_INDEX_NAME):
        self.application_name = application_name
        self.splunk = client.connect(**splunk_info)
        self.index = index

        if not self.index in self.splunk.indexes:
            self.splunk.indexes.create(self.index)
        assert(self.index in self.splunk.indexes)

        if AnalyticsGlobals.ANALYTICS_SOURCETYPE not in self.splunk.confs['props']:
            self.splunk.confs["props"].create(AnalyticsGlobals.ANALYTICS_SOURCETYPE)
            stanza = self.splunk.confs["props"][AnalyticsGlobals.ANALYTICS_SOURCETYPE]
            stanza.submit({
                "LINE_BREAKER": "(%s)" % AnalyticsGlobals.EVENT_TERMINATOR,
                "CHARSET": "UTF-8",
                "SHOULD_LINEMERGE": "false"
            })
        assert(AnalyticsGlobals.ANALYTICS_SOURCETYPE in self.splunk.confs['props'])
        
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

            encoded += ('%s%s="%s" ' % (AnalyticsGlobals.PROPERTY_PREFIX, k, v))

        return encoded

    def __counts(self, job, result_key):
    	applications = []
    	reader = results.ResultsReader(job.results())
    	for result in reader:
    		if isinstance(result, dict):
    			applications.append({
    				"name": result[result_key],
    				"count": int(result["count"] or 0)
    				})
   		return applications

    def getApplication(self, appName):
        app = None
        if appName in self.client.apps:
            app = self.client.apps[appName]
        return app

    def applications(self):
        query = "search index=%s | stats count by application" % (self.index)
        job = self.splunk.jobs.create(query, exec_mode="blocking")
        return self.__counts(job, "application")

    def events(self):  		
        query = "search index=%s application=%s | stats count by event" % (self.index, self.application_name)
        job = self.splunk.jobs.create(query, exec_mode="blocking")
        return self.__counts(job, "event")

    def track(self, event_name, time = None, distinct_id = None, **props):
        if time is None:
            time = datetime.now().isoformat()
            
        event = '%s %s="%s" %s="%s" ' % (
            time,
            AnalyticsGlobals.APPLICATION_KEY, self.application_name, 
            AnalyticsGlobals.EVENT_KEY, event_name)

        assert(not AnalyticsGlobals.APPLICATION_KEY in props.keys())
        assert(not AnalyticsGlobals.EVENT_KEY in props.keys())

        if distinct_id is not None:
            event += ('%s="%s" ' % (AnalyticsGlobals.DISTINCT_KEY, distinct_id))
            assert(not AnalyticsGlobals.DISTINCT_KEY in props.keys())

        event += AnalyticsTracker.encode(props)

        self.splunk.indexes[self.index].submit(event, sourcetype=AnalyticsGlobals.ANALYTICS_SOURCETYPE)

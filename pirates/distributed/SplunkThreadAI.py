from direct.distributed.AstronInternalRepository import msgpack_encode
from direct.distributed.PyDatagram import PyDatagram
from threading import Thread

class SplunkThreadAI(Thread):

    def run(self):
        while True:
            item = simbase.air.logQueue.get()

            if not simbase.air.analyticsMgr.isReady():
                if simbase.air.eventSocket is not None:
                    dg = PyDatagram()
                    msgpack_encode(dg, item)
                    simbase.air.eventSocket.Send(dg.getMessage())
            else:
                del item['type']
                simbase.air.analyticsMgr.track(logType, item)

            simbase.air.logQueue.task_done()
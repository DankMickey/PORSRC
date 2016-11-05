from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task
from pirates.inventory.DistributedLootContainerAI import DistributedLootContainerAI

class DistributedLootManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.containers = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.purgeContainers = taskMgr.doMethodLater(15, self.__removeContainers, 'purgeContainers')

    def delete(self):
        DistributedObjectAI.delete(self)
        taskMgr.remove(self.purgeContainers)
        
        for containerId in self.containers:
            self.deleteContainer(containerId)

    def spawnLoot(self, npc):
        return # Temporarily disabled
        try:
            gameArea = npc.spawner.spawner.gameArea
            
            if not gameArea:
                self.notify.warning("Failed to spawn Loot. '%s' has no game area" % npc)
                return

            container = DistributedLootContainerAI.makeFromObjectData(self.air, npc)
            self.containers[container.getUniqueId()] = container
            gameArea.generateChild(container)
            self.notify.info("Loot Spawned")
        except Exception, e:
             self.notify.warning("Failed to spawn Loot. An unknown error has occured")
             self.notify.warning(e)

    def __removeContainers(self, task=None):
        garbage = []

        for containerId, container in self.containers.iteritems():
            container.tick()
            
            if container.getEmpty() or container.getTimeout() <= 0:
                garbage.append(containerId)
        
        for containerId in garbage:
            self.deleteContainer(containerId)

        return Task.again

    def deleteContainer(self, containerId):
        self.containers[containerId].delete()
        del self.containers[containerId]

    def requestItemFromContainer(self, containerId, itemInfo):
        pass

    def requestItems(self, containers): 
        pass
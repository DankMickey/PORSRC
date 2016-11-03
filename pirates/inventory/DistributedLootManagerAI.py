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
        self.purgeContainers = taskMgr.doMethodLater(15, self.__removeEmptyContainers, 'purgeContainers')

    def delete(self):
        DistributedObjectAI.delete(self)
        taskMgr.remove(self.purgeContainers)
        if len(self.containers) > 0:
            for containerId in self.containers:
                self.deleteContainer(containerId)

    def spawnLoot(self, avatar):
        try: 
            gameArea = avatar.spawner.spawner.gameArea
            if not gameArea:
                self.notify.warning("Failed to spawn Loot. '%s' has no game area" % avatar)
                return

            container = DistributedLootContainerAI.makeFromObjectData(self.air, avatar)
            self.containers[container.getUniqueId()] = container
            gameArea.generateChild(container, cellParent=False)
            self.notify.info("Loot Spawned")

        except Exception, e:
             self.notify.warning("Failed to spawn Loot. An unknown error has occured")
             self.notify.warning(e)

    def __removeEmptyContainers(self, task=None):
        garbage = []
        if len(self.containers) > 0:
            for containerId in self.containers:
                container = self.containers[containerId]
                if container.getEmpty():
                    garbage.append(containerId)

        if len(garbage) > 0:
            for trash in garbage:
                self.deleteContainer(trash)
        return Task.again

    def deleteContainer(self, containerId):
        pass

    def requestItemFromContainer(self, containerId, itemInfo):
        pass

    def requestItems(self, containers): 
        pass
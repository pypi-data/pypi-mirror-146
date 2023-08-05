from python_helper import ObjectHelper
from python_framework import Repository

from enumeration.ModelState import ModelState


MESSAGE_MODEL = 'message'
EMISSION_MODEL = 'emission'


@Repository()
class MemoryRepository:

    messageDictionary = {}


    def existsMessageByQueueKeyAndMessageKey(self, queueKey, messageKey):
        return messageKey in self.getMessageQueue(queueKey)


    def findAllMessagesByStateIn(self, stateList):
        return [
            self.getMessage(queueKey, messageKey)
            for queueKey in self.getQueueKeyIterator()
            for messageKey in self.getMessageKeyIterator(queueKey)
            if self.messageStateIn(queueKey, messageKey, stateList)
        ]










    def getEmissionList(self, queueKey, messageKey):
        return self.getEmissionQueue(queueKey).get(messageKey, [])


    def findAllEmissionsByStateIn(self, stateList):
        return [
            emission
            for queueKey in self.getQueueKeyIterator()
            for messageKey in self.getEmissionMessageKeyIterator(queueKey)
            for emission in self.getEmissionList(queueKey, messageKey)
            if self.emissionStateIn(emission, stateList)
        ]


    def findAllEmissionsByStatusInFromOneQueue(self, statusList):
        queueKeyList = self.getQueueKeyIterator()
        if ObjectHelper.isEmpty(queueKeyList):
            return []
        for queueKey in queueKeyList:
            modelList = [
                emission
                for messageKey in self.getMessageKeyIterator(queueKey)
                for emission in self.getEmissionList(queueKey, messageKey)
                if self.emissionStatusIn(emission, statusList)
            ]
            if 0 < len(modelList):
                return modelList
        return []


    def emissionStatusIn(self, emission, statusList):
        return ObjectHelper.isNotNone(emission) and emission.status in statusList
        # return ObjectHelper.isNotNone(emission) and emission.status in statusList and self.emissionStateIn(
        #     emission,
        #     [
        #         ModelState.MODIFIED,
        #         ModelState.INSTANTIATED
        #     ]
        # )


    def emissionStateIn(self, emission, stateList):
        return ObjectHelper.isNotNone(emission) and emission.state in stateList












    def removeAllMessagesByStateIn(self, stateList):
        modelList = [
            self.popMessage(queueKey, messageKey)
            for queueKey in self.getQueueKeyIterator()
            for messageKey in self.getMessageKeyIterator(queueKey)
            if self.messageStateIn(queueKey, messageKey, stateList)
        ]
        self.removeEmptyQueues()
        return modelList


    def findAllMessagesByStatusIn(self, statusList):
        return [
            self.getMessage(queueKey, messageKey)
            for queueKey in self.getQueueKeyIterator()
            for messageKey in self.getMessageKeyIterator(queueKey)
            if self.messageStatusIn(queueKey, messageKey, statusList)
        ]


    def removeAllMessageByStatusIn(self, statusList):
        modelList = [
            self.popMessage(queueKey, messageKey)
            for queueKey in self.getQueueKeyIterator()
            for messageKey in self.getMessageKeyIterator(queueKey)
            if self.messageStatusIn(queueKey, messageKey, statusList)
        ]
        self.removeEmptyQueues()
        return modelList


    def findAllMessagesByStatusInFromOneQueue(self, statusList):
        queueKeyList = self.getQueueKeyIterator()
        if ObjectHelper.isEmpty(queueKeyList):
            return []
        for queueKey in queueKeyList:
            modelList = [
                self.getMessage(queueKey, messageKey)
                for messageKey in self.getMessageKeyIterator(queueKeyList[0])
                if self.messageStatusIn(queueKey, messageKey, statusList)
            ]
            if 0 < len(modelList):
                return modelList
        return []


    def removeEmptyQueues(self):
        for queueKey in self.getQueueKeyIterator():
            if ObjectHelper.isEmpty(self.getMessageQueue(queueKey)) and ObjectHelper.isEmpty(self.getEmissionQueue(queueKey)):
                ObjectHelper.deleteDictionaryEntry(queueKey)


    def getMessageKeyIterator(self, queueKey):
        return [*self.getMessageQueue(queueKey).keys()]


    def getEmissionMessageKeyIterator(self, queueKey):
        return [*self.getEmissionQueue(queueKey).keys()]


    def getMessage(self, queueKey, messageKey):
        return self.getMessageQueue(queueKey).get(messageKey)


    def popMessage(self, queueKey, messageKey):
        return self.getMessageQueue(queueKey).pop(messageKey)


    def getMessageQueue(self, queueKey):
        return self.getQueue(queueKey).get(MESSAGE_MODEL, {})


    def getEmissionQueue(self, queueKey):
        return self.getQueue(queueKey).get(EMISSION_MODEL, {})


    def messageStateIn(self, queueKey, messageKey, stateList):
        return ObjectHelper.isNotNone(self.getMessage(queueKey, messageKey)) and self.getMessage(queueKey, messageKey).state in stateList


    def messageStatusIn(self, queueKey, messageKey, statusList):
        return ObjectHelper.isNotNone(self.getMessage(queueKey, messageKey)) and self.getMessage(queueKey, messageKey).status in statusList
        # return ObjectHelper.isNotNone(self.getMessage(queueKey, messageKey)) and self.getMessage(queueKey, messageKey).status in statusList and self.messageStateIn(
        #     queueKey,
        #     messageKey,
        #     [
        #         ModelState.MODIFIED,
        #         ModelState.INSTANTIATED
        #     ]
        # )


    def acceptMessage(self, message):
        self.addQueueKeyIfNeeded(message.queueKey)
        self.messageDictionary[message.queueKey][MESSAGE_MODEL][message.key] = message


    def acceptEmissionList(self, emissionList, queue):
        if ObjectHelper.isNotEmpty(emissionList):
            message = emissionList[0].message
            self.addQueueKeyIfNeeded(queue.key)
            self.messageDictionary[queue.key][EMISSION_MODEL][message.key] = emissionList


    def addQueueKeyIfNeeded(self, queueKey):
        if queueKey not in self.messageDictionary:
            self.messageDictionary[queueKey] = {
                MESSAGE_MODEL: {},
                EMISSION_MODEL: {}
            }


    def getQueueKeyIterator(self):
        return [*{**self.messageDictionary}.keys()]


    def getQueue(self, queueKey):
        return self.messageDictionary.get(queueKey, {})

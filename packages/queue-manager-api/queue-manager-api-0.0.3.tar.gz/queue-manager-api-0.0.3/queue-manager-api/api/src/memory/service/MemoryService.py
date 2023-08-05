from python_helper import log, ObjectHelper
from python_framework import Service, ServiceMethod

import Message, Emission, QueueModel
from enumeration.ModelState import ModelState
from enumeration.ModelStatus import ModelStatus


LOG_LEVEL = log.STATUS


@Service()
class MemoryService:

    @ServiceMethod()
    def findAll(self):
        return self.repository.memory.messageDictionary


    @ServiceMethod(requestClass=[Message.Message])
    def acceptMessage(self, message):
        self.validator.memory.validateMessageDoesNotExists(message)
        log.prettyPython(self.acceptMessage, f'Accepting new queued message', message, logLevel=LOG_LEVEL)
        return self.repository.memory.acceptMessage(message)


    @ServiceMethod(requestClass=[[Emission.Emission], QueueModel.QueueModel])
    def acceptEmissionList(self, emissionList, queue):
        self.validator.memory.validateThereAreAtLeastOneEmission(emissionList, queue)
        log.prettyPython(self.acceptEmissionList, f'Accepting queued message emissions', emissionList, logLevel=LOG_LEVEL)
        return self.repository.memory.acceptEmissionList(emissionList, queue)


    @ServiceMethod(requestClass=[Message.Message])
    def messageExists(self, message):
        return self.repository.memory.existsMessageByQueueKeyAndMessageKey(message.queueKey, message.key)


    @ServiceMethod()
    def getAllInstantiatedMessages(self):
        return self.repository.memory.findAllMessagesByStateIn([ModelState.INSTANTIATED])


    @ServiceMethod()
    def getAllInstantiatedEmissions(self):
        return self.repository.memory.findAllEmissionsByStateIn([ModelState.INSTANTIATED])


    @ServiceMethod()
    def getAllAcceptedMessages(self):
        return self.repository.memory.findAllMessagesByStatusIn([ModelStatus.ACCEPTED])


    @ServiceMethod()
    def getAllModifiedMessages(self):
        return self.repository.memory.findAllMessagesByStateIn([
            ModelState.INSTANTIATED,
            ModelState.MODIFIED
        ])


    @ServiceMethod()
    def getAllAcceptedMessagesFromOneQueue(self):
        return self.repository.memory.findAllMessagesByStatusInFromOneQueue([ModelStatus.ACCEPTED])


    @ServiceMethod()
    def getAcceptedEmissionsFromOneQueue(self):
        return self.repository.memory.findAllEmissionsByStatusInFromOneQueue([ModelStatus.ACCEPTED])


    @ServiceMethod()
    def getAllModifiedEmissions(self):
        return self.repository.memory.findAllEmissionsByStateIn([
            ModelState.INSTANTIATED,
            ModelState.MODIFIED
        ])


    @ServiceMethod()
    def removeAllProcessedMessages(self):
        messageList = self.repository.memory.removeAllMessagesByStateIn([ModelState.PROCESSED])
        if ObjectHelper.isEmpty(messageList):
            return []
        self.service.messageModel.createOrUpdateAll(messageList)
        log.prettyPython(self.removeAllProcessedMessages, 'Messages removed from memory', messageList, logLevel=LOG_LEVEL)
        return messageList

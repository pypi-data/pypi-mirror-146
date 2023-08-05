from python_framework import Serializer, HttpStatus
from MessageEmitterAnnotation import MessageEmitter
from MessageEmitterAnnotation import MessageEmitterMethod

from config import MessageConfig
import MessageDto
import Message


@MessageEmitter(
    muteLogs = False,
    logRequest = True,
    logResponse = True,
    timeout = MessageConfig.EMITTER_TIMEOUT,
    headers = {'Content-Type': 'application/json'}
)
class MessageEmitter:

    @MessageEmitterMethod(
        logRequest = True,
        logResponse = True,
        requestClass=[MessageDto.MessageRequestDto, str],
        responseClass=[MessageDto.MessageRequestDto]
    )
    def send(self, dto, destinyUri):
        return self.emit(additionalUrl=destinyUri, body=Serializer.getObjectAsDictionary(dto))

from python_helper import log
from python_framework import HttpStatus, FlaskUtil
from MessageListenerAnnotation import MessageListener
from MessageListenerAnnotation import MessageListenerMethod

from config import MessageConfig
import MessageDto
import Message


@MessageListener(
    url = '/api/queue/subscription/message/listener',
    timeout = MessageConfig.LISTENER_TIMEOUT
    , logRequest = True
    , logResponse = True
    , muteLogs = False
)
class MessageListener:

    @MessageListenerMethod(requestClass=[MessageDto.MessageRequestDto])
    def accept(self, dto):
        self.service.message.globals.api.resource.emitter.message.send(dto, 'https://some-url')
        responseDto = self.service.message.acceptWithoutValidation(dto)
        return responseDto, HttpStatus.ACCEPTED

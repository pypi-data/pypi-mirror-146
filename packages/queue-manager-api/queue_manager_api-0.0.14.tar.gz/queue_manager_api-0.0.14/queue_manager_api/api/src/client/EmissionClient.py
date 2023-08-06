from python_framework import Serializer, HttpStatus, HttpClient, HttpClientMethod

from config import MessageConfig
import MessageDto
import Emission


@HttpClient(
    # muteLogs = False,
    logRequest = True,
    logResponse = True,
    timeout = MessageConfig.EMITTER_TIMEOUT,
    headers = {'Content-Type': 'application/json'}
)
class EmissionClient:

    @HttpClientMethod(
        logRequest = True,
        logResponse = True,
        requestClass = [str, MessageDto.MessageRequestDto],
        responseClass = [MessageDto.MessageResponseDto]
    )
    def send(self, url, dto):
        return self.post(
            additionalUrl = url,
            body = Serializer.getObjectAsDictionary(dto)
        )

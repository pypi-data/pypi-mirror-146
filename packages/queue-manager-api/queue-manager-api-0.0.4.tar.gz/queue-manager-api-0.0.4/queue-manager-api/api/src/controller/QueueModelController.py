from python_framework import Controller, ControllerMethod, HttpStatus

from enumeration.AccessDomain import AccessDomain
import QueueDto


@Controller(url = '/queue', tag='Queue', description='Queue controller')
class QueueModelController:

    @ControllerMethod(url = '/',
        apiKeyRequired = [AccessDomain.API],
        requestClass = [QueueDto.QueueRequestDto],
        responseClass = [QueueDto.QueueResponseDto]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self, dto):
        return self.service.queueModel.createOrUpdate(dto), HttpStatus.CREATED

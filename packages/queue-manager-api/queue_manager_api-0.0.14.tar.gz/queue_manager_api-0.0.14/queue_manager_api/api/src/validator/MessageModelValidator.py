from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import MessageDto


@Validator()
class MessageModelValidator:

    @ValidatorMethod(requestClass=[MessageDto.MessageRequestDto])
    def validateRequestDto(self, dto):
        if ObjectHelper.isNone(dto) or ObjectHelper.isNone(dto.key):
            raise GlobalException(
                logMessage = f'Message key cannot be None. Message dto: {dto}',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )


    @ValidatorMethod(requestClass=[MessageDto.MessageRequestDto])
    def validateDoesNotExists(self, dto):
        self.validateRequestDto(dto)
        self.validateDoesNotExistsByKey(dto.key)


    @ValidatorMethod(requestClass=[str])
    def validateDoesNotExistsByKey(self, key):
        if ObjectHelper.isNone(key) or self.service.messageModel.existsByKey(key):
            raise GlobalException(
                message = 'Message aleady exists',
                logMessage = f'Message {key} aleady exists',
                status = HttpStatus.BAD_REQUEST
            )

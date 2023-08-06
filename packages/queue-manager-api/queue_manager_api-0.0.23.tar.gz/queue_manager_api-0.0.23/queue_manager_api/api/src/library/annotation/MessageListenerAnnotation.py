from python_helper import Constant as c
from python_helper import ReflectionHelper, ObjectHelper, log, Function, StringHelper
from python_framework import (
    FlaskManager,
    GlobalException,
    ConverterStatic,
    Listener,
    ListenerMethod,
    FlaskUtil,
    Serializer,
    ConfigurationKeyConstant,
    EncapsulateItWithGlobalException,
    OpenApiManager,
    HttpStatus,
    HttpDomain,
    LogConstant
)

try:
    from queue_manager_api.api.src.library.util import AnnotationUtil
    from queue_manager_api.api.src.library.util import ThreadUtil
    from queue_manager_api.api.src.library.constant import MessageConstant
    from queue_manager_api.api.src.library.dto import MessageDto
except:
    import AnnotationUtil, ThreadUtil
    import MessageConstant
    import MessageDto


DEFAULT_TIMEOUT = 2


@Function
def MessageListener(
    *resourceArgs,
    url = c.SLASH,
    timeout = DEFAULT_TIMEOUT,
    responseHeaders = None,
    logRequest = False,
    logResponse = False,
    enabled = None,
    muteLogs = None,
    **resourceKwargs
):
    def Wrapper(OuterClass, *outterArgs, **outterKwargs):
        resourceUrl = url
        resourceTimeout = timeout
        resourceLogRequest = logRequest
        resourceLogResponse = logResponse
        resourceEnabled = enabled
        resourceMuteLogs = muteLogs
        resourceInstanceResponseHeaders = responseHeaders
        log.wrapper(MessageListener, f'''wrapping {OuterClass.__name__}(*{outterArgs}, **{outterKwargs})''')
        api = FlaskManager.getApi()
        class InnerClass(OuterClass):
            url = resourceUrl
            responseHeaders = resourceInstanceResponseHeaders
            logRequest = resourceLogRequest
            logResponse = resourceLogResponse
            enabled = resourceEnabled
            muteLogs = resourceMuteLogs
            def __init__(self, *args, **kwargs):
                log.wrapper(OuterClass, f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self, *args,**kwargs)
                AnnotationUtil.initializeComunicationLayerResource(
                    resourceInstance = self,
                    api = api,
                    timeout = resourceTimeout,
                    enabled = resourceEnabled,
                    muteLogs = resourceMuteLogs,
                    logRequest = resourceLogRequest,
                    logResponse = resourceLogResponse,
                    resourceEnabledConfigKey = ConfigurationKeyConstant.API_LISTENER_ENABLE,
                    resourceMuteLogsConfigKey = ConfigurationKeyConstant.API_LISTENER_MUTE_LOGS,
                    resourceTimeoutConfigKey = ConfigurationKeyConstant.API_LISTENER_TIMEOUT
                )
                self.threadManager = ThreadUtil.ThreadManager(threadTimeout=self.timeout)
        ReflectionHelper.overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper


@Function
def MessageListenerMethod(
    *methodArgs,
    url = c.SLASH,
    timeout = DEFAULT_TIMEOUT,
    requestHeaderClass = None,
    requestParamClass = None,
    requestClass = None,
    responseClass = None,
    responseHeaders = None,
    apiKeyRequired = None,
    consumes = OpenApiManager.DEFAULT_CONTENT_TYPE,
    produces = OpenApiManager.DEFAULT_CONTENT_TYPE,
    logRequest = True,
    logResponse = True,
    enabled = True,
    muteLogs = False,
    muteStacktraceOnBusinessRuleException = True,
    **methodKwargs
):
    def innerMethodWrapper(resourceInstanceMethod, *innerMethodArgs, **innerMethodKwargs):
        resourceInstanceMethodUrl = url
        wrapperManager = AnnotationUtil.InnerMethodWrapperManager(
            wrapperType = MessageListenerMethod,
            resourceInstanceMethod = resourceInstanceMethod,
            timeout = timeout,
            enabled = enabled,
            muteLogs = muteLogs,
            logRequest = logRequest,
            logResponse = logResponse,
            resourceTypeName = FlaskManager.KW_LISTENER_RESOURCE,
            resourceEnabledConfigKey = ConfigurationKeyConstant.API_LISTENER_ENABLE,
            resourceMuteLogsConfigKey = ConfigurationKeyConstant.API_LISTENER_MUTE_LOGS,
            resourceTimeoutConfigKey = ConfigurationKeyConstant.API_LISTENER_TIMEOUT
        )
        resourceInstanceMethodMuteStacktraceOnBusinessRuleException = muteStacktraceOnBusinessRuleException
        listenerUrl = f'{wrapperManager.api.baseUrl}{resourceInstanceMethodUrl}'
        if listenerUrl.endswith(c.SLASH):
            listenerUrl = listenerUrl[:-1]
        @wrapperManager.api.app.route(listenerUrl, methods=['POST'], endpoint=f'{resourceInstanceMethod.__qualname__}')
        def innerResourceInstanceMethod(*args, **kwargs):
            args = wrapperManager.addResourceInFrontOfArgs(args)
            messageAsJson = FlaskUtil.safellyGetRequestBody()
            if not wrapperManager.muteLogs:
                log.info(wrapperManager.resourceInstanceMethod, f'''{LogConstant.LISTENER_SPACE}{FlaskUtil.safellyGetVerb()}{c.SPACE_DASH_SPACE}{FlaskUtil.safellyGetUrl()}''')

            if not wrapperManager.enabled:
                completeResponse = FlaskManager.getCompleteResponseByException(
                    GlobalException(logMessage='This resource is temporarily disabled', status=HttpStatus.SERVICE_UNAVAILABLE),
                    wrapperManager.resourceInstance,
                    wrapperManager.resourceInstanceMethod,
                    resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
                    context = HttpDomain.LISTENER_CONTEXT
                )
            elif ObjectHelper.isEmpty(messageAsJson):
                completeResponse = FlaskManager.getCompleteResponseByException(
                    GlobalException(message='Content cannot be empty', logResponse=f'Content: {messageContent}', status=HttpStatus.BAD_REQUEST),
                    wrapperManager.resourceInstance,
                    wrapperManager.resourceInstanceMethod,
                    resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
                    context = HttpDomain.LISTENER_CONTEXT
                )
            else:
                # wrapperManager.resourceInstance.threadManager.runInAThread(
                    # resolveListenerCall,
                resolveListenerCall(
                    args,
                    kwargs,
                    wrapperManager,
                    requestHeaderClass,
                    requestParamClass,
                    requestClass,
                    messageAsJson.get(MessageConstant.MESSAGE_CONTENT_KEY, {}),
                    responseClass,
                    responseHeaders,
                    consumes,
                    produces,
                    resourceInstanceMethodMuteStacktraceOnBusinessRuleException
                )
                completeResponse = [
                    MessageDto.MessageCreationResponseDto(
                        key = messageAsJson.get(MessageConstant.MESSAGE_KEY_KEY),
                        queueKey = messageAsJson.get(MessageConstant.MESSAGE_QUEUE_KEY_KEY),
                        groupKey = messageAsJson.get(MessageConstant.MESSAGE_GROUP_KEY)
                    ),
                    {},
                    HttpStatus.ACCEPTED
                ]

            httpResponse = FlaskUtil.buildHttpResponse(completeResponse[1], completeResponse[0], completeResponse[-1].enumValue, produces)
            if wrapperManager.shouldLogResponse():
                try:
                    resourceMethodResponseStatus = completeResponse[-1]
                    log.prettyJson(
                        wrapperManager.resourceInstanceMethod,
                        LogConstant.LISTENER_RESPONSE,
                        {
                            'headers': FlaskUtil.safellyGetResponseHeaders(httpResponse),
                            'body': FlaskUtil.safellyGetFlaskResponseJson(httpResponse),
                            'status': resourceMethodResponseStatus.enumValue
                        },
                        condition = True,
                        logLevel = log.INFO
                    )
                except Exception as exception:
                    log.failure(innerResourceInstanceMethod, 'Not possible to log response properly', exception)

            return httpResponse
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, wrapperManager.resourceInstanceMethod)
        innerResourceInstanceMethod.url = url
        innerResourceInstanceMethod.requestHeaderClass = requestHeaderClass
        innerResourceInstanceMethod.requestParamClass = requestParamClass
        innerResourceInstanceMethod.requestClass = requestClass
        innerResourceInstanceMethod.responseClass = responseClass
        innerResourceInstanceMethod.responseHeaders = responseHeaders
        innerResourceInstanceMethod.apiKeyRequired = apiKeyRequired
        innerResourceInstanceMethod.produces = produces
        innerResourceInstanceMethod.consumes = consumes
        innerResourceInstanceMethod.logRequest = logRequest
        innerResourceInstanceMethod.logResponse = logResponse
        innerResourceInstanceMethod.enabled = enabled
        innerResourceInstanceMethod.muteLogs = muteLogs
        innerResourceInstanceMethod.muteStacktraceOnBusinessRuleException = resourceInstanceMethodMuteStacktraceOnBusinessRuleException
        return innerResourceInstanceMethod
    return innerMethodWrapper




def resolveListenerCall(
    args,
    kwargs,
    wrapperManager,
    requestHeaderClass,
    requestParamClass,
    requestClass,
    requestBody,
    responseClass,
    defaultResponseHeaders,
    consumes,
    produces,
    resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
    verb = HttpDomain.Verb.POST,
    logRequestMessage = LogConstant.LISTENER_REQUEST,
    context = HttpDomain.LISTENER_CONTEXT

) :
    completeResponse = None
    try:
        completeResponse = FlaskManager.handleControllerMethod(
            args,
            kwargs,
            consumes,
            wrapperManager.resourceInstance,
            wrapperManager.resourceInstanceMethod,
            requestHeaderClass,
            requestParamClass,
            requestClass,
            wrapperManager.shouldLogRequest(),
            resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
            requestBody = requestBody,
            verb = verb,
            logRequestMessage = logRequestMessage
        )
        FlaskManager.validateCompleteResponse(responseClass, completeResponse)
    except Exception as exception:
        log.log(resolveListenerCall, 'Failure at controller method execution. Getting complete response as exception', exception=exception, muteStackTrace=True)
        completeResponse = FlaskManager.getCompleteResponseByException(
            exception,
            wrapperManager.resourceInstance,
            wrapperManager.resourceInstanceMethod,
            resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
            context = context
        )
    try:
        status = HttpStatus.map(completeResponse[-1])
        additionalResponseHeaders = completeResponse[1]
        if ObjectHelper.isNotNone(wrapperManager.resourceInstance.responseHeaders):
            additionalResponseHeaders = {**wrapperManager.resourceInstance.responseHeaders, **additionalResponseHeaders}
        if ObjectHelper.isNotNone(defaultResponseHeaders):
            additionalResponseHeaders = {**defaultResponseHeaders, **additionalResponseHeaders}
        responseBody = completeResponse[0] if ObjectHelper.isNotNone(completeResponse[0]) else {'message' : status.enumName}
        httpResponse = FlaskUtil.buildHttpResponse(additionalResponseHeaders, responseBody, status.enumValue, produces)
    except Exception as exception:
        log.failure(resolveListenerCall, f'Failure while parsing complete response: {completeResponse}. Returning simplified version of it', exception, muteStackTrace=True)
        completeResponse = getCompleteResponseByException(
            Exception(f'Not possible to handle complete response. Cause: {str(exception)}'),
            wrapperManager.resourceInstance,
            wrapperManager.resourceInstanceMethod,
            resourceInstanceMethodMuteStacktraceOnBusinessRuleException
        )
        httpResponse = FlaskUtil.buildHttpResponse(completeResponse[1], completeResponse[0], completeResponse[-1].enumValue, produces)
    return httpResponse

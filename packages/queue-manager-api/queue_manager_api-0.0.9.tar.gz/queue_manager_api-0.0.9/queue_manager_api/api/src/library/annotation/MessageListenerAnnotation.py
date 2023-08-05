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
    from queue_manager_api.api.src.library.dto import MessageDto
except:
    import AnnotationUtil, MessageDto


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
        @wrapperManager.api.app.route(f'{wrapperManager.api.baseUrl}{resourceInstanceMethodUrl}', methods=['POST'])
        def innerResourceInstanceMethod(*args, **kwargs):
            args = wrapperManager.addResourceInFrontOfArgs(args)
            messageAsJson = FlaskUtil.safellyGetRequestBody()
            if ObjectHelper.isEmpty(messageAsJson):
                completeResponse = FlaskManager.getCompleteResponseByException(
                    GlobalException(message='Content cannot be empty', logResponse=f'Content: {messageContent}', status=HttpStatus.BAD_REQUEST),
                    wrapperManager.resourceInstance,
                    wrapperManager.resourceInstanceMethod,
                    resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
                    context = HttpDomain.LISTENER_CONTEXT
                )
                httpResponse = FlaskUtil.buildHttpResponse(completeResponse[1], completeResponse[0], completeResponse[-1].enumValue, produces)
            else:
                completeResponse = None
                if not wrapperManager.muteLogs:
                    log.info(wrapperManager.resourceInstanceMethod, f'''{LogConstant.LISTENER_SPACE}{FlaskUtil.safellyGetVerb()}{c.SPACE_DASH_SPACE}{FlaskUtil.safellyGetUrl()}''')

                if wrapperManager.enabled:
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
                            logRequest,
                            resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
                            requestBody = messageAsJson.get('content'),
                            verb = HttpDomain.Verb.POST,
                            logRequestMessage = LogConstant.LISTENER_REQUEST
                        )
                        FlaskManager.validateCompleteResponse(responseClass, completeResponse)
                    except Exception as exception:
                        completeResponse = FlaskManager.getCompleteResponseByException(
                            exception,
                            wrapperManager.resourceInstance,
                            wrapperManager.resourceInstanceMethod,
                            resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
                            context = HttpDomain.LISTENER_CONTEXT
                        )
                else:
                    completeResponse = FlaskManager.getCompleteResponseByException(
                        GlobalException(logMessage='This resource is temporarily disabled', status=HttpStatus.SERVICE_UNAVAILABLE),
                        wrapperManager.resourceInstance,
                        wrapperManager.resourceInstanceMethod,
                        resourceInstanceMethodMuteStacktraceOnBusinessRuleException,
                        context = HttpDomain.LISTENER_CONTEXT
                    )

                try:
                    status = HttpStatus.map(completeResponse[-1])
                    additionalResponseHeaders = completeResponse[1]
                    if ObjectHelper.isNotNone(wrapperManager.resourceInstance.responseHeaders):
                        additionalResponseHeaders = {**wrapperManager.resourceInstance.responseHeaders, **additionalResponseHeaders}
                    if ObjectHelper.isNotNone(responseHeaders):
                        additionalResponseHeaders = {**responseHeaders, **additionalResponseHeaders}
                    responseBody = completeResponse[0] if ObjectHelper.isNotNone(completeResponse[0]) else {'message' : status.enumName}
                    httpResponse = FlaskUtil.buildHttpResponse(additionalResponseHeaders, responseBody, status.enumValue, produces)
                except Exception as exception:
                    log.failure(innerResourceInstanceMethod, f'Failure while parsing complete response: {completeResponse}. Returning simplified version of it', exception, muteStackTrace=True)
                    completeResponse = getCompleteResponseByException(
                        Exception('Not possible to handle complete response'),
                        wrapperManager.resourceInstance,
                        wrapperManager.resourceInstanceMethod,
                        resourceInstanceMethodMuteStacktraceOnBusinessRuleException
                    )
                    httpResponse = FlaskUtil.buildHttpResponse(completeResponse[1], completeResponse[0], completeResponse[-1].enumValue, produces)

            try:
                if wrapperManager.shouldLogResponse():
                    log.prettyJson(
                        wrapperManager.resourceInstanceMethod,
                        LogConstant.LISTENER_RESPONSE,
                        {
                            'headers': FlaskUtil.safellyGetResponseHeaders(httpResponse),
                            'body': FlaskUtil.safellyGetFlaskResponseJson(httpResponse),
                            'status': status
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

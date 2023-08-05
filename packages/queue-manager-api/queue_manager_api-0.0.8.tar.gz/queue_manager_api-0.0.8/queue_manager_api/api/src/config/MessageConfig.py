from python_helper import log
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


EMITTER_URL = globalsInstance.getSetting('queue.message.emitter.url')
EMITTER_TIMEOUT = globalsInstance.getSetting('queue.message.emitter.timeout')

LISTENER_URL = globalsInstance.getSetting('queue.message.listener.url')
LISTENER_TIMEOUT = globalsInstance.getSetting('queue.message.listener.timeout')

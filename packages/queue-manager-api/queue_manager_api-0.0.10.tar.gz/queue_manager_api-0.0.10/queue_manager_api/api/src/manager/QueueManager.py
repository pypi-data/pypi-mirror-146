

class QueueManager:

    def addResource(self, api, app):
        api.queueManager = self
        self.api = api


    def onHttpRequestCompletion(self, api, app):
        ...


    def onRun(self, api, app):
        ...


    def initialize(self, api, app):
        ...


    def onShutdown(self, api, app):
        ...

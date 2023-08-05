from python_helper import log
from threading import Thread
import time


DEFAULT_TIMEOUT = 1


class ApplicationThread:

    shouldStop = False

    def __init__(self, target, *args, timeout=DEFAULT_TIMEOUT, **kwargs):
        self.thread = Thread(
            target = target,
            args = args,
            kwargs = kwargs
        )
        self.timeout = timeout


    def run(self):
        self.thread.join(timeout=timeout)
        self.thread.start()


    def isAlive(self):
        return self.thread.is_alive()


def killDeadThreads(threadManager, threadDictionary):
    while 0 < len(threadDictionary):
        time.sleep(5)
        finishedThreads = [k for k, t in threadDictionary.items() if not t.isAlive()]
        for k in finishedThreads:
            threadDictionary.pop(k)
            log.debug(killDeadThreads, f'The {k}th tread is finished')
    threadManager.killingDeadThreads = False


class ThreadManager:

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.threadDictionary = {}
        self.killingDeadThreads = False
        self.timeout = timeout


    def new(self, target, *args, **kwargs):
        return ApplicationThread(target, *args, timeout=self.timeout, **kwargs)



    def runInAThread(self, target, *args, **kwargs):
        thread = self.new(target, *args, **kwargs)
        self.threadDictionary[len(self.threadDictionary)] = thread
        thread.run()
        self.killDeadThreads()


    def killDeadThreads(self):
        if not self.killingDeadThreads:
            self.killingDeadThreads = True
            self.runInAThread(killDeadThreads, self, self.threadDictionary)

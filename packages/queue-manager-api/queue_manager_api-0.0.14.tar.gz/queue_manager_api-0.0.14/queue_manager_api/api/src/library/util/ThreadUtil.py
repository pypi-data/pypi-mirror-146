from python_helper import log, ObjectHelper
from python_framework import ConverterStatic
from threading import Thread
import time


DEFAULT_TIMEOUT = 20


def killDeadThreads(threadManager, threadDictionary):
    while 0 < len(threadDictionary):
        time.sleep(5)
        finishedThreads = [k for k, t in threadDictionary.items() if not t.isAlive()]
        for k in finishedThreads:
            threadDictionary.pop(k)
            log.debug(killDeadThreads, f'The {k}th tread is finished')
    threadManager.killingDeadThreads = False


def runInSimpleThread(target, *args, threadTimeout=DEFAULT_TIMEOUT, **kwargs):
    applicationThread = ApplicationThread(target, *args, threadTimeout=DEFAULT_TIMEOUT, **kwargs)
    applicationThread.run()


class ApplicationThread:

    shouldStop = False

    def __init__(self, target, *args, threadTimeout=DEFAULT_TIMEOUT, **kwargs):
        self.thread = Thread(
            target = target,
            args = args,
            kwargs = kwargs
        )
        self.timeout = ConverterStatic.getValueOrDefault(threadTimeout, DEFAULT_TIMEOUT)


    def run(self, threadTimeout=DEFAULT_TIMEOUT):
        self.thread.start()
        # self.thread.join(timeout=threadTimeout if ObjectHelper.isNone(self.timeout) else self.timeout)


    def isAlive(self):
        return self.thread.is_alive()


class ThreadManager:

    def __init__(self, threadTimeout=DEFAULT_TIMEOUT):
        self.threadDictionary = {}
        self.killingDeadThreads = False
        self.timeout = threadTimeout


    def new(self, target, *args, **kwargs):
        return ApplicationThread(target, *args, **kwargs)


    def runInAThread(self, target, *args, **kwargs):
        thread = self.new(target, *args, threadTimeout=self.timeout, **kwargs)
        self.threadDictionary[len(self.threadDictionary)] = thread
        thread.run()
        self.killDeadThreads()


    def killDeadThreads(self):
        if not self.killingDeadThreads:
            self.killingDeadThreads = True
            self.runInAThread(killDeadThreads, self, self.threadDictionary)

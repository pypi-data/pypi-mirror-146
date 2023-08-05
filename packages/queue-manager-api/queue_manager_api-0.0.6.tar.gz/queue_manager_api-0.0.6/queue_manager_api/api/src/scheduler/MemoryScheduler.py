from python_framework import SchedulerType
from python_framework import Scheduler, SchedulerMethod, WeekDay, WeekDayConstant


@Scheduler(muteLogs=True)
class MemoryScheduler:

    @SchedulerMethod(SchedulerType.INTERVAL, seconds=15, instancesUpTo=2)
    def removeAllProcessedMessages(self) :
        self.service.memory.removeAllProcessedMessages()

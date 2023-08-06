import time
from threading import Thread
from efr.utils.Task import *


class BUILTTASK(Task): ...


class STOPTASK(BUILTTASK):
    def __init__(self, worker):
        super(STOPTASK, self).__init__(lambda :worker.stop())


class Worker(Thread):
    """
    提供一个循环执行器线程
    3 method to stop it:
        1.call: worker.stop()
        2.add stop task: worker.addTask(STOPTASK)  # After it start. It will stop on the end of all other tasks
        3.instance with always=False: Worker(always=False)  # After it start. It will stop when the tasks is empty.
    """

    def __init__(self, name=None, daemon=True, mindt=0.5, always=True):
        super(Worker, self).__init__(name=name, daemon=daemon)
        self.alive  = True
        self.mindt  = mindt
        self.tasks  = []
        self.always = always

    def run(self) -> None:
        while self.alive:
            next_point = time.time() + self.mindt

            tasks = []
            for task in self.tasks:
                task()
                if task.left > 0:
                    tasks += [task]
                if not self.alive:
                    break
            self.tasks = tasks

            if not (self.always or self.tasks):  # auto stop
                self.alive = False
                break

            delta = next_point - time.time()
            if delta > 0:
                time.sleep(delta)

    def addTask(self, task: Task = STOPTASK) -> bool:
        task = STOPTASK(self) if task is STOPTASK else task
        self.tasks += [task]
        return True

    def removeTask(self, task: Task) -> bool:
        """
        移除任务
        remove task
        :param task: Task
        :return:
        """
        try:
            if task is STOPTASK:
                for _task in self.tasks:
                    if isinstance(_task, STOPTASK):
                        self.tasks.remove(_task)
                        return True
                return False
            else:
                self.tasks.remove(task)
        except:
            ...
        return True

    def stop(self):
        """
        停止线程，但是至少需要等待到进行中的任务结束
        Stop the thread, but at least wait until the end of the task in progress
        :return:
        """
        self.alive = False

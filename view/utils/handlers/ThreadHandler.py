import threading
from typing import List


class ThreadHandler:
    def __init__(self):
        self.threads: List[StoppableThread] = []

    def start_task(self, task):
        background_thread = StoppableThread(target=task)
        background_thread.daemon = True
        self.threads.append(background_thread)
        background_thread.start()

    def stop_specific_task(self, task_name):
        for thread in self.threads:
            if thread.name == task_name:
                thread.stop()

    def stop_all_tasks(self):
        for thread in self.threads:
            thread.stop()


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

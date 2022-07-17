import time
import uuid
from multiprocessing import Process, Queue


# class ThreadWithReturn(multiprocessing.Process):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._return = None
#
#     def run(self):
#         if self._target is not None:
#             self._return = self._target(*self._args, **self._kwargs)
#
#     def join(self, *args, **kwargs):
#         super().join(*args, **kwargs)
#         return self._return
from threading import Thread

def execute(task, results) -> None:
    results.put([task.id, _OPERATIONS[task.command](task.sequence)])

class Front:

    def __init__(self, messages, result) -> None:
        super().__init__()
        self._worker = None
        self._messages = messages
        self.storage = {}
        self._results = result

    def get_result(self, id_):
        if id_ in self.storage:
            return self.storage.pop(id_)

        id_, result = self.results.get()
        if id_ == id_:
            return result

        self.storage[id_] = result

        return self.get_result(id_)

    def call_command(self, command_name, params):
        id_ = uuid.uuid4()
        self._messages.put((id_, command_name, params))

        return id_

    def start(self):
        self._worker = Process(
            target=self._run, args=(self._messages, self._results))
        self._worker.start()

    def stop(self):
        self._worker.terminate()
        self._worker.join()

    @staticmethod
    def _run(messages, tasks):
        while True:
            message = messages.get()
            if message:
                tasks.put(message)

            time.sleep(1.0)


class Back:
    commands = {
        'min': min,
        'max': max,
        'sum': sum
    }

    def __init__(self, messages, results):
        super().__init__()
        self._worker = None
        self._messages = messages
        self._results = results

    def start(self):
        self._worker = Process(
            target=self._run, args=(self._messages, self._results))
        self._worker.start()

    def stop(self):
        self._worker.terminate()
        self._worker.join()

    @staticmethod
    def _run(tasks: Queue, results: Queue):
        while True:
            task = tasks.get()
            thread = Thread(target=, args=(task, results))
            thread.start()
            thread.join()

    def execute(self, elements):
        result = None
        if self._command is not None:
            result = self._command(elements)
        return result


class Composer:

    def __init__(self) -> None:
        super().__init__()
        self._messages = Queue()
        self._results = Queue()
        self._front = Front(self._messages, self._results)
        self._back = Back(self._messages, self._results)

    def start(self):
        self._back.start()
        self._front.start()

    def stop(self):
        self._front.stop()
        self._back.stop()

    def get_front(self):
        return self._front


if __name__ == '__main__':
    # multiprocessing.Process = process = CustomProcess

    composer = Composer()
    composer.start()
    front = composer.get_front()

    command_max = front.call_command('max', [1, 2, 3])
    command_min = front.call_command('min', [1, 2, 3])

    result_min = front.get_result(command_min)
    result_max = front.get_result(command_max)

    # pcount = process._init_count
    # self.assertGreaterEqual(self.Thread._init_count, 2)

    composer.stop()

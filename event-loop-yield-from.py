import heapq
import logging
from typing import Set, Callable, Any
from time import monotonic
from queue import SimpleQueue
from functools import partial


class Future:
    def __init__(self):
        self.result = None
        self.done = False
        self.done_callbacks: Set[Callable[["Future"], Any]] = set()
        self.exception = None

    def _handle_callbacks(self):
        for cb in self.done_callbacks:
            try:
                cb(self)
            except Exception:
                logging.exception("Unhandled exception in %r", cb)

    def set_result(self, result):
        self.done = True
        self.result = result
        self._handle_callbacks()

    def set_exception(self, exception):
        self.done = True
        self.exception = exception
        self._handle_callbacks()

    def get_result(self):
        if self.exception:
            raise self.exception
        return self.result
        
    def __iter__(self):
        while not self.done:
            yield None
        return self.get_result()


class CallbackHandler:
    def __init__(self):
        self.heap = []

    def call_later(self, delay, func, *args) -> Future:
        future = Future()
        heapq.heappush(
            self.heap,
            (
                delay + monotonic(),    # absolute time
                future,                 # result future
                partial(func, *args)    # callable
            )
        )
        return future

    def step(self) -> None:
        while self.heap:
            if self.heap[0][0] > monotonic():
                return
            soon, future, func = heapq.heappop(self.heap)
            try:
                future.set_result(func())
            except Exception as e:
                future.set_exception(e)


class EventLoop:
    def __init__(self):
        self.events = SimpleQueue()
        self.callbacks = CallbackHandler()

    def call_later(self, delay, callback, *args) -> Future:
        return self.callbacks.call_later(delay, callback, *args)

    def step(self, coro):
        try:
            next(coro)
        except StopIteration as e:
            return e.value
        self.events.put(coro)

    def run(self):
        while not self.events.empty():
            self.callbacks.step()
            self.step(self.events.get())

    def create_task(self, coro):
        future = Future()

        def wrapper():
            try:
                result = yield from coro
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)

        gen = wrapper()
        self.events.put(gen)
        return future

    def run_until_complete(self, coro):
        future = self.create_task(coro)
        self.run()
        return future.get_result()


loop = EventLoop()


def sleep(seconds) -> Future:
    return loop.call_later(seconds, lambda: True)


def test():
    yield from sleep(2)
    print(monotonic(), "test done")


print(monotonic(), "start")
loop.create_task(test())
loop.create_task(test())
loop.run_until_complete(test())
print(monotonic(), "finished")

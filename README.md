EventLoop в 100 строк
=====================

В файле `event-loop-yield-from.py` реализован простой event-loop.
Необходимо добавить в его поддержку `async def` и `await` выражений.

После доработок нижеприведенный код должен работать.

```python

def sleep(seconds) -> Future:
    return loop.call_later(seconds, lambda: True)


async def test():
    await sleep(2)
    print(monotonic(), "test done")


print(monotonic(), "start")
loop.create_task(test())
loop.create_task(test())
loop.run_until_complete(test())
print(monotonic(), "finished")
```

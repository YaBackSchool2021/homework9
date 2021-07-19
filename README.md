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


Порядок сдачи
-------------

1. Сделать fork репозитория. Например, пользователь `v-pupkin` делает fork 
   `v-pupkin/homework9` 
2. В своем форке сделать ветку, например `feature/async-await-support`
3. В ветку внести все, необходимые изменения, и закомитить одним или 
   несколькими комитами
4. Создать pull request в репозитории-forkе на ветку master. Например: 
   `v-pupkin/homework9:feature/async-await-support` > 
   `v-pupkin/homework9:master`
5. Проверяться будет именно pull request, поэтому сдавать необходимо ссылку 
   на него
6. Ссылку на pull request необходимо приложить в соответствующий тикет в 
   очереди в Трекере (https://tracker.yandex.ru/SHBRHOMEWORK).


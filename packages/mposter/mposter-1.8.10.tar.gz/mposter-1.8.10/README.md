# MPoster

## Queues

Работа с очередями:

```
from mposter import queues

def queues_method(data):
    print(data)

_queues = queues.Queues(threads=10, target=queues_method)
for i in range(10):
    _queues.put(i)
_queues.join()
```


## Http

### Fuck_proxies

Пул для плохих проксей:

```
from mposter import http

fuck_proxies = http.Fuck_proxies()
...
for proxy in proxies:
    if fuck_proxies.check_proxy(_proxies.get('http')):  # Прокси есть в пуле, она плохая, идём за новой
        continue
...
if r.status_code == 403:  # Прокси забанена, добавляем в пул
    fuck_proxies.add(_proxy_port)
```
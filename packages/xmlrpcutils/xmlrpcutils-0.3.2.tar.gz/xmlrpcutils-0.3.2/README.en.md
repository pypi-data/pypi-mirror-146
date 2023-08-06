# xmlrpcutils

xmlrpc server simplify.

## Install

```
pip install xmlrpcutils
```

## TestServer

```
from xmlrpcutils.server import SimpleXmlRpcServer
from xmlrpcutils.service import ServiceBase

class SayHelloService(ServiceBase):

    def hello(self, name):
        return f"Hello {name}, how are you!"

class TestServer(SimpleXmlRpcServer):
    
    def register_services(self):
        super().register_services()
        SayHelloService(namespace="debug").register_to(self.server)

app =  TestServer()
app_ctrl = app.get_controller()

if __name__ == "__main__":
    app_ctrl()

```
## Start test server

```
python test_server.py start
```

## Remote call with TestServer

```
In [9]: from xmlrpc.client import ServerProxy

In [10]: server = ServerProxy('http://127.0.0.1:8381')

In [11]: server.system.listMethods()
Out[11]:
['debug.counter',
 'debug.echo',
 'debug.false',
 'debug.hello',
 'debug.hostname',
 'debug.null',
 'debug.ping',
 'debug.sleep',
 'debug.sum',
 'debug.timestamp',
 'debug.true',
 'debug.uname',
 'debug.urandom',
 'debug.uuid4',
 'system.listMethods',
 'system.methodHelp',
 'system.methodSignature',
 'system.multicall']

In [12]: server.debug.hello('zencore')
Out[12]: 'Hello zencore, how are you!'
```


## Use apikey auth mechanism.

*Add `apikeys` in the server's config file*

```
apikeys:
  HyuTMsNzcSZYmwlVDdacERde9azdTKT8:
    appid: test01
    other-app-info: xxx
  SEEpVkus5b86aHxS6UMSCFLxkIhYMMZF:
    appid: test02
    other-app-info: xxx
```

*Add `apikey` header at the client side*

```
In [93]: from xmlrpc.client import ServerProxy
    ...: service = ServerProxy("http://127.0.0.1:8911", headers=[("apikey", "HyuTMsNzcSZYmwlVDdacERde9azdTKT8")])
    ...: result = service.debug.ping()
    ...: print(result)
pong
```

## Releases

### v0.1.1

- First release.

### v0.1.2

- Fix license_files missing problem.

### v0.1.3

- Fix DebugService init method problem, add super().__init__() calling.

### v0.2.0

- Don't force to use gevent.
- Allow non-namespace services.

### v0.3.1

- Remove all gevent things.
- Add apikey auth mechanism. Use headers parameter to provide apikey at then client side.

### v0.3.2

- Fix get_ignore_methods name.

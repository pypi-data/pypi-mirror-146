# xmlrpcutils

xmlrpc服务器简化工具。

## 安装

```
pip install xmlrpcutils
```

## TestServer测试服务器

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

## 启动测试服务器

```
python test_server.py
```

## 远程调用xmlrpc测试服务器

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

## 使用apikey认证

*服务器端在配置文件中增加apikeys配置*

```
apikeys:
  HyuTMsNzcSZYmwlVDdacERde9azdTKT8:
    appid: test01
    other-app-info: xxx
  SEEpVkus5b86aHxS6UMSCFLxkIhYMMZF:
    appid: test02
    other-app-info: xxx
```

*客户端在初始化ServerProxy中指定*

```
In [93]: from xmlrpc.client import ServerProxy
    ...: service = ServerProxy("http://127.0.0.1:8911", headers=[("apikey", "HyuTMsNzcSZYmwlVDdacERde9azdTKT8")])
    ...: result = service.debug.ping()
    ...: print(result)
pong
```

## 版本

### v0.1.1

- 初始版本。

### v0.1.2

- 修正安装包打包时缺少license_files的问题。

### v0.1.3

- 修正DebugService的__init__方法，补充super().__init__()的调用。

### v0.2.0

- 不强制使用gevent。
- 允许注册无命名空间函数。

### v0.3.1

- 清理gevent遗留。
- 增加apikey认证机制。客户端通过headers指定apikey。

### v0.3.2

- 修正get_ignore_methods函数命名。

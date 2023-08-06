

import json
import logging
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from fastutils import logutils
from daemon_application import DaemonApplication

logger = logging.getLogger(__name__)

XMLRPC_403_XML = b"""<?xml version="1.0" encoding="UTF-8" ?>
<methodResponse>
    <fault>
        <value>
            <struct>
                <member>
                    <name>faultCode</name>
                    <value><int>403</int></value>
                </member>
                <member>
                    <name>faultString</name>
                    <value><string>403 Forbidden</string></value>
                </member>
            </struct>
        </value>
    </fault>
</methodResponse>
"""

class SimpleApikeyAuthXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    
    def do_POST(self):
        if self.server.enable_apikeys_auth:
            self._apikey = self.headers.get(self.server.apikey_auth_header_name, None)
            if self._apikey:
                self._appinfo = self.server.apikeys.get(self._apikey, None)
            else:
                self._appinfo = None
            if self._apikey and self._appinfo:
                return super().do_POST()
            else:
                # apikey verify failed, return error message
                logger.error("Apikey auth verify failed, headers={}".format(json.dumps(dict(self.headers))))
                self.send_response(403)
                self.send_header("Content-Type", "text/xml")
                self.send_header("Content-Length", len(XMLRPC_403_XML))
                self.end_headers()
                self.wfile.write(XMLRPC_403_XML)
        else:
            return super().do_POST() 

class SimpleThreadedXmlRpcServer(ThreadingMixIn, SimpleXMLRPCServer):
    
    def __init__(self, *args, **kwargs):
        self.enable_apikeys_auth = False
        self.apikeys = {}
        self.apikey_auth_header_name = "apikey"
        super().__init__(*args, **kwargs)
        self.register_introspection_functions()
        self.register_multicall_functions()

    def set_apikey(self, apikey, appinfo=None):
        self.enable_apikeys_auth = True
        appinfo = appinfo or apikey
        self.apikeys[apikey] = appinfo
    
    def set_apikeys(self, apikeys):
        self.enable_apikeys_auth = True
        apikeys = apikeys or {}
        if isinstance(apikeys, dict):
            for apikey, appinfo in apikeys.items():
                self.set_apikey(apikey, appinfo)
        elif isinstance(apikeys, (tuple, set, list)):
            for apikey in apikeys:
                self.set_apikey(apikey)

class SimpleXmlRpcServer(DaemonApplication):

    def get_default_listen_port(self):
        return getattr(self, "default_listen_port", 8381)
    
    def get_disable_debug_service_flag(self):
        return getattr(self, "disable_debug_service", False)

    def main(self):
        logutils.setup(**self.config)
        self.server_listen = tuple(self.config.get("server", {}).get("listen", ("0.0.0.0", self.get_default_listen_port())))
        logger.warn("Starting xmlrpc server on {server_listen}...".format(server_listen=self.server_listen))
        apikeys = self.config.get("apikeys", None)
        self.server = SimpleThreadedXmlRpcServer(
            self.server_listen,
            requestHandler=SimpleApikeyAuthXMLRPCRequestHandler,
            allow_none=True,
            encoding="utf-8",
            )
        if apikeys:
            self.server.set_apikeys(apikeys)
        self.register_services()
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.warn("Got KeyboardInterrupt signal, stopping the service...")

    def register_services(self):
        disable_debug_service_flag = self.get_disable_debug_service_flag()
        if not disable_debug_service_flag:
            from .service import DebugService
            DebugService().register_to(self.server)

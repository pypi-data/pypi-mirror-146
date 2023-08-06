import sys
import socket
import requests


def init_http_session(headers, *, keepalive = False):
    http_session = requests.Session()
    http_session.headers.update(headers)

    socket_options = []
    if keepalive:
        socket_options = get_keepalive_socket_options()

    adapter = HTTPAdapterWithSocketOptions(socket_options=socket_options)
    http_session.mount("http://", adapter)
    http_session.mount("https://", adapter)

    return http_session


#


class HTTPAdapterWithSocketOptions(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapterWithSocketOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapterWithSocketOptions, self).init_poolmanager(*args, **kwargs)


def get_keepalive_socket_options():
    options = []
    platform = sys.platform
    has_tcp_attributes = (
        hasattr(socket, "TCP_KEEPIDLE")
        and hasattr(socket, "TCP_KEEPINTVL")
        and hasattr(socket, "TCP_KEEPCNT")
    )

    if platform == "linux" and has_tcp_attributes:
        options.append((socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1))
        options.append((socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10))
        options.append((socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10))
        options.append((socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 10))

    return options

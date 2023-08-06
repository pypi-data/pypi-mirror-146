import socket
from typing import Final

from datalink_levl.helpful import send


class TcpClient:
    EXIT: Final[str] = "!exit"

    def __init__(self, type_net: int):
        """
        type_net: Транспортный уровень
            - socket.AF_UNIX = uds
            - socket.AF_INET = ipv4
            - socket.AF_INET6 = ipv6
        """
        # Настройка socket
        self.client_socket = socket.socket(family=type_net, type=socket.SOCK_STREAM)

    def disconnect(self):
        send(self.EXIT.encode("utf-8"), self.client_socket)  # Уведомить сервер об отключении
        self.client_socket.close()


class UdpClient:
    def __init__(self, type_net: int):
        """
        type_net: Транспортный уровень
            - socket.AF_UNIX = uds
            - socket.AF_INET = ipv4
            - socket.AF_INET6 = ipv6
        """
        # Настройка socket
        self.client_socket = socket.socket(family=type_net, type=socket.SOCK_DGRAM)

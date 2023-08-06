import os
import socket
from typing import Final


class _UdsServer:
    """
    Порядок наследования:
        - (_UdsServer, TcpServer)
        - (_UdsServer, UdpServer)

    ---\n
    class UdsTcpServer(_UdsServer, TcpServer):
        def __init__(self, socket_file_name: str):
            super().__init__(socket_file_name)
    """

    def __init__(self, socket_file_name: str):
        # Запоминаем unix файл
        self.SOCKET_FILE: Final[str] = socket_file_name
        # Инициализируем транспортный уровень
        super().__init__(socket.AF_UNIX, self.SOCKET_FILE)

    def __del__(self):
        """
        По окончанию удаляем unix файл
        """
        os.remove(self.SOCKET_FILE)


class _Ip4Server:
    """
    Порядок наследования:
        - (_Ip4Server, TcpServer)
        - (_Ip4Server, UdpServer)

    ---\n
    class Ip4TcpServer(_Ip4Server, TcpServer):
        def __init__(self, ip: str, port:int):
            super().__init__(ip, port)
    """

    def __init__(self, ip: str, port: int):
        # Запоминаем Ip и Port
        self.Ip, self.Port = ip, port
        # Инициализируем транспортный уровень
        super().__init__(socket.AF_INET, (self.Ip, self.Port))

import socket
from typing import Final, Optional


class _UdsClient:
    """
    Порядок наследования:
        - (_UdsClient, TcpClient)
        - (_UdsClient, UdpClient)

    ---\n
    class UdsTcpClient(_UdsClient, TcpClient):
        def __init__(self, socket_file_name: str):
            super().__init__(socket_file_name)
    """

    def __init__(self, socket_file_name: str):
        # Запоминаем unix файл
        self.SOCKET_FILE: Final[str] = socket_file_name
        # Инициализируем транспортный уровень
        self.client_socket: Optional[socket.socket] = None
        super().__init__(socket.AF_UNIX)

    def connect(self):
        self.client_socket.connect(self.SOCKET_FILE)


class _Ip4Client:
    """
    Порядок наследования:
        - (_Ip4Client, TcpClient)
        - (_Ip4Client, UdpClient)

    ---\n
    class Ip4TcpClient(_Ip4Client, TcpClient):
        def __init__(self, ip: str, port:int):
            super().__init__(ip, port)
    """

    def __init__(self, ip: str, port: int):
        # Запоминаем Ip и Port
        self.Ip, self.Port = ip, port
        # Инициализируем транспортный уровень
        self.client_socket: Optional[socket.socket] = None
        super().__init__(socket.AF_INET)

    def connect(self):
        self.client_socket.connect((self.Ip, self.Port))
import socket
from typing import Final, Union

from datalink_levl.helpful import recv, send


class TcpServer:
    EXIT: Final[str] = "!exit"

    def __init__(self,
                 type_net: int,
                 connectTo: Union[tuple[str, int], str],
                 count_listen: int = 1
                 ):
        """
        type_net: Транспортный уровень
            - socket.AF_UNIX    = uds
            - socket.AF_INET    = ipv4
            - socket.AF_INET6   = ipv6

        connectTo: Канальный уровень
            - (Ip:str,Port:int)     = ip
            - UnixFile              = uds

        count_listen: Сколько ожидаем подключений
        """
        # Настройка socket
        self.server_socket = socket.socket(family=type_net, type=socket.SOCK_STREAM)
        # Резервируем канал для прослушивания
        self.server_socket.bind(connectTo)
        # Сколько ожидаем подключений
        self.server_socket.listen(count_listen)

    def accept(self) -> tuple[socket.socket, Union[str, tuple[str, int]]]:
        user, client_address = self.server_socket.accept()
        print(f"=== connect: {client_address}")
        return user, client_address

    @staticmethod
    def disconnect(user, client_address):
        """
        Отключиться от клиента
        """
        print(f"===\tdisconnect: {client_address}")
        user.close()

    @staticmethod
    def is_connect(data: str) -> bool:
        """
        Если клиент не создал условия для отключения
        """
        return False if data == TcpServer.EXIT else True

    def _main_loop(self):
        user, client_address = self.accept()  # Ждем подключения
        Live = True
        while Live:
            try:
                if user.fileno() > -1:  # Если есть подключение

                    # GET
                    stream: bytes = recv(user)
                    stream_str: str = stream.decode("utf-8")
                    print(stream_str)

                    if self.is_connect(stream_str):
                        # SEND
                        send("[+]".encode('utf-8'), user)
                    else:
                        # Если клиент хочет разорвать соединение, то отключаемся от него
                        self.disconnect(user, client_address)

                else:  # Если нет подключения, то ждать новое подключение
                    user, address = self.accept()  # Ждем подключения

            except KeyboardInterrupt as e:
                print(f"[close] {e}")
                Live = False
                break

            except BrokenPipeError:
                self.disconnect(user, client_address)


class UdpServer:
    def __init__(self,
                 type_net: int,
                 connectTo: Union[tuple[str, int], str],
                 ):
        """
        type_net: Транспортный уровень
            - socket.AF_UNIX = uds
            - socket.AF_INET = ipv4
            - socket.AF_INET6 = ipv6

        connectTo: Канальный уровень
            - (Ip:str,Port:int)     = ip
            - UnixFile              = uds
        """
        # Настройка socket
        self.server_socket = socket.socket(family=type_net, type=socket.SOCK_DGRAM)
        # Резервируем канал для прослушивания
        self.server_socket.bind(connectTo)

import socket

from datalink_levl.client_datalink import _UdsClient, _Ip4Client
from datalink_levl.helpful import send, recv, recvfrom
from transport_levl.client_transport import UdpClient, TcpClient


class UdsUdpClient(_UdsClient, UdpClient):
    def __init__(self, socket_file_name: str):
        super().__init__(socket_file_name)

    def main_loop(self):
        print(f"Run Client Uds UDP: {self.SOCKET_FILE}")

        self.connect()  # Подключаем к серверу

        Live = True
        while Live:
            try:
                # INPUT
                x = input("::: ")
                if x == "exit":
                    # STOP
                    raise socket.error

                # SEND
                self.client_socket.send(x.encode('utf-8'))

                # GET в udp uds не получиться поучать данные от сервера, так как у нас одинаковые адреса с сервером
                # stream, client_acres = self.client_socket.recvfrom(self.SIZE_CONTENT)

            except (KeyboardInterrupt, socket.error) as e:
                print(f"[close] {e}")
                Live = False
                break


class Ip4UdpClient(_Ip4Client, UdpClient):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def main_loop(self):
        print(f"Run Client Ip4 UDP:\t{self.Ip}:{self.Port}")

        self.connect()  # Подключаем к серверу

        Live = True
        while Live:
            try:
                # INPUT
                x = input("::: ")
                if x == "exit":
                    # STOP
                    raise socket.error

                # SEND
                send(x.encode('utf-8'), self.client_socket)

                # GET
                stream, client_acres = recvfrom(self.client_socket)
                print(stream.decode("utf-8"))

            except (KeyboardInterrupt, socket.error) as e:
                print(f"[close] {e}")
                Live = False
                break


class UdsTcpClient(_UdsClient, TcpClient):
    def __init__(self, socket_file_name: str):
        super().__init__(socket_file_name)

    def main_loop(self):
        print(f"Run Client Uds TCP: {self.SOCKET_FILE}")

        self.connect()  # Подключаем к серверу

        Live = True
        while Live:
            try:
                # INPUT
                x = input("::: ")
                if x == "exit":
                    # STOP
                    self.disconnect()
                    raise socket.error

                # SEND
                send(x.encode('utf-8'), self.client_socket)

                # GET
                stream: bytes = recv(self.client_socket)
                stream_str: str = stream.decode("utf-8")
                print(stream_str)

            except (KeyboardInterrupt, socket.error) as e:
                print(f"[close] {e}")
                Live = False
                break


class Ip4TcpClient(_Ip4Client, TcpClient):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def main_loop(self):
        print(f"Run Client Ip4 TCP:\t{self.Ip}:{self.Port}")

        self.connect()  # Подключаем к серверу

        Live = True
        while Live:
            try:
                # INPUT
                x = input("::: ")
                if x == "exit":
                    # STOP
                    self.disconnect()
                    raise socket.error

                # SEND
                send(x.encode('utf-8'), self.client_socket)

                # GET
                stream: bytes = recv(self.client_socket)
                stream_str: str = stream.decode("utf-8")
                print(stream_str)

            except (KeyboardInterrupt, socket.error) as e:
                print(f"[close] {e}")
                Live = False
                break


if __name__ == '__main__':
    UdsTcpClient("./ech.socket").main_loop()
    # UdsUdpClient("./ech.socket").main_loop()
    #
    # Ip4TcpClient("127.0.0.1", 8919).main_loop()
    # Ip4UdpClient("127.0.0.1", 8919).main_loop()

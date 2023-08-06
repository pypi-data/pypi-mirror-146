from datalink_levl.helpful import recvfrom, sendto
from datalink_levl.server_datalink import _UdsServer, _Ip4Server
from transport_levl.server_transport import UdpServer, TcpServer


class UdsUdpServer(_UdsServer, UdpServer):
    def __init__(self, socket_file_name: str):
        super().__init__(socket_file_name)

    def main_loop(self):
        print(f"Run Server Uds UDP: {self.SOCKET_FILE}")

        Live = True
        while Live:
            try:

                # GET
                stream, client_acres = self.server_socket.recvfrom(1024)  # !!!!
                stream_str: str = stream.decode("utf-8")
                print(stream_str)

                # SEND в udp uds не получиться отправлять данные, так как у нас одинаковые адреса с клиентом
                # self.server_socket.sendto("[+]".encode("utf-8"), client_acres

            except KeyboardInterrupt as e:
                print(f"[close] {e}")
                Live = False
                break


class Ip4UdpServer(_Ip4Server, UdpServer):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def main_loop(self):
        print(f"Run Server Ip4 UDP: {self.Ip}:{self.Port}")

        Live = True
        while Live:
            try:

                # GET
                stream, client_acres = recvfrom(self.server_socket)
                stream_str: str = stream.decode("utf-8")
                print(stream_str)

                # SEND
                sendto("[+]".encode("utf-8"), self.server_socket, client_acres)

            except KeyboardInterrupt as e:
                print(f"[close] {e}")
                Live = False
                break


class UdsTcpServer(_UdsServer, TcpServer):
    def __init__(self, socket_file_name: str):
        super().__init__(socket_file_name)

    def main_loop(self):
        print(f"Run Server Uds TCP: {self.SOCKET_FILE}")
        self._main_loop()


class Ip4TcpServer(_Ip4Server, TcpServer):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def main_loop(self):
        print(f"Run Server Ip4 TCP: {self.Ip}:{self.Port}")
        self._main_loop()


if __name__ == '__main__':
    UdsTcpServer("./ech.socket").main_loop()
    # UdsUdpServer("./ech.socket").main_loop()
    #
    # Ip4TcpServer("127.0.0.1", 8919).main_loop()
    # Ip4UdpServer("127.0.0.1", 8919).main_loop()

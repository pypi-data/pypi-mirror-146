from async_socket.transport_levl.client_transport import ClientIpAsync
from general_settings import port, host

if __name__ == '__main__':
    # https://docs.python.org/3/library/asyncio-stream.html
    message = ''
    while message != "exit":
        message = input(":::")
        ClientIpAsync(
            host=host,
            port=port
        ).send(
            message_to_server=message,
            send_to_server=ClientIpAsync.base_send_to_server,
        )

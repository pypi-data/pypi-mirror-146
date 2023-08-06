from async_socket.transport_levl.server_transport import ServerIpAsync
from general_settings import host, port


async def echo_server(message: str) -> str:
    return message


async def ack(message: str) -> str:
    return 'ok'


if __name__ == '__main__':
    # https://docs.python.org/3/library/asyncio-stream.html
    ServerIpAsync(
        host=host,
        port=port
    ).run(
        client_connected_cb=ServerIpAsync.base_handle,
        callback_build_send_data=ack
    )

from asyncio import start_server, StreamReader, StreamWriter, run
from asyncio.base_events import Server
from functools import partial
from typing import Optional, Any, Coroutine, Callable, Protocol

from logsmal import logger

from helpful import recv, sendto


class CallableBuildSendData(Protocol):
    def __call__(
            self,
            _reader: StreamReader,
            _writer: StreamWriter,
            _callback_build_send_data: Callable[[str], None]
    ) -> Coroutine[Any, Any, None]: ...


class ServerIpAsync:

    def __init__(self, host: str, port: int, ):
        self.host = host
        self.port = port
        self.server: Optional[Coroutine[Any, Any, Server]] = None
        self.address: Optional[str] = None

    def run(
            self,
            client_connected_cb: CallableBuildSendData,
            callback_build_send_data: Callable[[str], Any]
    ):
        """
        Запустить сервер

        :param client_connected_cb: Низкоуровневая функция для обработки клиента при подключение
        :param callback_build_send_data: Функция для обработки данных от клиента
        """
        client_connected_cb = partial(
            client_connected_cb,
            _callback_build_send_data=callback_build_send_data
        )

        async def _self():
            self.server = await start_server(
                client_connected_cb=client_connected_cb,
                host=self.host,
                port=self.port
            )
            self.address = ', '.join(str(sock.getsockname()) for sock in self.server.sockets)
            logger.success(f'Serving on {self.address}', 'START')
            async with self.server:
                await self.server.serve_forever()

        run(_self())

    @staticmethod
    async def base_handle(
            _reader: StreamReader,
            _writer: StreamWriter,
            _callback_build_send_data: Callable[[str], Any]
    ):
        """
        - Получить данные от сервера
        - Отправить эти данны в функцию `_callback_build_send_data`
        - Получить результат из функции и отправить его клиенту

        :param _callback_build_send_data:
        :param _reader:
        :param _writer:
        """
        # Получить сообщение
        message: str = str(await recv(_reader))
        address_client = _writer.get_extra_info('peername')
        logger.info(f"Received {message} from {address_client}", 'RECV')
        # Логика отправки сообщения
        data = ''
        try:
            # Вызываем пользовательскую функцию
            data = await _callback_build_send_data(message)
        except Exception as e:
            # Если возникло исключение, то уведомляем клиента
            data = f"Error: {str(e)}"
            logger.error(str(e), 'Exception')
        finally:
            # Отправить сообщение
            await sendto(data, _writer)
            logger.info(f"Send {data} from {address_client}", 'SEND')
            # Закрыть соединение с клиентом
            _writer.close()
            logger.info(f"{address_client}", 'CLOSE')


async def echo_server(message: str) -> str:
    return message.upper()


async def ack(message: str) -> str:
    return 'ok'


if __name__ == '__main__':
    ServerIpAsync(
        host='127.0.0.1',
        port=8888
    ).run(
        client_connected_cb=ServerIpAsync.base_handle,
        callback_build_send_data=ack
    )

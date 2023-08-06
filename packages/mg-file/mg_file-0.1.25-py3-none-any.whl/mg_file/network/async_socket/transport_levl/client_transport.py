from asyncio import open_connection, run, StreamReader, StreamWriter
from asyncio.base_events import Server
from typing import Any, Coroutine, Optional
from typing import Protocol

from logsmal import logger

from helpful import sendto, recv


class CallableSendToServer(Protocol):
    def __call__(
            self,
            message_to_server: Any,
            _reader: StreamReader,
            _writer: StreamWriter,
    ) -> Coroutine[Any, Any, None]: ...


class ClientIpAsync:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server: Optional[Coroutine[Any, Any, Server]] = None
        self.address: Optional[str] = None

    def send(
            self,
            message_to_server: str,
            send_to_server: CallableSendToServer,
    ):
        """
        Отправить сообщение на сервер

        :param message_to_server: Тело сообщения
        :param send_to_server: Низкоуровневая функция реализующая логику отправки сообщения
        """

        async def _self():
            reader, writer = await open_connection(host=self.host, port=self.port)
            logger.success(f'Connect', 'Connect')
            await send_to_server(
                message_to_server=message_to_server,
                _reader=reader,
                _writer=writer
            )

        return run(_self())

    @staticmethod
    async def base_send_to_server(
            message_to_server: Any,
            _reader: StreamReader,
            _writer: StreamWriter,
    ):
        """
        Стандартная низкоуровневая функция реализующая логику отправки сообщения

        :param message_to_server: Тело сообщения
        :param _reader:
        :param _writer:
        """
        # Отправить сообщение
        await sendto(message_to_server, _writer)
        logger.info(f'Send: {message_to_server!r}', 'SEND')
        # Поучить ответ
        data = await recv(_reader)
        logger.info(f'Received: {data}', 'RECV')
        # Отсоединиться от сервера
        _writer.close()
        await _writer.wait_closed()
        logger.info('Close the connection', 'CLOSE')


if __name__ == '__main__':
    message = input(":::")
    ClientIpAsync('127.0.0.1', 8888).send(
        message_to_server=message,
        send_to_server=ClientIpAsync.base_send_to_server,
    )

from asyncio import StreamReader, StreamWriter
from pickle import dumps, loads
from typing import Any, Final

SIZE_BUFFER: Final[int] = 8  # Размер числа которое содержит размер всего пакета.


async def sendto(data: Any, writer: StreamWriter):
    """Отправить данные в сокет"""
    # Сереализуем данные
    data_b: bytes = dumps(data, protocol=3)
    # Получаем длину данных, и сераилизуем её
    len_b: bytes = len(data_b).to_bytes(SIZE_BUFFER, byteorder='big')
    # Отправляем размер данных
    writer.write(len_b)
    await writer.drain()
    # Отправляем данные
    writer.write(data_b)
    await writer.drain()


async def recv(reader: StreamReader):
    """Получить данные из сокета"""
    # Получаем размер данных
    size_data = await reader.read(SIZE_BUFFER)
    # Если есть размер
    if size_data:
        # Получаем полезные данные
        data_b = await reader.read(int.from_bytes(size_data, byteorder="big"))
        # Десереализовать данные
        return loads(data_b)
    else:
        return b''

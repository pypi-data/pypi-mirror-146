import socket
from pickle import dumps, loads
from typing import Any, Final, Union

SIZE_BUFFER: Final[int] = 8  # Размер числа которое содержит размер всего пакета.


def send(data: Any, client_socket: socket.socket):
    data_b: bytes = dumps(data, protocol=3)  # Сереализуем данные
    len_b: bytes = len(data_b).to_bytes(SIZE_BUFFER, byteorder='big')  # Получаем длину данных, и сераилизуем её

    client_socket.send(len_b)  # Отправляем размер данных
    client_socket.send(data_b)  # Отправляем данные


def sendto(data: Any, client_socket: socket.socket, client_acres: Union[tuple, str]):
    data_b: bytes = dumps(data, protocol=3)  # Сереализуем данные
    len_b: bytes = len(data_b).to_bytes(SIZE_BUFFER, byteorder='big')  # Получаем длину данных, и сераилизуем её

    client_socket.sendto(len_b, client_acres)  # Отправляем размер данных
    client_socket.sendto(data_b, client_acres)  # Отправляем данные


def recv(user: socket.socket):
    size_data = user.recv(SIZE_BUFFER)  # Получаем размер данных

    if size_data:  # Если есть размер
        data_b = user.recv(int.from_bytes(size_data, byteorder="big"))  # Получаем данные
        return loads(data_b)  # Десереализовать данные
    else:
        return b''


def recvfrom(user: socket.socket):
    size_data, client_acres = user.recvfrom(SIZE_BUFFER)  # Получаем размер данных

    if size_data:  # Если есть размер
        data_b, client_acres = user.recvfrom(int.from_bytes(size_data, byteorder="big"))  # Получаем данные
        return loads(data_b), client_acres  # Десереализовать данные
    else:
        return b''

'''Создать простой TCP-сервер, который принимает от клиента строку (порциями по 1 КБ) и возвращает ее. (Эхо-сервер).
Сервер должен выводить в консоль служебные сообщения (с пояснениями) при наступлении любых событий:
Запуск сервера;
Начало прослушивания порта;
Подключение клиента;
Прием данных от клиента;
Отправка данных клиенту;
Отключение клиента;
Остановка сервера'''
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 12345

server_socket.bind((host, port))

print("Запуск сервера")
print(f"Начало прослушивания порта {port}")

server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключение клиента {addr}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        response = 'test'
        print(f"Прием данных от клиента: {data.decode()}")

        client_socket.sendall(data)
        print(f"Отправка данных клиенту: {data.decode()}")

    print(f"Отключение клиента {addr}")
    client_socket.close()

print("Остановка сервера")
server_socket.close()

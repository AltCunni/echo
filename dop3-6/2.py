'''Напишите простой TCP-клиент, который устанавливает соединение с сервером, считывает строку со стандартного ввода и посылает его серверу.
Клиент должен выводить в консоль служебные сообщения (с пояснениями) при наступлении любых событий:
Соединение с сервером;
Разрыв соединения с сервером;
Отправка данных серверу;
Прием данных от сервера.'''
import socket

def tcp_client():
    host = input("Enter server host: ")
    port = int(input("Enter server port number: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server {host}:{port}")

            while True:
                message = input("Enter message to send (or type 'exit' to close connection): ")

                if message.lower() == 'exit':
                    break

                client_socket.sendall(message.encode())
                print("Message sent to server")

                data = client_socket.recv(1024)
                if not data:
                    print("Connection closed by server")
                    break

                print(f"Received from server: {data.decode()}")

        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")

    print("Connection closed")

if __name__ == '__main__':
    tcp_client()

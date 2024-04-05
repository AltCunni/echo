import socket
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)


def load_known_clients():
    try:
        with open('known_clients.txt', 'r') as file:
            known_clients = {}
            for line in file:
                ip, name = line.strip().split(',')
                known_clients[ip] = name
            return known_clients
    except FileNotFoundError:
        return {}


def save_known_clients(known_clients):
    with open('known_clients.txt', 'w') as file:
        for ip, name in known_clients.items():
            file.write(f"{ip},{name}\n")


def identify_client(client_socket, client_address, known_clients):
    if client_address[0] in known_clients:
        client_name = known_clients[client_address[0]]
        client_socket.send(f"Welcome back, {client_name}!\n".encode('utf-8'))
        logging.info(f"Client {client_address} identified as {client_name}")
    else:
        client_socket.send("Hello! What's your name?\n".encode('utf-8'))
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        known_clients[client_address[0]] = client_name
        save_known_clients(known_clients)
        logging.info(f"New client {client_address} identified as {client_name}")


def identification_server():
    host = input("Enter host (default: localhost): ") or 'localhost'
    port = int(input("Enter port number (default: 12345): ") or 12345)

    known_clients = load_known_clients()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)

        logging.info(f"Server is listening on {host}:{port}")
        print(f"Server is listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            logging.info(f"Connection established from {addr}")

            with conn:
                identify_client(conn, addr, known_clients)


if __name__ == '__main__':
    identification_server()

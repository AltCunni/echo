import socket
import logging
import hashlib
import secrets

logging.basicConfig(filename='auth_server.log', level=logging.INFO)


class AuthServerSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_message(self, message):
        message_length = len(message)
        header = f"{message_length:<10}".encode('utf-8')
        self.sendall(header + message.encode('utf-8'))

    def receive_message(self):
        header = self.recv(10)
        message_length = int(header.strip())
        message = self.recv(message_length).decode('utf-8')
        return message


def load_users():
    try:
        with open('users.txt', 'r') as file:
            users = {}
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
            return users
    except FileNotFoundError:
        return {}


def save_users(users):
    with open('users.txt', 'w') as file:
        for username, password in users.items():
            file.write(f"{username},{password}\n")


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def generate_token():
    return secrets.token_hex(16)


def authenticate_client(client_socket, client_address, users):
    client_socket.send_message("Enter your username:")
    username = client_socket.receive_message()

    if username in users:
        client_socket.send_message("Enter your password:")
        password = client_socket.receive_message()

        if hash_password(password) == users[username]:
            token = generate_token()
            client_socket.send_message(f"Authentication successful. Your token: {token}")
            logging.info(f"Client {client_address} authenticated as {username}")
        else:
            client_socket.send_message("Authentication failed. Incorrect password.")
            logging.info(f"Client {client_address} failed authentication")
    else:
        client_socket.send_message("User not found. Please register.")
        logging.info(f"Client {client_address} not found in users")


def authentication_server():
    host = input("Enter host (default: localhost): ") or 'localhost'
    port = int(input("Enter port number (default: 12345): ") or 12345)

    users = load_users()

    with AuthServerSocket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)

        logging.info(f"Authentication server is listening on {host}:{port}")
        print(f"Authentication server is listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            logging.info(f"Connection established from {addr}")

            with conn:
                authenticate_client(conn, addr, users)


if __name__ == '__main__':
    authentication_server()

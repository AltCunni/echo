import socket
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)


def tcp_server():
    host = input("Enter host (default: localhost): ") or 'localhost'
    port = int(input("Enter port (default: 12345): ") or 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        logging.info(f"Server is listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            logging.info(f"Connection established from {addr}")

            with conn:
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    logging.info(f"Received message: {data}")
                    if data.strip() == 'exit':
                        logging.info("Client requested to close connection")
                        break

    logging.info("Server is no longer listening")

def tcp_client():
    host = input("Enter host (default: localhost): ") or 'localhost'
    port = int(input("Enter port (default: 12345): ") or 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        while True:
            message = input("Enter message: ")
            client_socket.sendall(message.encode('utf-8'))
            if message.strip() == 'exit':
                break

    print("Connection closed")

if __name__ == '__main__':
    tcp_server()
    tcp_client()

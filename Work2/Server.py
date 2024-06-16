import socket
import threading



arr_port = [10001, 10002, 10003,10004,10005]
port = int(input("Choose number port: "))
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_server.bind(('0.0.0.0', port))
sock_server.listen(1)

print(f"Server started on port {port}")

clients = []
def recv_from_server(sock_client, i):
    try:
        print(f"Connected to port {i} as client")
        while True:
            response = sock_client.recv(1024)
            if response:
                print(f"Response from port {i}: {response.decode()}")
            else:
                break
    except ConnectionError as e:
        print(f"Error communicating with port {i}: {e}")
    finally:
        sock_client.close()
        print(f"Client on port {i} closed")


def recv_respond_to_client(conn_socket, client_address):
    print('Start listening from', client_address)
    try:
        while True:
            data = conn_socket.recv(1024)
            if not data:
                break  # Exit the loop if no data is received
            print('Received from', client_address, 'text:', data.decode())
            conn_socket.send(f"world".encode())
    except ConnectionAbortedError:
        print('Connection aborted by the client:', client_address)
    finally:
        conn_socket.close()  # Close the connection
        print('Connection closed with', client_address)


# Attempt to connect to other ports as clients
for i in arr_port:
    if i != port:
        try:
            sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_client.connect(("127.0.0.1", i))
            sock_client.send(f"Hello its {port}".encode())
            clients.append(sock_client)
            threading.Thread(target=recv_from_server, args=(sock_client, i)).start()
        except ConnectionRefusedError:
            print(f"Could not connect to port {i}")
        except Exception as e:
            print(f"Unexpected error while connecting to port {i}: {e}")


# Server main loop
def accept_connections():
    while True:
        connect, client_address = sock_server.accept()
        print("New connection", client_address)
        threading.Thread(target=recv_respond_to_client, args=(connect, client_address)).start()


communication = threading.Thread(target=accept_connections)
communication.start()

communication.join()
for client in clients:
    client.close()
sock_server.close()

# import socket
# import threading

# # Lists to keep track of Publisher and Subscriber clients
# publishers = []
# subscribers = []

# # Flag to indicate server running state
# server_running = True

# # Function to handle client connections
# def handle_client(client_socket, client_address, role):
#     global publishers, subscribers, server_running

#     if role == "PUBLISHER":
#         publishers.append(client_socket)
#         print(f"[{client_address}] Connected as PUBLISHER")
#     elif role == "SUBSCRIBER":
#         subscribers.append(client_socket)
#         print(f"[{client_address}] Connected as SUBSCRIBER")

#     try:
#         while True:
#             message = client_socket.recv(1024).decode('utf-8')
#             if not message:
#                 break
#             if message.strip().lower() == "terminate":
#                 print(f"Received 'terminate' from {client_address}. Shutting down server.")
#                 server_running = False
#                 break
#             if role == "PUBLISHER":
#                 print(f"[{client_address}] PUBLISHER: {message}")
#                 # Broadcast message to all subscribers
#                 for subscriber in subscribers:
#                     subscriber.send(message.encode('utf-8'))
#     except:
#         pass
#     finally:
#         # Remove the client from respective list
#         if role == "PUBLISHER":
#             publishers.remove(client_socket)
#         elif role == "SUBSCRIBER":
#             subscribers.remove(client_socket)
#         client_socket.close()

# # Main server function
# def start_server(server_ip, server_port):
#     global server_running

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Server listening on {server_ip}:{server_port}")

#     try:
#         while server_running:
#             client_socket, client_address = server.accept()
#             # Receive the role of the client (PUBLISHER or SUBSCRIBER)
#             role = client_socket.recv(1024).decode('utf-8')
#             # Start a new thread to handle the client connection
#             client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, role))
#             client_thread.start()
#     except KeyboardInterrupt:
#         print("Server manually stopped.")
#     finally:
#         print("Server is shutting down.")
#         server.close()

# # Start the server
# start_server('0.0.0.0', 5000)

import socket
import threading

# Lists to keep track of Publisher and Subscriber clients
publishers = []
subscribers = []

# Flag to indicate server running state
server_running = True

# Function to handle client connections
def handle_client(client_socket, client_address, role):
    global publishers, subscribers, server_running

    if role == "PUBLISHER":
        publishers.append(client_socket)
        print(f"[{client_address}] Connected as PUBLISHER")
    elif role == "SUBSCRIBER":
        subscribers.append(client_socket)
        print(f"[{client_address}] Connected as SUBSCRIBER")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.strip().lower() == "terminate":
                print(f"Received 'terminate' from {client_address}. Shutting down server.")
                server_running = False
                break
            if role == "PUBLISHER":
                print(f"[{client_address}] PUBLISHER: {message}")
                # Broadcast message to all subscribers
                for subscriber in subscribers:
                    subscriber.send(message.encode('utf-8'))
    except:
        pass
    finally:
        # Remove the client from the respective list
        if role == "PUBLISHER":
            publishers.remove(client_socket)
        elif role == "SUBSCRIBER":
            subscribers.remove(client_socket)
        client_socket.close()

# Main server function
def start_server(server_ip, server_port):
    global server_running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    # List to keep track of all connected client sockets
    all_clients = []

    def accept_clients():
        while server_running:
            try:
                server.settimeout(1.0)  # Set a timeout to periodically check the server_running flag
                client_socket, client_address = server.accept()
                # Receive the role of the client (PUBLISHER or SUBSCRIBER)
                role = client_socket.recv(1024).decode('utf-8')
                # Add client to all_clients list
                all_clients.append(client_socket)
                # Start a new thread to handle the client connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, role))
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Exception: {e}")
                break

    try:
        # Start a thread to accept clients
        accept_thread = threading.Thread(target=accept_clients)
        accept_thread.start()

        # Wait for the server to stop running
        while server_running:
            pass

        print("Server is shutting down...")
    finally:
        # Close all client connections
        for client in all_clients:
            client.close()
        server.close()
        print("Server has shut down.")

# Start the server
start_server('0.0.0.0', 5000)

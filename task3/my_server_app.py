# import socket
# import threading

# # Dictionary to keep track of subscribers by topic
# topics = {}

# # Function to handle client connections
# def handle_client(client_socket, client_address, role, topic):
#     global topics

#     if role == "PUBLISHER":
#         print(f"[{client_address}] Connected as PUBLISHER on topic '{topic}'")
#     elif role == "SUBSCRIBER":
#         if topic not in topics:
#             topics[topic] = []
#         topics[topic].append(client_socket)
#         print(f"[{client_address}] Connected as SUBSCRIBER on topic '{topic}'")

#     try:
#         while True:
#             message = client_socket.recv(1024).decode('utf-8')
#             if not message or message.strip().lower() == "terminate":
#                 break
#             if role == "PUBLISHER":
#                 print(f"[{client_address}] PUBLISHER on '{topic}': {message}")
#                 # Broadcast message to all subscribers of the topic
#                 if topic in topics:
#                     for subscriber in topics[topic]:
#                         subscriber.send(message.encode('utf-8'))
#     except:
#         pass
#     finally:
#         # Remove the client from the respective list
#         if role == "SUBSCRIBER":
#             if topic in topics:
#                 topics[topic].remove(client_socket)
#         client_socket.close()

# # Main server function
# def start_server(server_ip, server_port):
#     global server_running

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Server listening on {server_ip}:{server_port}")

#     while True:
#         client_socket, client_address = server.accept()
#         # Receive the role and topic of the client (PUBLISHER or SUBSCRIBER, and the topic)
#         role = client_socket.recv(1024).decode('utf-8')
#         topic = client_socket.recv(1024).decode('utf-8')
#         # Start a new thread to handle the client connection
#         client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, role, topic))
#         client_thread.start()

# # Start the server
# start_server('0.0.0.0', 5000)

# import socket
# import threading

# # Dictionary to keep track of subscribers by topic
# topics = {}

# # Function to handle client connections
# def handle_client(client_socket, client_address, role, topic):
#     global topics

#     if role == "PUBLISHER":
#         print(f"[{client_address}] Connected as PUBLISHER on topic '{topic}'")
#     elif role == "SUBSCRIBER":
#         if topic not in topics:
#             topics[topic] = []
#         topics[topic].append(client_socket)
#         print(f"[{client_address}] Connected as SUBSCRIBER on topic '{topic}'")

#     try:
#         while True:
#             message = client_socket.recv(1024).decode('utf-8')
#             if not message:
#                 break
#             if message.strip().lower() == "terminate":
#                 print(f"Received 'terminate' from {client_address}. Disconnecting client.")
#                 break
#             if role == "PUBLISHER":
#                 print(f"[{client_address}] PUBLISHER on '{topic}': {message}")
#                 # Broadcast message to all subscribers of the topic
#                 if topic in topics:
#                     for subscriber in topics[topic]:
#                         subscriber.send(f"{topic}: {message}".encode('utf-8'))
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         # Remove the client from the respective list
#         if role == "SUBSCRIBER":
#             if topic in topics:
#                 topics[topic].remove(client_socket)
#         client_socket.close()

# # Main server function
# def start_server(server_ip, server_port):
#     global server_running

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Server listening on {server_ip}:{server_port}")

#     # List to keep track of all connected client sockets
#     all_clients = []

#     def accept_clients():
#         while server_running:
#             try:
#                 server.settimeout(1.0)  # Set a timeout to periodically check the server_running flag
#                 client_socket, client_address = server.accept()
#                 # Receive the role and topic of the client (PUBLISHER or SUBSCRIBER, and the topic)
#                 role = client_socket.recv(1024).decode('utf-8')
#                 topic = client_socket.recv(1024).decode('utf-8')
#                 # Add client to all_clients list
#                 all_clients.append(client_socket)
#                 # Start a new thread to handle the client connection
#                 client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, role, topic))
#                 client_thread.start()
#             except socket.timeout:
#                 continue
#             except Exception as e:
#                 print(f"Exception: {e}")
#                 break

#     try:
#         # Start a thread to accept clients
#         accept_thread = threading.Thread(target=accept_clients)
#         accept_thread.start()

#         # Wait for the server to stop running
#         while server_running:
#             pass

#         print("Server is shutting down...")
#     finally:
#         # Close all client connections
#         for client in all_clients:
#             client.close()
#         server.close()
#         print("Server has shut down.")

# # Start the server
# server_running = True
# start_server('0.0.0.0', 5000)

import socket
import threading

# Dictionary to keep track of subscribers by topic
topics = {}

# Function to handle client connections
def handle_client(client_socket, client_address, role, topic):
    global topics

    print(f"[{client_address}] Connected as {role} on topic '{topic}'")
    
    if role == "PUBLISHER":
        print(f"[{client_address}] Connected as PUBLISHER on topic '{topic}'")
    elif role == "SUBSCRIBER":
        if topic not in topics:
            topics[topic] = []
        topics[topic].append(client_socket)
        print(f"[{client_address}] Connected as SUBSCRIBER on topic '{topic}'")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.strip().lower() == "terminate":
                print(f"Received 'terminate' from {client_address}. Disconnecting client.")
                break
            if role == "PUBLISHER":
                print(f"[{client_address}] PUBLISHER on '{topic}': {message}")
                # Broadcast message to all subscribers of the topic
                if topic in topics:
                    for subscriber in topics[topic]:
                        try:
                            subscriber.send(f"{topic}: {message}".encode('utf-8'))
                        except:
                            print(f"Failed to send message to a subscriber.")
            else:
                print(f"[{client_address}] Received message: {message}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Remove the client from the respective list
        if role == "SUBSCRIBER":
            if topic in topics:
                topics[topic].remove(client_socket)
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
                # Receive the role and topic of the client (PUBLISHER or SUBSCRIBER, and the topic)
                role = client_socket.recv(1024).decode('utf-8')
                topic = client_socket.recv(1024).decode('utf-8')
                # Add client to all_clients list
                all_clients.append(client_socket)
                # Start a new thread to handle the client connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, role, topic))
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
server_running = True
start_server('0.0.0.0', 5000)

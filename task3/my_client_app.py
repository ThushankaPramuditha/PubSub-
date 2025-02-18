# import socket
# import sys
# import threading

# def handle_incoming_messages(client):
#     try:
#         while True:
#             message = client.recv(1024).decode('utf-8')
#             if not message:
#                 break
#             print(f"Message: {message}")
#     except:
#         pass
#     finally:
#         client.close()

# def start_client(server_ip, server_port, role, topic):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((server_ip, server_port))
#     # Send role and topic information to the server
#     client.send(role.encode('utf-8'))
#     client.send(topic.encode('utf-8'))

#     if role == "PUBLISHER":
#         while True:
#             message = input("Enter message: ")
#             if message.strip().lower() == "terminate":
#                 client.send(message.encode('utf-8'))
#                 break
#             client.send(message.encode('utf-8'))
#     elif role == "SUBSCRIBER":
#         # Start a thread to handle incoming messages
#         threading.Thread(target=handle_incoming_messages, args=(client,)).start()
#         while True:
#             if input().strip().lower() == "terminate":
#                 client.send("terminate".encode('utf-8'))
#                 break

#     client.close()

# if __name__ == "__main__":
#     if len(sys.argv) != 5:
#         print("Usage: my_client_app <server_ip> <server_port> <PUBLISHER|SUBSCRIBER> <TOPIC>")
#         sys.exit(1)

#     server_ip = sys.argv[1]
#     server_port = int(sys.argv[2])
#     role = sys.argv[3].upper()
#     topic = sys.argv[4].upper()

#     start_client(server_ip, server_port, role, topic)

# import socket
# import sys
# import threading

# def handle_incoming_messages(client):
#     try:
#         while True:
#             message = client.recv(1024).decode('utf-8')
#             if not message:
#                 break
#             print(f"Message: {message}")
#     except:
#         pass
#     finally:
#         client.close()

# def start_client(server_ip, server_port, role, topic):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((server_ip, server_port))
#     # Send role and topic information to the server
#     client.send(role.encode('utf-8'))
#     client.send(topic.encode('utf-8'))

#     if role == "PUBLISHER":
#         while True:
#             message = input("Enter message: ")
#             if message.strip().lower() == "terminate":
#                 client.send(message.encode('utf-8'))
#                 break
#             client.send(message.encode('utf-8'))
#     elif role == "SUBSCRIBER":
#         # Start a thread to handle incoming messages
#         threading.Thread(target=handle_incoming_messages, args=(client,)).start()
#         while True:
#             if input().strip().lower() == "terminate":
#                 client.send("terminate".encode('utf-8'))
#                 break

#     client.close()

# if __name__ == "__main__":
#     if len(sys.argv) != 5:
#         print("Usage: my_client_app <server_ip> <server_port> <PUBLISHER|SUBSCRIBER> <TOPIC>")
#         sys.exit(1)

#     server_ip = sys.argv[1]
#     server_port = int(sys.argv[2])
#     role = sys.argv[3].upper()
#     topic = sys.argv[4].upper()

#     start_client(server_ip, server_port, role, topic)

import socket
import sys
import threading

def handle_incoming_messages(client):
    try:
        while True:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message: {message}")
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client.close()

def start_client(server_ip, server_port, role, topic):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    # Send role and topic information to the server
    client.send(role.encode('utf-8'))
    client.send(topic.encode('utf-8'))

    if role == "PUBLISHER":
        while True:
            message = input("Enter message: ")
            if message.strip().lower() == "terminate":
                client.send(message.encode('utf-8'))
                break
            client.send(message.encode('utf-8'))
    elif role == "SUBSCRIBER":
        # Start a thread to handle incoming messages
        threading.Thread(target=handle_incoming_messages, args=(client,)).start()
        while True:
            if input().strip().lower() == "terminate":
                client.send("terminate".encode('utf-8'))
                break

    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: my_client_app <server_ip> <server_port> <PUBLISHER|SUBSCRIBER> <TOPIC>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4].upper()

    start_client(server_ip, server_port, role, topic)

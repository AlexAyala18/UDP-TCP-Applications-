import socket
import threading

HOST = '0.0.0.0'   # Listen on all interfaces
PORT = 12345

clients = []
usernames = []

# Broadcast message to all clients
def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                remove_client(client)

# Remove client
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        print(f"{username} disconnected")

        clients.remove(client)
        usernames.remove(username)
        client.close()

        broadcast(f"{username} left the chat\n".encode())

# Handle each client
def handle_client(conn, addr):
    print(f"Connected with {addr}")

    try:
        # Ask for username
        conn.send("USERNAME".encode())
        username = conn.recv(1024).decode()

        usernames.append(username)
        clients.append(conn)

        print(f"Username: {username}")

        broadcast(f"{username} joined the chat\n".encode())

        # Listen for messages
        while True:
            message = conn.recv(1024)
            if message:
                msg = f"{username}: {message.decode()}"
                print(msg)
                broadcast(msg.encode(), conn)
            else:
                remove_client(conn)
                break

    except:
        remove_client(conn)

# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
import socket
import threading

HOST = '127.0.0.1'  # Change if server is remote
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages from server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "USERNAME":
                username = input("Enter your username: ")
                client.send(username.encode())
            else:
                print(message)

        except:
            print("Connection closed")
            client.close()
            break

# Send messages to server
def send_messages():
    while True:
        message = input()
        client.send(message.encode())

# Start threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
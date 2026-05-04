import socket
import time

HOST = '127.0.0.1'
PORT = 12346

CHUNK_SIZE = 1024

def request_file():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    filename = input("Enter filename to request: ")
    client.send(filename.encode())

    # Receive response from server (OK + filesize)
    response = client.recv(1024).decode()

    if response.startswith("ERROR"):
        print("File not found on server")
        client.close()
        return

    # Parse response
    lines = response.split("\n")
    
    if len(lines) < 2 or not lines[1].isdigit():
        print("Invalid response from server:", response)
        client.close()
        return

    filesize = int(lines[1])

    # Start timing
    start_time = time.time()

    received_size = 0

    with open("received_" + filename, "wb") as f:
        while received_size < filesize:
            data = client.recv(CHUNK_SIZE)
            if not data:
                break
            f.write(data)
            received_size += len(data)

    end_time = time.time()

    # Metrics
    total_time = end_time - start_time
    throughput = filesize / total_time if total_time > 0 else 0

    print("\n--- Transfer Complete ---")
    print(f"File size: {filesize} bytes")
    print(f"Time taken: {total_time:.4f} seconds")
    print(f"Throughput: {throughput:.2f} bytes/sec")

    client.close()

if __name__ == "__main__":
    request_file()
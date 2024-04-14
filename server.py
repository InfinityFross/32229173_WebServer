import socket
import threading

def handle_client(client_socket):
    # Initialize response_data
    response_data = b""

    request_data = client_socket.recv(1024).decode("utf-8")
    print(request_data)

    # Split the request data by spaces
    request_parts = request_data.split(' ')

    # Check if the request data contains at least two elements
    if len(request_parts) >= 2:
        # Extract the request method and path
        request_method = request_parts[0]
        request_path = request_parts[1]
        
        # Prepare the response
        if request_method == 'GET':
            if request_path == '/':
                with open('index.html', 'r') as file:
                    response_body = file.read()
                response_headers = "HTTP/1.1 200 OK\nContent-Type: text/html\nContepnt-Length: {}\n\n".format(len(response_body))
                response_data = response_headers.encode("utf-8") + response_body.encode("utf-8")
            else:
                response_headers = "HTTP/1.1 404 Not Found\n\n"
                response_data = response_headers.encode("utf-8")
        else:
            response_headers = "HTTP/1.1 501 Not Implemented\n\n"
            response_data = response_headers.encode("utf-8")

    # Send the response
    client_socket.sendall(response_data)
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 81))
    server_socket.listen(5)
    print("Server listening on port 81...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected to", addr)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
import socket

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind(('127.0.0.1', 8080))

ServerSocket.listen(10)
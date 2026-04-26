# import socket library
import socket

import threading
import os
import datetime
from email.utils import formatdate, parsedate_to_datetime

def client_thread(connectionSocket, addr):
    # show IP address of HTTP request
    print('Connection IP: ', addr)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    connectionSocket.settimeout(3)

    while True:
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        body = "<html><body><h1>400 Bad Request</h1></body></html>"
        response = (
            "HTTP/1.1 400 Bad Request\r\n"
            f"Date: {date}\r\n"
            "Server: COMP2022WebServer\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
            f"{body}"
        )

        try:
            # receive and decode clients' request into string
            all_request = connectionSocket.recv(4096).decode()
            if not all_request:
                connectionSocket.close()
                break
        except socket.timeout:
            connectionSocket.close()
            break

        print(all_request)
        request = all_request.splitlines()[0].strip().split()
        hostname = "N/A"
        for line in all_request.splitlines():
            if line.lower().startswith("host:"):
                hostname = line.split(":", 1)[1].strip()
                break
        if len(request) == 3 and request[2].startswith("HTTP/"):
            command, path, version = request
            filepath = '/index.html' if (path == '/index.html' or path == "/") else 'file' + path

            if command not in ["GET", "HEAD"]:
                write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 400)
                connectionSocket.send(response.encode())
                connectionSocket.close()
                break

            if version == "HTTP/1.1":
                connection_type = "keep-alive"
            else:
                connection_type = "close"
            for line in all_request.splitlines():
                if line.lower().startswith("connection:"):
                    connection_type = line.split(":", 1)[1].strip().lower()
                    break

            if filepath not in ('/index.html', '/') and os.path.exists(filepath):
                last_modified = formatdate(os.path.getmtime(filepath), localtime=False, usegmt=True)

                if filepath.endswith('.txt'):
                    content_type = "text/plain"
                    with open(filepath, "r") as f:
                        content = f.read().encode()
                elif filepath.endswith('.pdf'):
                    content_type = "application/pdf"
                    with open(filepath, "rb") as f:
                        content = f.read()
                elif filepath.endswith('.jpg'):
                    content_type = "image/jpeg"
                    with open(filepath, "rb") as f:
                        content = f.read()
                elif filepath.endswith('.png'):
                    content_type = "image/png"
                    with open(filepath, "rb") as f:
                        content = f.read()
                elif "." in filepath:
                    body = "<html><body><h1>403 Forbidden</h1></body></html>"
                    response = (
                        "HTTP/1.1 403 Forbidden\r\n"
                        f"Date: {date}\r\n"
                        "Server: COMP2022WebServer\r\n"
                        f"Content-Length: {len(body.encode())}\r\n"
                        f"Connection: {connection_type}\r\n"
                        f"Content-Type: text/html\r\n\r\n"
                        f"{body}"
                    )
                    write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 403)
                    connectionSocket.send(response.encode())
                    if connection_type == "close":
                        connectionSocket.close()
                        break
                    else:
                        continue
                else:
                    write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 400)
                    connectionSocket.send(response.encode())
                    connectionSocket.close()
                    break

                for line in all_request.splitlines():
                    if line.lower().startswith("if-modified-since:"):
                        if_modified_since = line.split(":", 1)[1].strip()
                        try:
                            if int(parsedate_to_datetime(if_modified_since).timestamp()) >= int(
                                    os.path.getmtime(filepath)):
                                response = (
                                    "HTTP/1.1 304 Not Modified\r\n"
                                    f"Date: {date}\r\n"
                                    "Server: COMP2022WebServer\r\n"
                                    f"Last-Modified: {last_modified}\r\n"
                                    f"Connection: {connection_type}\r\n\r\n"
                                )
                                write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 304)
                                connectionSocket.send(response.encode())
                                if connection_type == "close":
                                    connectionSocket.close()
                                    break
                                else:
                                    continue
                        except Exception as e:
                            pass

                if command == "GET":
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Date: {date}\r\n"
                        "Server: COMP2022WebServer\r\n"
                        f"Last-Modified: {last_modified}\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        f"Connection: {connection_type}\r\n"
                        f"Content-Type: {content_type}\r\n\r\n"
                    )
                    write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 200)
                    # reply to the client with their http requests
                    connectionSocket.send(response.encode())
                    connectionSocket.send(content)

                if command == "HEAD":
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Date: {date}\r\n"
                        "Server: COMP2022WebServer\r\n"
                        f"Last-Modified: {last_modified}\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        f"Connection: {connection_type}\r\n"
                        f"Content-Type: {content_type}\r\n\r\n"
                    )
                    write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 200)
                    # reply to the client with their http requests
                    connectionSocket.send(response.encode())

            elif filepath in ('/index.html', '/'):
                if command == "GET":
                    body = "<html><body><h1>Hello! This is Jackie's server!</h1></body></html>"
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Date: {date}\r\n"
                        "Server: COMP2022WebServer\r\n"
                        f"Content-Length: {len(body.encode())}\r\n"
                        f"Connection: {connection_type}\r\n"
                        f"Content-Type: text/html\r\n\r\n"
                        f"{body}"
                    )
                    write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 200)
                    connectionSocket.send(response.encode())
                elif command == "HEAD":
                    body = "<html><body><h1>Hello! This is Jackie's server!</h1></body></html>"
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Date: {date}\r\n"
                        "Server: COMP2022WebServer\r\n"
                        f"Content-Length: {len(body.encode())}\r\n"
                        f"Connection: {connection_type}\r\n"
                        f"Content-Type: text/html\r\n\r\n"
                    )
                    write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 200)
                    connectionSocket.send(response.encode())
            else:
                body = "<html><body><h1>404 File Not Found</h1></body></html>"
                response = (
                    "HTTP/1.1 404 File Not Found\r\n"
                    f"Date: {date}\r\n"
                    "Server: COMP2022WebServer\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(body.encode())}\r\n"
                    f"Connection: {connection_type}\r\n\r\n"
                    f"{body}"
                )
                write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), path, 404)
                connectionSocket.send(response.encode())
        else:
            connection_type = "close"
            write(hostname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "N/A", 400)
            connectionSocket.send(response.encode())

        # close the connection with the client
        if connection_type == "close":
            connectionSocket.close()
            break
        else:
            continue

# to write the record into the log file
def write(host, accessTime, requested, statusCode):
    with log_lock:
        with open(logName, "a") as logFile:
            logFile.write(f"{host}, {accessTime}, {requested}, {statusCode}\n")

# main program
# create a socket, bind it and change into listening mode
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind(('0.0.0.0', 8080))
ServerSocket.listen(10)

# create log file with right directory
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")
os.makedirs(log_dir, exist_ok = True)
logName = os.path.join(log_dir, f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
log_lock = threading.Lock()

# infinite loop until user interrupt it or occurs errors
while True:
    # establish connection with client
    connectionSocket, addr = ServerSocket.accept()
    # create and start a new thread to handle connection
    threading.Thread(target = client_thread, args = (connectionSocket, addr)).start()

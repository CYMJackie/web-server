# web-server

## Project overview
This is a multi-threaded HTTP web server implemented using Python socket programming. 
It can handle basic HTTP requests, supports various status codes, and has log file recording capabilities. 
This server can run on a local area network and can be tested via a browser or a custom client program.

## Features

Multi-threaded architecture:Handles multiple client connections simultaneously.

Supported status codes:\
200 OK\
304 Not Modified\
400 Bad Request\
403 Forbidden\
404 File Not Found

Supported methods:\
GET command: Returns a file or HTML page.\
HEAD command: Returns only the header, excluding the body.\
Supported file types: .txt, .pdf, .jpg, .png

Logging:\
Each request corresponds to one record: (host, accessTime, requested, statusCode)\
User can try to read the log as a .csv file!

## Structures
server.py // main program\
file/ // folder for saving server file\
log/ // folder for saving server log

## Installation and execution

1. Ensure that Python 3.x is installed.
2. Open the file server.py with python IDE 
3. Change your server port and host to meet your requirement (Preset host 0.0.0.0:8080)
4. Keep all the device at the same network
5. Access server though browsers or programs!